import unittest
import unittest.mock as mock

import filters.confirmfilter as confirmfilter


class ConfirmFilterTests(unittest.TestCase):
    def test_constructor_sets_action_name(self):
        mock_context = self.create_mock_context('no')
        action_name = 'test action name'
        filter = confirmfilter.ConfirmFilter(mock_context, action_name)
        self.assertEqual(action_name, filter.action_name)

    def test_filter_items_does_not_prompt_for_zero_items(self):
        mock_context = self.create_mock_context('no')
        items = []
        filter = confirmfilter.ConfirmFilter(mock_context, '')
        filter.filter_items(items)
        mock_context.console.input.assert_not_called()

    def test_filter_items_prompts_for_one_item(self):
        mock_context = self.create_mock_context('no')
        mock_item = mock.Mock()
        mock_item.index = 1
        mock_item.name = 'test'
        items = [mock_item]
        filter = confirmfilter.ConfirmFilter(mock_context, 'action')
        filter.filter_items(items)
        expected_message = 'action? [y/n]... ID: 1, name: "test"> '
        mock_context.console.input.assert_called_once_with(expected_message)

    def test_filter_items_prompts_for_multiple_items(self):
        mock_context = self.create_mock_context('no')
        items = [mock.Mock(), mock.Mock()]
        filter = confirmfilter.ConfirmFilter(mock_context, 'action')
        filter.filter_items(items)
        expected_message = 'action? [y/n]... 2 items> '
        mock_context.console.input.assert_called_once_with(expected_message)

    def test_filter_items_returns_empty_list_on_negative_confirmation(self):
        filter = confirmfilter.ConfirmFilter(self.create_mock_context('no'), 'action')
        items = [mock.Mock(), mock.Mock()]
        result = filter.filter_items(items)
        self.assertEqual(0, len(result))

    def test_filter_items_returns_original_list_on_positive_confirmation(self):
        filter = confirmfilter.ConfirmFilter(self.create_mock_context('yes'), 'action')
        items = [mock.Mock(), mock.Mock()]
        result = filter.filter_items(items)
        self.assertEqual(items, result)
    
    def create_mock_context(self, input_return):
        mock_context = mock.Mock()
        mock_context.console = mock.Mock()
        mock_context.console.input = mock.MagicMock(return_value=input_return)
        return mock_context
