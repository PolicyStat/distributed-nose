
import logging

from hash_ring import HashRing

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
            metavar="DISTRIBUTED_NODES",
            help="Across how many nodes are tests being distributed?",
        )
        parser.add_option(
            "--node-number",
            action="store",
            dest="distributed_node_number",
            default=env.get('NOSE_NODE_NUMBER', 1),
            metavar="DISTRIBUTED_NODE_NUMBER",
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
            metavar="DISTRIBUTED_DISABLED",
            help=((
                "Set this flag to disable distribution, "
                "despite having more than 1 node configured. "
                "This is useful if you use environment configs "
                "and want to temporarily disable test distribution."
            )),
        )

    def configure(self, options, config):
        self.node_count = options.distributed_nodes
        self.node_id = options.distributed_node_number

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

    def wantMethod(self, method):
        return self.validateName(method)

    def wantFunction(self, function):
        return self.validateName(function)
