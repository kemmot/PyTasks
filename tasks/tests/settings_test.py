import configparser
import unittest
import unittest.mock as mock

import settings


class SettingTests(unittest.TestCase):
    @mock.patch('settings.os.path')
    def test_read_command_annotate_confirm_exists(self, mock_path):
        self._test_read_boolean(mock_path, \
            'command.annotate.confirm', 'command_annotate_confirm')

    @mock.patch('settings.os.path')
    def test_read_command_default_exists(self, mock_path):
        self._test_setting_exists(mock_path, \
            'command.default', 'woble', 'command_default')

    @mock.patch('settings.os.path')
    def test_read_command_default_not_exists(self, mock_path):
        self._test_setting_not_exists(mock_path, 'command.default')

    @mock.patch('settings.os.path')
    def test_read_command_default_zero_items_exists(self, mock_path):
        self._test_setting_exists(mock_path, \
            'command.default.zero_items', 'woble', 'command_default_zero_items')

    @mock.patch('settings.os.path')
    def test_read_command_default_zero_items_not_exists(self, mock_path):
        self._test_setting_not_exists(mock_path, 'command.default.zero_items')

    @mock.patch('settings.os.path')
    def test_read_command_default_one_item_exists(self, mock_path):
        self._test_setting_exists(mock_path, \
            'command.default.one_item', 'woble', 'command_default_one_item')

    @mock.patch('settings.os.path')
    def test_read_command_default_one_item_not_exists(self, mock_path):
        self._test_setting_not_exists(mock_path, 'command.default.one_item')


    @mock.patch('settings.os.path')
    def test_read_command_default_multi_items_exists(self, mock_path):
        self._test_setting_exists(mock_path, \
            'command.default.multi_items', 'woble', 'command_default_multi_items')

    @mock.patch('settings.os.path')
    def test_read_command_default_multi_items_not_exists(self, mock_path):
        self._test_setting_not_exists(mock_path, 'command.default.multi_items')

    @mock.patch('settings.os.path')
    def test_read_command_done_confirm_exists(self, mock_path):
        self._test_read_boolean(mock_path, \
            'command.done.confirm', 'command_done_confirm')

    @mock.patch('settings.os.path')
    def test_read_command_modify_confirm_exists(self, mock_path):
        self._test_read_boolean(mock_path, \
            'command.modify.confirm', 'command_modify_confirm')

    @mock.patch('settings.os.path')
    def test_read_command_start_confirm_exists(self, mock_path):
        self._test_read_boolean(mock_path, \
            'command.start.confirm', 'command_start_confirm')

    @mock.patch('settings.os.path')
    def test_read_command_stop_confirm_exists(self, mock_path):
        self._test_read_boolean(mock_path, \
            'command.stop.confirm', 'command_stop_confirm')

    @mock.patch('settings.os.path')
    def test_read_data_done_filename_exists(self, mock_path):
        self._test_setting_exists(mock_path, 'data.done.filename', 'done.dat', 'data_done_filename')

    @mock.patch('settings.os.path')
    def test_read_data_done_filename_not_exists(self, mock_path):
        self._test_setting_not_exists(mock_path, 'data_done_filename')

    @mock.patch('settings.os.path')
    def test_read_data_location_category_not_exists(self, mock_path):
        mock_path.isfile.return_value = True
        config = configparser.ConfigParser()
        target = settings.Settings(config=config)
        target.read('test path')
        with self.assertRaises(Exception):
            target.data_location

    @mock.patch('settings.os.path')
    def test_read_data_location_exists(self, mock_path):
        self._test_setting_exists(mock_path, 'data.location', '/folder', 'data_location')

    @mock.patch('settings.os.path')
    def test_read_data_location_does_not_exist(self, mock_path):
        self._test_setting_not_exists(mock_path, 'data_location')

    @mock.patch('settings.os.path')
    def test_read_data_pending_filename_exists(self, mock_path):
        self._test_setting_exists(mock_path, \
            'data.pending.filename', 'pending.dat', 'data_pending_filename')

    @mock.patch('settings.os.path')
    def test_read_data_pending_filename_not_exists(self, mock_path):
        self._test_setting_not_exists(mock_path, 'data_pending_filename')

    @mock.patch('settings.os.path')
    def test_read_file_does_not_exist(self, mock_path):
        mock_path.isfile.return_value = False
        with self.assertRaises(Exception):
            settings.Settings().read('./womble.ini')

    @mock.patch('settings.os.path')
    def test_read_file_exists(self, mock_path):
        mock_path.isfile.return_value = True
        mock_config = mock.Mock()
        mock_config.read = mock.MagicMock()
        test_path = 'test path'
        settings.Settings(config=mock_config).read(test_path)
        mock_config.read.assert_called_with(test_path)

    @mock.patch('settings.os.path')
    def test_read_raises(self, mock_path):
        mock_path.isfile.return_value = True
        mock_config = mock.Mock()
        mock_config.read = mock.Mock()
        mock_config.read.side_effect = Exception()
        test_path = 'test path'
        with self.assertRaises(Exception):
            settings.Settings(config=mock_config).read(test_path)

    @mock.patch('settings.os.path')
    def test_read_command_table_column_separator_without_quotes(self, mock_path):
        self._test_setting_exists(mock_path, \
            'table.column.separator', '|', 'table_column_separator')

    @mock.patch('settings.os.path')
    def test_read_command_table_column_separator_with_quotes(self, mock_path):
        self._test_setting_exists(mock_path, \
            'table.column.separator', ' | ', 'table_column_separator', '" | "')

    @mock.patch('settings.os.path')
    def test_read_table_header_underline_exists(self, mock_path):
        self._test_read_boolean(mock_path, \
            'table.header.underline', 'table_header_underline')

    def _test_read_boolean(self, mock_path, key, test_property_name):
        self._test_setting_exists(mock_path, key, False, test_property_name)
        self._test_setting_exists(mock_path, key, True, test_property_name)
        # test that type is parsed and no longer a string
        with self.assertRaises(Exception):
            self._test_setting_exists(mock_path, key, 'False', test_property_name)
        with self.assertRaises(Exception):
            self._test_setting_exists(mock_path, key, 'True', test_property_name)
        self._test_setting_not_exists(mock_path, test_property_name)

    def _test_setting_not_exists(self, mock_path, test_property_name):
        mock_path.isfile.return_value = True
        config = configparser.ConfigParser()
        config['general'] = {}
        target = settings.Settings(config=config)
        target.read('test path')
        with self.assertRaises(Exception):
            getattr(target, test_property_name)

    def _test_setting_exists(self, mock_path, key, expected_value, test_property_name, configured_value=None):
        mock_path.isfile.return_value = True
        config = configparser.ConfigParser()
        config['general'] = {}
        if configured_value is None:
            config['general'][key] = str(expected_value)
        else:
            config['general'][key] = str(configured_value)
        target = settings.Settings(config=config)
        target.read('test path')
        result = getattr(target, test_property_name)
        self.assertEqual(expected_value, result)
