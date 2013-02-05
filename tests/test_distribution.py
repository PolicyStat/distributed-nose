
import unittest
from optparse import OptionParser

from nose.config import Config

from distributed_nose.plugin import DistributedNose

from tests.dummy_tests import TC1, TC2, test_func1, test_func2

class TestTestSelection(unittest.TestCase):

    def setUp(self):
        self.plugin = DistributedNose()
        self.parser = OptionParser()

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

