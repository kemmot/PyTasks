import unittest
import unittest.mock as mock

import filters.anybatchfilter as anybatchfilter


class AnyBatchFilterTests(unittest.TestCase):
    def test_constructor_succeeds(self):
        anybatchfilter.AnyBatchFilter(mock.Mock())

    def test_filter_items_calls_filter_items_on_subfilters(self):
        items = [mock.Mock(), mock.Mock(), mock.Mock()]

        filter1 = self._create_filter(False)
        filter2 = self._create_filter(False)

        batch_filter = anybatchfilter.AnyBatchFilter(mock.Mock())
        batch_filter.add_filter(filter1)
        batch_filter.add_filter(filter2)

        results = batch_filter.filter_items(items)
        self.assertEqual([], results)

        filter1.is_match.assert_called()
        filter2.is_match.assert_called()

    def test_is_match_does_not_return_item_if_no_subfilters_return_true(self):
        self._execute_is_match_test(False, [False, False, False])

    def test_is_match_does_return_item_if_only_some_subfilters_return_true(self):
        self._execute_is_match_test(True, [False, True, False])

    def test_is_match_returns_item_if_all_filters_return_true(self):
        self._execute_is_match_test(True, [True, True, True])

    def _execute_is_match_test(self, expected_result, filter_results):
        batch_filter = anybatchfilter.AnyBatchFilter(mock.Mock())
        for filter_result in filter_results:
            batch_filter.add_filter(self._create_filter(filter_result))
        self.assertEqual(expected_result, batch_filter.is_match(mock.Mock()))

    def _create_filter(self, return_value):
        mock_filter = mock.Mock()
        mock_filter.is_match = mock.MagicMock(return_value=return_value)
        return mock_filter
