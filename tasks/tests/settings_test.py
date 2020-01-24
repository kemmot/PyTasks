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
    def test_read_connection_string_exists(self, mock_path):
        #mock_path.isfile.return_value = True
        #mock_config = mock.Mock()
        #mock_config.read = mock.MagicMock()
        #mock_config.has_option = mock.MagicMock(return_value=True)
        #s = settings.Settings(config=mock_config)
        #s.read('path')
        #connection_string = s.connection_string
        #self.assertEqual('result', connection_string)
        #mock_config.read.assert_called_with('general', 'storage.connectionstring')
        pass