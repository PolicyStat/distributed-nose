
import logging

from nose.plugins.base import Plugin

logger = logging.getLogger('distributed_runs')

class DistributedRuns(Plugin):
    """
    Distribute a test run shared-nothing style by specifying the total number
    of runners and a unique ID for this runner.
    """
    name = 'distributed-runs'

    def __init__(self):
        Plugin.__init__(self)

        self.node_count = None
        self.node_id = None

    def options(self, parser, env):
        parser.add_option(
            "--distributed-nodes",
            action="store",
            dest="distributed_nodes",
            default=env.get('NOSE_DISTRIBUTED_NODES', 1),
            metavar="DISTRIBUTED_NODES",
            help="Across how many nodes are tests being distributed?",
        )
        parser.add_option(
            "--distributed-node-number",
            action="store",
            dest="distributed_node_number",
            default=env.get('NOSE_DISTRIBUTED_NODE_NUMBER', 1),
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

    def _options_are_valid(self):
        try:
            self.node_count = int(self.node_count)
        except ValueError:
            logger.critical("--distributed-nodes must be an integer")
            return False

        try:
            self.node_id = int(self.node_id)
        except ValueError:
            logger.critical("--distributed-node-number must be an integer")
            return False

        if self.node_id > self.node_count:
            logger.critical((
                "--distributed-node-number can't be larger "
                "than the number of nodes"
            ))
            return False

        if self.node_id < 1:
            logger.critical(
                "--distributed-node-number must be greater than zero"
            )
            return False

        return True


    def wantClass(self, cls):
        return None

    def wantFunction(self, cls):
        return None
