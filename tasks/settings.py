import configparser
import logging
import os


class Settings:
    def __init__(self, config=None):
        self._category = 'general'
        if config is None:
            config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self._config = config
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def command_default(self):
        return self._get_value('command.default')

    @property
    def command_default_zero_items(self):
        return self._get_value('command.default.zero_items')

    @property
    def command_default_one_item(self):
        return self._get_value('command.default.one_item')

    @property
    def command_default_multi_items(self):
        return self._get_value('command.default.multi_items')

    @property
    def command_annotate_confirm(self):
        return self._get_value_boolean('command.annotate.confirm')
    
    @property
    def command_done_confirm(self):
        return self._get_value_boolean('command.done.confirm')
    
    @property
    def command_modify_confirm(self):
        return self._get_value_boolean('command.modify.confirm')
    
    @property
    def command_start_confirm(self):
        return self._get_value_boolean('command.start.confirm')
    
    @property
    def command_stop_confirm(self):
        return self._get_value_boolean('command.stop.confirm')

    @property
    def data_done_filename(self):
        return self._get_value('data.done.filename')

    @property
    def data_location(self):
        return self._get_value('data.location')

    @property
    def data_pending_filename(self):
        return self._get_value('data.pending.filename')
    
    def _get_value_boolean(self, key):
        if not self._config.has_option(self._category, key):
            raise Exception('Config element not found, category: [{}], key: [{}]'.format(self._category, key))
        return self._config[self._category].getboolean(key)
    
    def _get_value(self, key):
        if not self._config.has_option(self._category, key):
            message = 'Config element not found, category: [{}], key: [{}]'
            raise Exception(message.format(self._category, key))
        return self._config[self._category][key]

    def read(self, path):
        if not os.path.isfile(path):
            raise Exception("Config file does not exist: [{}]".format(path))

        try:
            self._config.read(path)
            self._logger.debug('Read config from file: [{}]'.format(path))
        except Exception as ex:
            raise Exception('Failed to read config from file: [{}]'.format(path)) from ex
