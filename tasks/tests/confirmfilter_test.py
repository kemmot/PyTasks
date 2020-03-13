import unittest
import unittest.mock as mock

import filters.confirmfilter as confirmfilter


class ConfirmFilterTests(unittest.TestCase):
    def test_constructor_sets_action_name(self):
        action_name = 'test action name'
        filter = confirmfilter.ConfirmFilter(action_name)
        self.assertEqual(action_name, filter.action_name)

    def test_filter_items_does_not_prompt_for_zero_items(self):
        items = []
        filter = confirmfilter.ConfirmFilter('')
        mock_print = mock.MagicMock()
        with mock.patch('filters.confirmfilter.print', mock_print):
            filter.filter_items(items)
        mock_print.assert_not_called()

    def test_filter_items_prompts_for_one_item(self):
        mock_item = mock.Mock()
        mock_item.index = 1
        mock_item.name = 'test'
        items = [mock_item]
        filter = confirmfilter.ConfirmFilter('action')
        mock_print = mock.MagicMock()
        with mock.patch('filters.confirmfilter.print', mock_print):
            with mock.patch('filters.confirmfilter.input', return_value='no'):
                filter.filter_items(items)
        expected_message = 'action? [y/n]... ID: 1, name: test'
        mock_print.assert_called_once_with(expected_message)

    def test_filter_items_prompts_for_multiple_items(self):
        items = [mock.Mock(), mock.Mock()]
        filter = confirmfilter.ConfirmFilter('action')
        mock_print = mock.MagicMock()
        with mock.patch('filters.confirmfilter.print', mock_print):
            with mock.patch('filters.confirmfilter.input', return_value='no'):
                filter.filter_items(items)
        expected_message = 'action? [y/n]... 2 items'
        mock_print.assert_called_once_with(expected_message)

    def test_filter_items_returns_empty_list_on_negative_confirmation(self):
        items = [mock.Mock(), mock.Mock()]
        filter = confirmfilter.ConfirmFilter('action')
        mock_print = mock.MagicMock()
        with mock.patch('filters.confirmfilter.print', mock_print):
            with mock.patch('filters.confirmfilter.input', return_value='no'):
                result = filter.filter_items(items)
        self.assertEqual(0, len(result))

    def test_filter_items_returns_original_list_on_positive_confirmation(self):
        items = [mock.Mock(), mock.Mock()]
        filter = confirmfilter.ConfirmFilter('action')
        mock_print = mock.MagicMock()
        with mock.patch('filters.confirmfilter.print', mock_print):
            with mock.patch('filters.confirmfilter.input', return_value='yes'):
                result = filter.filter_items(items)
        self.assertEqual(items, result)

