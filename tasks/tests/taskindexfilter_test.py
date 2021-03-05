import unittest
import unittest.mock as mock

import filters.taskindexfilter as taskindexfilter


class TaskIndexFilterTests(unittest.TestCase):
    def test_constructor_sets_index(self):
        target = taskindexfilter.TaskIndexFilter(mock.Mock(), 9)
        self.assertEqual(9, target.index)

    def test_is_match_returns_true_on_matching_index(self):
        mock_context = mock.Mock()
        task = mock.Mock()
        task.index = 1
        self.assertTrue(taskindexfilter.TaskIndexFilter(mock_context, 1).is_match(task))

    def test_is_match_returns_false_on_non_matching_index(self):
        mock_context = mock.Mock()
        task = mock.Mock()
        task.index = 1
        self.assertFalse(taskindexfilter.TaskIndexFilter(mock_context, 2).is_match(task))


class TaskIndexFilterParserTests(unittest.TestCase):
    def test_parse_integer_returns_filter(self):
        mock_context = mock.Mock()
        target = taskindexfilter.TaskIndexFilterParser().parse(mock_context, '13')
        self.assertIsInstance(target, taskindexfilter.TaskIndexFilter)
        self.assertEqual(13, target.index)

    def test_parse_non_integer_returns_none(self):
        mock_context = mock.Mock()
        target = taskindexfilter.TaskIndexFilterParser().parse(mock_context, 'words')
        self.assertIsNone(target)
