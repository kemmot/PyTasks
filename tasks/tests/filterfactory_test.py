import unittest
from unittest import mock

import filters.filterfactory as filterfactory


class FilterFactoryTests(unittest.TestCase):
    def test_parse_raises_if_no_match_found(self):
        mock_parser1 = mock.Mock()
        mock_parser1.parse = mock.MagicMock(return_value=None)
        mock_parser2 = mock.Mock()
        mock_parser2.parse = mock.MagicMock(return_value=None)

        mock_context = mock.Mock()

        factory = filterfactory.FilterFactory()
        factory.register_type(mock_parser1)
        factory.register_type(mock_parser2)

        with self.assertRaises(Exception):
            factory.parse(mock_context, 'unknown')

        mock_parser1.parse.assert_called_once_with(mock_context, 'unknown')
        mock_parser2.parse.assert_called_once_with(mock_context, 'unknown')

    def test_parse_returns_matching_filter(self):
        mock_filter = mock.Mock()

        mock_parser = mock.Mock()
        mock_parser.parse = mock.MagicMock(return_value=mock_filter)

        mock_context = mock.Mock()

        factory = filterfactory.FilterFactory()
        factory.register_type(mock_parser)

        argument = 'unknown'
        result = factory.parse(mock_context, argument)
        mock_parser.parse.assert_called_with(mock_context, argument)
        self.assertEqual(mock_filter, result)
