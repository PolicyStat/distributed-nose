
import unittest

from nose.plugins import PluginTester

from nose_distributed_runs.plugin import DistributedRuns

class TestSmoke(PluginTester):
    activate = ''
    plugins = [DistributedRuns()]
    args = [
        '--distributed-nodes=4',
        '--distributed-node-number=1',
    ]
    suitepath = 'tests.dummy_tests'

    def test_some_tests_found(self):
        # At least some tests should be located
        self.assertTrue(self.nose.success, self.output)

        num_tests_ran = self.nose.test.countTestCases()
        self.assertTrue(num_tests_ran > 0)

    def test_not_all_tests_found(self):
        # But we shouldn't have run all of the tests
        self.assertTrue(self.nose.success, self.output)

        num_tests_ran = self.nose.test.countTestCases()
        self.assertTrue(num_tests_ran < 12, num_tests_ran)

