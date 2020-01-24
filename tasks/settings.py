import configparser
import logging
import os


class Settings:
    def __init__(self, config=None):
        self._category = 'general'
        if config == None:
            config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self._config = config
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def data_location(self):
        key = 'data.location'
        if not self._config.has_option(self._category, key):
            raise Exception('Config element not found, category: [{}], key: [{}]'.format(self._category, key))
        return self._config[self._category][key]
    
    @property
    def data_pending_filename(self):
        key = 'data.pending.filename'
        if not self._config.has_option(self._category, key):
            raise Exception('Config element not found, category: [{}], key: [{}]'.format(self._category, key))
        return self._config[self._category][key]

    def read(self, path):
        if (not os.path.isfile(path)):
            raise Exception("Config file does not exist: [{}]".format(path))

        try:
            self._config.read(path)
            self._logger.debug('Read config from file: [{}]'.format(path))
        except Exception as ex:
            raise Exception('Failed to read config from file: [{}]'.format(path)) from ex