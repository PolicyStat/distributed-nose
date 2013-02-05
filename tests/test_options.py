
import unittest
from optparse import OptionParser

from nose_distributed_runs.plugin import DistributedRuns


class TestOptionValidation(unittest.TestCase):

    def setUp(self):
        self.plugin = DistributedRuns()
        self.parser = OptionParser()

        self.plugin.options(self.parser, env={})


    def test_defaults(self):
        args = []
        options, args = self.parser.parse_args(args)

        self.assertEqual(options.machine_count, 1)
        self.assertEqual(options.machine_id, 1)

