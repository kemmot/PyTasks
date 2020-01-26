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
        expected_value = '/folder'
        config = configparser.ConfigParser()
        target = settings.Settings(config=config)
        target.read('test path')
        with self.assertRaises(Exception):
            result = target.data_location
    
    @mock.patch('settings.os.path')
    def test_read_data_location_exists(self, mock_path):
        mock_path.isfile.return_value = True
        expected_value = '/folder'
        config = configparser.ConfigParser()
        config['general'] = {}
        config['general']['data.location'] = expected_value
        target = settings.Settings(config=config)
        target.read('test path')
        result = target.data_location
        self.assertEqual(expected_value, result)

    @mock.patch('settings.os.path')
    def test_read_data_location_does_not_exist(self, mock_path):
        mock_path.isfile.return_value = True
        mock_config = mock.Mock()
        mock_config.read = mock.MagicMock()
        mock_config.has_option = mock.MagicMock(return_value=False)
        s = settings.Settings(config=mock_config)
        s.read('path')
        with self.assertRaises(Exception):
            data_location = s.data_location
        mock_config.has_option.assert_called_with('general', 'data.location')
    
    @mock.patch('settings.os.path')
    def test_read_data_pending_filename_not_exists(self, mock_path):
        mock_path.isfile.return_value = True
        expected_value = 'pending.dat'
        config = configparser.ConfigParser()
        config['general'] = {}
        target = settings.Settings(config=config)
        target.read('test path')
        with self.assertRaises(Exception):
            result = target.data_pending_filename
    
    @mock.patch('settings.os.path')
    def test_read_data_pending_filename_exists(self, mock_path):
        mock_path.isfile.return_value = True
        expected_value = 'pending.dat'
        config = configparser.ConfigParser()
        config['general'] = {}
        config['general']['data.pending.filename'] = expected_value
        target = settings.Settings(config=config)
        target.read('test path')
        result = target.data_pending_filename
        self.assertEqual(expected_value, result)
    
    @mock.patch('settings.os.path')
    def test_read_data_done_filename_exists(self, mock_path):
        mock_path.isfile.return_value = True
        expected_value = 'done.dat'
        config = configparser.ConfigParser()
        config['general'] = {}
        config['general']['data.done.filename'] = expected_value
        target = settings.Settings(config=config)
        target.read('test path')
        result = target.data_done_filename
        self.assertEqual(expected_value, result)
    
    @mock.patch('settings.os.path')
    def test_read_data_done_filename_not_exists(self, mock_path):
        mock_path.isfile.return_value = True
        expected_value = 'done.dat'
        config = configparser.ConfigParser()
        config['general'] = {}
        target = settings.Settings(config=config)
        target.read('test path')
        with self.assertRaises(Exception):
            result = target.data_done_filename
