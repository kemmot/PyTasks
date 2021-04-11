import unittest
import unittest.mock as mock

import filters.taskattributefilter as taskattributefilter


class TaskAttributeFilterTests(unittest.TestCase):
    def test_constructor_sets_name(self):
        target = taskattributefilter.TaskAttributeFilter(mock.Mock(), 'key', 'value')
        self.assertEqual('key', target.attribute_name)

    def test_constructor_sets_value(self):
        target = taskattributefilter.TaskAttributeFilter(mock.Mock(), 'key', 'value')
        self.assertEqual('value', target.attribute_value)

    def test_is_match_returns_false_on_missing_attribute(self):
        task = mock.Mock()
        task.attributes = {}
        task.attributes['partnumber'] = 'sea side'
        task_filter = taskattributefilter.TaskAttributeFilter(mock.Mock(), 'location', 'sea side')
        self.assertFalse(task_filter.is_match(task))

    def test_is_match_returns_false_on_different_attribute(self):
        task = mock.Mock()
        task.attributes = {}
        task.attributes['location'] = 'docks'
        task_filter = taskattributefilter.TaskAttributeFilter(mock.Mock(), 'location', 'sea side')
        self.assertFalse(task_filter.is_match(task))

    def test_is_match_returns_true_on_matching_value(self):
        task = mock.Mock()
        task.attributes = {}
        task.attributes['location'] = 'sea side'
        task_filter = taskattributefilter.TaskAttributeFilter(mock.Mock(), 'location', 'sea side')
        self.assertTrue(task_filter.is_match(task))

    def test_str_is_correct(self):
        task_filter = taskattributefilter.TaskAttributeFilter(mock.Mock(), 'location', 'sea side')
        description = str(task_filter)
        self.assertEqual('TaskAttributeFilter(location:sea side)', description)


class TaskAttributeFilterParserTests(unittest.TestCase):
    def test_parse_none_returns_none(self):
        target = taskattributefilter.TaskAttributeFilterParser().parse(mock.Mock(), None)
        self.assertIsNone(target)

    def test_parse_empty_string_returns_none(self):
        target = taskattributefilter.TaskAttributeFilterParser().parse(mock.Mock(), '')
        self.assertIsNone(target)

    def test_parse_non_empty_string_without_colon_returns_none(self):
        target = taskattributefilter.TaskAttributeFilterParser().parse(mock.Mock(), 'test')
        self.assertIsNone(target)

    def test_parse_non_empty_string_with_colon_returns_filter(self):
        target = taskattributefilter.TaskAttributeFilterParser().parse(mock.Mock(), 'test:one')
        self.assertIsInstance(target, taskattributefilter.TaskAttributeFilter)
        self.assertEqual('test', target.attribute_name)
        self.assertEqual('one', target.attribute_value)
