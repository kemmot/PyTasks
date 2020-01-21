import unittest
import unittest.mock as mock

import filters.taskindexfilter as taskindexfilter


class TaskIndexFilterTests(unittest.TestCase):
    def test_is_match_returns_true_on_matching_index(self):
        task = mock.Mock()
        task.index = 1
        self.assertTrue(taskindexfilter.TaskIndexFilter(1).is_match(task))

    def test_is_match_returns_false_on_non_matching_index(self):
        task = mock.Mock()
        task.index = 1
        self.assertFalse(taskindexfilter.TaskIndexFilter(2).is_match(task))