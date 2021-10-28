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
    def command_add_format(self) -> str:
        return self._get_value('command.add.format')

    @property
    def command_add_next_key_id(self) -> int:
        return self._get_value_integer('command.add.next_key_id')

    @command_add_next_key_id.setter
    def command_add_next_key_id(self, value: int):
        self._config[self._category]['command.add.next_key_id'] = str(value)

    @property
    def command_default(self) -> str:
        return self._get_value('command.default')

    @property
    def command_default_zero_items(self) -> str:
        return self._get_value('command.default.zero_items')

    @property
    def command_default_one_item(self) -> str:
        return self._get_value('command.default.one_item')

    @property
    def command_default_multi_items(self) -> str:
        return self._get_value('command.default.multi_items')

    @property
    def command_annotate_confirm(self) -> bool:
        return self._get_value_boolean('command.annotate.confirm')

    @property
    def command_done_confirm(self) -> bool:
        return self._get_value_boolean('command.done.confirm')

    @property
    def command_edit_editor(self) -> str:
        return self._get_value('command.edit.editor')

    @property
    def command_modify_confirm(self) -> bool:
        return self._get_value_boolean('command.modify.confirm')

    @property
    def command_start_confirm(self) -> bool:
        return self._get_value_boolean('command.start.confirm')

    @property
    def command_stop_confirm(self) -> bool:
        return self._get_value_boolean('command.stop.confirm')

    @property
    def data_done_filename(self) -> str:
        return self._get_value('data.done.filename')

    @property
    def data_location(self) -> str:
        return self._get_value('data.location')

    @property
    def data_pending_filename(self) -> str:
        return self._get_value('data.pending.filename')

    @property
    def report_list_columns(self) -> str:
        return self._get_value('report.list.columns')

    @property
    def table_column_separator(self) -> str:
        return self._get_value('table.column.separator').replace('"', '')

    @property
    def table_header_underline(self) -> bool:
        return self._get_value_boolean('table.header.underline')

    @property
    def table_row_alt_backcolour(self) -> str:
        return self._get_value('table.row.alt_backcolour')

    @property
    def table_row_alt_forecolour(self) -> str:
        return self._get_value('table.row.alt_forecolour')

    @property
    def table_row_backcolour(self) -> str:
        return self._get_value('table.row.backcolour')

    @property
    def table_row_forecolour(self) -> str:
        return self._get_value('table.row.forecolour')

    def _get_value_boolean(self, key: str) -> bool:
        if not self._config.has_option(self._category, key):
            message_format = 'Config element not found, category: [{}], key: [{}]'
            message = message_format.format(self._category, key)
            raise Exception(message)
        return self._config[self._category].getboolean(key)

    def _get_value_integer(self, key: str) -> int:
        if not self._config.has_option(self._category, key):
            message_format = 'Config element not found, category: [{}], key: [{}]'
            message = message_format.format(self._category, key)
            raise Exception(message)
        return self._config[self._category].getint(key)

    def _get_value(self, key: str) -> str:
        if not self._config.has_option(self._category, key):
            message = 'Config element not found, category: [{}], key: [{}]'
            raise Exception(message.format(self._category, key))
        return self._config[self._category][key]

    def read(self, path: str):
        if not os.path.isfile(path):
            raise Exception("Config file does not exist: [{}]".format(path))

        try:
            self._config.read(path)
            self._logger.debug('Read config from file: [%s]', path)
        except Exception as ex:
            raise Exception('Failed to read config from file: [{}]'.format(path)) from ex

    def save(self, path: str):
        try:
            with open(path, 'w') as config_file:
                self._config.write(config_file, space_around_delimiters=False)
            self._logger.debug('Wrote config to file: [%s]', path)
        except Exception as ex:
            raise Exception('Failed to write config to file: [{}]'.format(path)) from ex
