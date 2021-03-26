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

    def test_string_representation_contains_class_and_index(self):
        description = str(taskindexfilter.TaskIndexFilter(mock.Mock(), 45))
        self.assertIn('TaskIndexFilter', description)
        self.assertIn('45', description)


class TaskIndexRangeFilterTests(unittest.TestCase):
    def test_constructor_sets_indexes(self):
        target = taskindexfilter.TaskIndexRangeFilter(mock.Mock(), 30, 199)
        self.assertEqual(30, target.start_index)
        self.assertEqual(199, target.end_index)

    def test_constructor_raises_when_range_end_before_start(self):
        with self.assertRaises(Exception):
            taskindexfilter.TaskIndexRangeFilter(mock.Mock(), 345, 23)

    def test_is_match_returns_true_on_start_of_range(self):
        mock_context = mock.Mock()
        task = mock.Mock()
        task.index = 75
        self.assertTrue(taskindexfilter.TaskIndexRangeFilter(mock_context, 75, 79).is_match(task))

    def test_is_match_returns_true_in_middle_of_range(self):
        mock_context = mock.Mock()
        task = mock.Mock()
        task.index = 77
        self.assertTrue(taskindexfilter.TaskIndexRangeFilter(mock_context, 75, 79).is_match(task))

    def test_is_match_returns_true_on_end_of_range(self):
        mock_context = mock.Mock()
        task = mock.Mock()
        task.index = 79
        self.assertTrue(taskindexfilter.TaskIndexRangeFilter(mock_context, 75, 79).is_match(task))

    def test_is_match_returns_false_before_range(self):
        mock_context = mock.Mock()
        task = mock.Mock()
        task.index = 1
        self.assertFalse(taskindexfilter.TaskIndexRangeFilter(mock_context, 301, 999).is_match(task))

    def test_is_match_returns_false_after_range(self):
        mock_context = mock.Mock()
        task = mock.Mock()
        task.index = 785
        self.assertFalse(taskindexfilter.TaskIndexRangeFilter(mock_context, 56, 784).is_match(task))

    def test_string_representation_contains_class_and_indexes(self):
        description = str(taskindexfilter.TaskIndexRangeFilter(mock.Mock(), 56, 784))
        self.assertIn('TaskIndexRangeFilter', description)
        self.assertIn('56', description)
        self.assertIn('784', description)

class TaskIndexFilterParserTests(unittest.TestCase):
    def test_parse_integer_returns_filter(self):
        mock_context = mock.Mock()
        target = taskindexfilter.TaskIndexFilterParser().parse(mock_context, '13')
        self.assertIsInstance(target, taskindexfilter.TaskIndexFilter)
        self.assertEqual(13, target.index)

    def test_parse_integer_range_returns_filter(self):
        mock_context = mock.Mock()
        target = taskindexfilter.TaskIndexFilterParser().parse(mock_context, '34-199')
        self.assertIsInstance(target, taskindexfilter.TaskIndexRangeFilter)
        self.assertEqual(34, target.start_index)
        self.assertEqual(199, target.end_index)

    def test_invalid_input_returns_none(self):
        mock_context = mock.Mock()
        self.assertIsNone(taskindexfilter.TaskIndexFilterParser().parse(mock_context, 'words'))

        # invalid or missing range end
        self.assertIsNone(taskindexfilter.TaskIndexFilterParser().parse(mock_context, '34-one'))
        self.assertIsNone(taskindexfilter.TaskIndexFilterParser().parse(mock_context, '34-'))

        # invalid or missing range start
        self.assertIsNone(taskindexfilter.TaskIndexFilterParser().parse(mock_context, 'one-14'))
        self.assertIsNone(taskindexfilter.TaskIndexFilterParser().parse(mock_context, '-14'))
