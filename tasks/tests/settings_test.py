import configparser
import unittest
import unittest.mock as mock

import settings


class SettingTests(unittest.TestCase):
    @mock.patch('settings.os.path')
    def test_read_file_does_not_exist(self, mock_path):
        mock_path.isfile.return_value = False
        with self.assertRaises(Exception):
            settings.Settings().read('./womble.ini')
    
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
    def test_read_file_exists(self, mock_path):
        mock_path.isfile.return_value = True
        mock_config = mock.Mock()
        mock_config.read = mock.MagicMock()
        test_path = 'test path'
        settings.Settings(config=mock_config).read(test_path)
        mock_config.read.assert_called_with(test_path)
    
    @mock.patch('settings.os.path')
    def test_read_data_location_category_not_exists(self, mock_path):
        mock_path.isfile.return_value = True
        config = configparser.ConfigParser()
        target = settings.Settings(config=config)
        target.read('test path')
        with self.assertRaises(Exception):
            result = target.data_location
    
    @mock.patch('settings.os.path')
    def test_read_data_location_exists(self, mock_path):
        self._test_setting_exists(mock_path, 'data.location', '/folder', 'data_location')

    @mock.patch('settings.os.path')
    def test_read_data_location_does_not_exist(self, mock_path):
        self._test_setting_not_exists(mock_path, 'data_location')
    
    @mock.patch('settings.os.path')
    def test_read_data_pending_filename_exists(self, mock_path):
        self._test_setting_exists(mock_path, 'data.pending.filename', 'pending.dat', 'data_pending_filename')
    
    @mock.patch('settings.os.path')
    def test_read_data_pending_filename_not_exists(self, mock_path):
        self._test_setting_not_exists(mock_path, 'data_pending_filename')
    
    @mock.patch('settings.os.path')
    def test_read_data_done_filename_exists(self, mock_path):
        self._test_setting_exists(mock_path, 'data.done.filename', 'done.dat', 'data_done_filename')
    
    @mock.patch('settings.os.path')
    def test_read_data_done_filename_not_exists(self, mock_path):
        self._test_setting_not_exists(mock_path, 'data_done_filename')

    def _test_setting_not_exists(self, mock_path, test_property_name):
        mock_path.isfile.return_value = True
        config = configparser.ConfigParser()
        config['general'] = {}
        target = settings.Settings(config=config)
        target.read('test path')
        with self.assertRaises(Exception):
            getattr(target, test_property_name)

    def _test_setting_exists(self, mock_path, key, expected_value, test_property_name):
        mock_path.isfile.return_value = True
        config = configparser.ConfigParser()
        config['general'] = {}
        config['general'][key] = expected_value
        target = settings.Settings(config=config)
        target.read('test path')
        result = getattr(target, test_property_name)
        self.assertEqual(expected_value, result)
