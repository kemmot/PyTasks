import unittest
import unittest.mock as mock

import filters.alwaysfilter as alwaysfilter


class AlwaysFilterTests(unittest.TestCase):
    def test_is_match_returns_true(self):
        self.assertTrue(alwaysfilter.AlwaysFilter().is_match(mock.Mock()))
