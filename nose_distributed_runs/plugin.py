
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

        self.machine_count = None
        self.machine_id = None

    def options(self, parser, env):
        parser.add_option(
            "--dr-machine-count",
            action="store",
            dest="machine_count",
            default=env.get('NOSE_DR_MACHINE_COUNT', 1),
            metavar="DR_MACHINE_COUNT",
            help="Number of machines that will be running tests.",
        )
        parser.add_option(
            "--dr-machine-id",
            action="store",
            dest="machine_id",
            default=env.get('NOSE_DR_MACHINE_ID', 1),
            metavar="DR_MACHINE_ID",
            help="Which number is this machine? (1-indexed)",
        )

    def configure(self, options, config):
        self.machine_count = options.machine_count
        self.machine_id = options.machine_id

    def wantClass(self, cls):
        return None

    def wantFunction(self, cls):
        return None
