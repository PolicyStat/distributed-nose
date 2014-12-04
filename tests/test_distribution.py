
import inspect
import unittest
from optparse import OptionParser

from nose.config import Config
from nose.plugins import PluginTester

from distributed_nose.plugin import DistributedNose

from tests.dummy_tests import TC1, TC2, test_func1, test_func2


class TestTestSelection(unittest.TestCase):

    def setUp(self):
        self.plugin = DistributedNose()
        self.parser = OptionParser()

    def test_nontest_collection(self):
        plug = self.plugin
        plug.options(self.parser, env={})
        args = []
        options, _ = self.parser.parse_args(args)
        plug.configure(options, Config())

        # This is a contrived example; in practice, this can be triggered by
        # function proxies like wrapt.
        nontest = list()
        self.assertEqual(plug.validateName(nontest), None)

    def test_some_tests_found(self):
        # At least some tests should be located
        plug = self.plugin
        plug.options(self.parser, env={})
        args = ['--nodes=2', '--node-number=1']
        options, _ = self.parser.parse_args(args)
        plug.configure(options, Config())

        any_allowed = False

        for test in [TC1, TC2, test_func1, test_func2]:
            if plug.validateName(test) is None:
                any_allowed = True

        self.assertTrue(any_allowed)

    def test_not_all_tests_found(self):
        # But we shouldn't have run all of the tests
        plug = self.plugin
        plug.options(self.parser, env={})
        args = ['--nodes=2', '--node-number=1']
        options, _ = self.parser.parse_args(args)
        plug.configure(options, Config())

        all_allowed = True

        for test in [TC1, TC2, test_func1, test_func2]:
            if plug.validateName(test) is None:
                all_allowed = False

        self.assertFalse(all_allowed)


class TestClassDistribution(PluginTester, unittest.TestCase):
    plugins = [DistributedNose()]
    suitepath = 'tests.dummy_tests'
    activate = '--nodes=3'
    args = [
        '--node-number=1',
        '-v'  # get test names into output
    ]

    def _tests_run(self):
        test_lines = str(self.output).split('\n\n')[0].split('\n')
        return [line.split(' ... ')[0] for line in test_lines]


class TestClassDistributionOff(TestClassDistribution):
    def test_tc1_hashes_apart(self):
        testnames = self._tests_run()
        from_tc1 = [name for name in testnames if '.TC1)' in name]
        self.assertTrue(0 < len(from_tc1) < 4)

    def test_tc3_hashes_apart(self):
        testnames = self._tests_run()
        from_tc3 = [name for name in testnames if '.TC3)' in name]
        self.assertTrue(0 < len(from_tc3) < 4)

    def test_func1_excluded(self):
        self.assertTrue('tests.dummy_tests.test_func1' not in self._tests_run())

    def test_func2_included(self):
        self.assertTrue('tests.dummy_tests.test_func2' in self._tests_run())


class TestClassDistributionOn(TestClassDistribution):
    args = TestClassDistributionOff.args + ['--hash-by-class']

    def test_tc1_is_excluded(self):
        testnames = self._tests_run()
        from_tc1 = [name for name in testnames if '.TC1)' in name]
        self.assertTrue(len(from_tc1) == 0)

    def test_tc3_is_included(self):
        testnames = self._tests_run()
        from_tc3 = [name for name in testnames if '.TC3)' in name]
        self.assertTrue(len(from_tc3) == 4)

    # Function selection should not have changed.
    def test_func1_excluded(self):
        self.assertTrue('tests.dummy_tests.test_func1' not in self._tests_run())

    def test_func2_included(self):
        self.assertTrue('tests.dummy_tests.test_func2' in self._tests_run())
