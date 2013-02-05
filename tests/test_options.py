
import unittest
from optparse import OptionParser

from nose.config import Config

from nose_distributed_runs.plugin import DistributedRuns


class TestOptionValidation(unittest.TestCase):

    def setUp(self):
        self.plugin = DistributedRuns()
        self.parser = OptionParser()

    def test_defaults(self):
        self.plugin.options(self.parser, env={})
        args = []
        options, _  = self.parser.parse_args(args)

        self.assertEqual(options.distributed_node_number, 1)
        self.assertEqual(options.distributed_nodes, 1)

    def test_vanilla(self):
        self.plugin.options(self.parser, env={})
        args = ['--distributed-nodes=4', '--distributed-node-number=3']
        options, _ = self.parser.parse_args(args)
        self.plugin.enabled = True
        self.plugin.configure(options, Config())

        self.assertEqual(self.plugin.node_count, 4)
        self.assertEqual(self.plugin.node_id, 3)
        self.assertTrue(self.plugin.enabled)

    def test_env_configs(self):
        env = {'NOSE_DISTRIBUTED_NODES': 6, 'NOSE_DISTRIBUTED_NODE_NUMBER': 4}
        self.plugin.options(self.parser, env=env)
        options, _ = self.parser.parse_args([])
        self.plugin.enabled = True
        self.plugin.configure(options, Config())

        self.assertEqual(self.plugin.node_count, 6)
        self.assertEqual(self.plugin.node_id, 4)
        self.assertTrue(self.plugin.enabled)

    def test_integer_required_count(self):
        self.plugin.options(self.parser, env={})
        args = ['--distributed-nodes=foo', '--distributed-node-number=1']
        options, _ = self.parser.parse_args(args)
        self.plugin.configure(options, Config())

        self.assertFalse(self.plugin.enabled)

    def test_integer_required_id(self):
        self.plugin.options(self.parser, env={})
        args = ['--distributed-nodes=2', '--distributed-node-number=baz']
        options, _ = self.parser.parse_args(args)
        self.plugin.configure(options, Config())

        self.assertFalse(self.plugin.enabled)

    def test_id_in_range(self):
        self.plugin.options(self.parser, env={})
        args = ['--distributed-nodes=2', '--distributed-node-number=3']
        options, _ = self.parser.parse_args(args)
        self.plugin.configure(options, Config())

        self.assertFalse(self.plugin.enabled)


