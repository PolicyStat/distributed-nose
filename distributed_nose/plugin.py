
import logging

from hashring import HashRing

from nose.plugins.base import Plugin
from nose.util import test_address

logger = logging.getLogger('nose.plugins.distributed_nose')


class DistributedNose(Plugin):
    """
    Distribute a test run, shared-nothing style, by specifying the total number
    of runners and a unique ID for this runner.
    """
    name = 'distributed'

    def __init__(self):
        Plugin.__init__(self)

        self.node_count = None
        self.node_id = None
        self.hash_ring = None

    def options(self, parser, env):
        parser.add_option(
            "--nodes",
            action="store",
            dest="distributed_nodes",
            default=env.get('NOSE_NODES', 1),
            help="Across how many nodes are tests being distributed?",
        )
        parser.add_option(
            "--node-number",
            action="store",
            dest="distributed_node_number",
            default=env.get('NOSE_NODE_NUMBER', 1),
            help=(
                "Of the total nodes running distributed tests, "
                "which number is this node? (1-indexed)"
            ),
        )
        parser.add_option(
            "--distributed-disabled",
            action="store_true",
            dest="distributed_disabled",
            default=False,
            help=((
                "Set this flag to disable distribution, "
                "despite having more than 1 node configured. "
                "This is useful if you use environment configs "
                "and want to temporarily disable test distribution."
            )),
        )
        parser.add_option(
            "--hash-by-class",
            action="store_true",
            dest="distributed_hash_by_class",
            # any non-empty value enables
            default=bool(env.get('NOSE_HASH_BY_CLASS', False)),
            help=((
                "By default, tests are distributed individually. "
                "This results in the most even distribution and the"
                " best speed if all tests have the same runtime. "
                "However, it duplicates class setup/teardown work; "
                "set this flag to keep tests in the same class on the same node. "  # noqa
            )),
        )

    def configure(self, options, config):
        self.node_count = options.distributed_nodes
        self.node_id = options.distributed_node_number
        self.hash_by_class = options.distributed_hash_by_class

        if not self._options_are_valid():
            self.enabled = False
            return

        if options.distributed_disabled:
            self.enabled = False
            return

        if self.node_count > 1:
            # If the user gives us a non-1 count of distributed nodes, then
            # let's distribute their tests
            self.enabled = True

        self.hash_ring = HashRing(range(1, self.node_count + 1))

    def _options_are_valid(self):
        try:
            self.node_count = int(self.node_count)
        except ValueError:
            logger.critical("--nodes must be an integer")
            return False

        try:
            self.node_id = int(self.node_id)
        except ValueError:
            logger.critical("--node-number must be an integer")
            return False

        if self.node_id > self.node_count:
            logger.critical((
                "--node-number can't be larger "
                "than the number of nodes"
            ))
            return False

        if self.node_id < 1:
            logger.critical(
                "--node-number must be greater than zero"
            )
            return False

        return True

    def validateName(self, testObject):
        try:
            _, module, call = test_address(testObject)
        except TypeError:
            module = 'unknown'
            call = str(testObject)

        node = self.hash_ring.get_node('%s.%s' % (module, call))
        if node != self.node_id:
            return False

        return None

    def wantClass(self, cls):
        if not self.hash_by_class:
            # Defer to wantMethod.
            return None

        node = self.hash_ring.get_node(str(cls))
        if node != self.node_id:
            return False

        return None

    def wantMethod(self, method):
        if self.hash_by_class:
            # Don't override class selection decisions.
            return None

        return self.validateName(method)

    def wantFunction(self, function):
        # Always operate directly on bare functions.
        return self.validateName(function)
