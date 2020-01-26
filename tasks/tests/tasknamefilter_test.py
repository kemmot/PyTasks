import unittest
import unittest.mock as mock

import filters.tasknamefilter as tasknamefilter


class TaskNameFilterTests(unittest.TestCase):
    def test_constructor_sets_name(self):
        target = tasknamefilter.TaskNameFilter('test')
        self.assertEqual('test', target.name)

    def test_is_match_returns_true_on_matching_name(self):
        task = mock.Mock()
        task.name = 'test'
        self.assertTrue(tasknamefilter.TaskNameFilter('test').is_match(task))

    def test_is_match_returns_false_on_non_matching_index(self):
        task = mock.Mock()
        task.name = 'woble'
        self.assertFalse(tasknamefilter.TaskNameFilter('test').is_match(task))

    def test_is_match_returns_true_when_name_contains_same_case(self):
        task = mock.Mock()
        task.name = 'onetesttwo'
        self.assertTrue(tasknamefilter.TaskNameFilter('test').is_match(task))

    def test_is_match_returns_true_when_name_contains_different_case(self):
        task = mock.Mock()
        task.name = 'oneTESTtwo'
        self.assertTrue(tasknamefilter.TaskNameFilter('test').is_match(task))


class TaskNameFilterParserTests(unittest.TestCase):
    def test_parse_none_returns_none(self):
        target = tasknamefilter.TaskNameFilterParser().parse(None)
        self.assertIsNone(target)

    def test_parse_empty_string_returns_none(self):
        target = tasknamefilter.TaskNameFilterParser().parse('')
        self.assertIsNone(target)

    def test_parse_non_empty_string_returns_filter(self):
        target = tasknamefilter.TaskNameFilterParser().parse('test')
        self.assertIsInstance(target, tasknamefilter.TaskNameFilter)
        self.assertEqual('test', target.name)

    def test_parse_strips_forward_slashes(self):
        target = tasknamefilter.TaskNameFilterParser().parse('/test/')
        self.assertIsInstance(target, tasknamefilter.TaskNameFilter)
        self.assertEqual('test', target.name)
