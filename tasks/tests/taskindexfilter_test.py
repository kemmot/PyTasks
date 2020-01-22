import unittest
import unittest.mock as mock

import filters.taskindexfilter as taskindexfilter


class TaskIndexFilterTests(unittest.TestCase):
    def test_constructor_sets_index(self):
        filter = taskindexfilter.TaskIndexFilter(9)
        self.assertEqual(9, filter.index)

    def test_is_match_returns_true_on_matching_index(self):
        task = mock.Mock()
        task.index = 1
        self.assertTrue(taskindexfilter.TaskIndexFilter(1).is_match(task))

    def test_is_match_returns_false_on_non_matching_index(self):
        task = mock.Mock()
        task.index = 1
        self.assertFalse(taskindexfilter.TaskIndexFilter(2).is_match(task))


class TaskIndexFilterParserTests(unittest.TestCase):
    def test_parse_integer_returns_filter(self):
        filter = taskindexfilter.TaskIndexFilterParser().parse('13')
        self.assertIsInstance(filter, taskindexfilter.TaskIndexFilter)
        self.assertEqual(13, filter.index)

    def test_parse_non_integer_returns_none(self):
        filter = taskindexfilter.TaskIndexFilterParser().parse('words')
        self.assertIsNone(filter)
