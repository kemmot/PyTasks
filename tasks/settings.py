import configparser
import logging
import os


class SettingNames:
	command_add_format = 'command.add.format'
	command_add_next_key_id = 'command.add.next_key_id'
	command_add_next_key_id = 'command.add.next_key_id'
	command_default = 'command.default'
	command_default_zero_items = 'command.default.zero_items'
	command_default_one_item = 'command.default.one_item'
	command_default_multi_items = 'command.default.multi_items'
	command_annotate_confirm = 'command.annotate.confirm'
	command_done_confirm = 'command.done.confirm'
	command_modify_confirm = 'command.modify.confirm'
	command_start_confirm = 'command.start.confirm'
	command_stop_confirm = 'command.stop.confirm'
	data_done_filename = 'data.done.filename'
	data_location = 'data.location'
	data_pending_filename = 'data.pending.filename'
	report_list_columns = 'report.list.columns'
	report_next_columns = 'report.next.columns'
	table_column_separator = 'table.column.separator'
	table_header_underline = 'table.header.underline'
	table_row_alt_backcolour = 'table.row.alt_backcolour'
	table_row_alt_forecolour = 'table.row.alt_forecolour'
	table_row_backcolour = 'table.row.backcolour'
	table_row_forecolour = 'table.row.forecolour'


class SettingsFacade:
	def __init__(self, settings_provider):
		self.__settings_provider = settings_provider

	@property
	def command_add_format(self):
		return self.__settings_provider.get_value(SettingNames.command_add_format)

	@property
	def command_add_next_key_id(self):
		return self.__settings_provider.get_value_integer(SettingNames.command_add_next_key_id)

	@command_add_next_key_id.setter
	def command_add_next_key_id(self, value):
		self.__settings_provider.set_value(SettingNames.command_add_next_key_id, value)

	@property
	def command_default(self):
		return self.__settings_provider.get_value(SettingNames.command_default)

	@property
	def command_default_zero_items(self):
		return self.__settings_provider.get_value(SettingNames.command_default_zero_items)

	@property
	def command_default_one_item(self):
		return self.__settings_provider.get_value(SettingNames.command_default_one_item)

	@property
	def command_default_multi_items(self):
		return self.__settings_provider.get_value(SettingNames.command_default_multi_items)

	@property
	def command_annotate_confirm(self):
		return self.__settings_provider.get_value_boolean(SettingNames.command_annotate_confirm)
    @property
    def command_edit_editor(self):
        return self._get_value('command.edit.editor')

    @property
    def command_modify_confirm(self):
        return self._get_value_boolean('command.modify.confirm')

	@property
	def command_done_confirm(self):
		return self.__settings_provider.get_value_boolean(SettingNames.command_done_confirm)

	@property
	def command_modify_confirm(self):
		return self.__settings_provider.get_value_boolean(SettingNames.command_modify_confirm)

	@property
	def command_start_confirm(self):
		return self.__settings_provider.get_value_boolean(SettingNames.command_start_confirm)

	@property
	def command_stop_confirm(self):
		return self.__settings_provider.get_value_boolean(SettingNames.command_stop_confirm)

	@property
	def data_done_filename(self):
		return self.__settings_provider.get_value(SettingNames.data_done_filename)

	@property
	def data_location(self):
		return self.__settings_provider.get_value(SettingNames.data_location)

	@property
	def data_pending_filename(self):
		return self.__settings_provider.get_value(SettingNames.data_pending_filename)

	@property
	def report_list_columns(self):
		return self.__settings_provider.get_value(SettingNames.report_list_columns)

	@property
	def report_next_columns(self):
		return self.__settings_provider.get_value(SettingNames.report_next_columns)

	@property
	def table_column_separator(self):
		return self.__settings_provider.get_value(SettingNames.table_column_separator).replace('"', '')

	@property
	def table_header_underline(self):
		return self.__settings_provider.get_value_boolean(SettingNames.table_header_underline)

	@property
	def table_row_alt_backcolour(self):
		return self.__settings_provider.get_value(SettingNames.table_row_alt_backcolour)

	@property
	def table_row_alt_forecolour(self):
		return self.__settings_provider.get_value(SettingNames.table_row_alt_forecolour)

	@property
	def table_row_backcolour(self):
		return self.__settings_provider.get_value(SettingNames.table_row_backcolour)

	@property
	def table_row_forecolour(self):
		return self.__settings_provider.get_value(SettingNames.table_row_forecolour)

	def read(self):
		self.__settings_provider.read()

	def save_if_needed(self):
		self.__settings_provider.save_if_needed()


class SettingsProviderConfigurator:
	def get_settings_provider(self, user_path, program_path):
		defaults = DefaultSettingsProvider()
		user = IniSettingsProvider(user_path)
		program = IniSettingsProvider(program_path)
		return SettingsFacade(LayeredSettingsProvider([user, program, defaults]))


class SettingsProviderBase:
	def __init__(self):
		self._logger = logging.getLogger(self.__class__.__name__)

	def get_value(self, key):
		raise Exception(f'get_value not implemented in {__class__.__name__}')

	def get_value_boolean(self, key):
		return bool(self.get_value(key))

	def get_value_integer(self, key):
		return int(self.get_value(key))

	def has_value(self, key):
		raise Exception(f'has_value not implemented in {__class__.__name__}')

	def is_writable(self):
		return False

	def read(self):
		raise Exception(f'read not implemented in {__class__.__name__}')

	def save_if_needed(self):
		raise Exception(f'save_if_needed not implemented in {__class__.__name__}')

	def save_value(self, key, value):
		raise Exception(f'save_value not implemented in {__class__.__name__}')


class DefaultSettingsProvider(SettingsProviderBase):
	@property
	def get_value(self, key):
		if key == SettingNames.command_add_format:
			return '{name}'
		elif key == SettingNames.command_add_next_key_id:
			return '1'
		elif key == SettingNames.command_annotate_confirm:
			return 'True'
		elif key == SettingNames.command_default:
			return '{name}'
		elif key == SettingNames.command_default_zero_items:
			return 'help'
		elif key == SettingNames.command_default_one_item:
			return 'info'
		elif key == SettingNames.command_default_multi_items:
			return 'next'
		elif key == SettingNames.command_done_confirm:
			return 'True'
		elif key == SettingNames.command_modify_confirm:
			return 'True'
		elif key == SettingNames.command_start_confirm:
			return 'True'
		elif key == SettingNames.command_stop_confirm:
			return 'True'
		elif key == SettingNames.data_done_filename:
			return 'completed.data'
		elif key == SettingNames.data_location:
			return '~\.task'
		elif key == SettingNames.data_pending_filename:
			return 'pending.data'
		elif key == SettingNames.report_list_columns:
			return 'id,status,project,priority,description'
		elif key == SettingNames.report_next_columns:
			return 'id,status,project,priority,description'
		elif key == SettingNames.table_column_separator:
			return ' | '
		elif key == SettingNames.table_header_underline:
			return 'True'
		elif key == SettingNames.table_row_alt_backcolour:
			return 'blue'
		elif key == SettingNames.table_row_alt_forecolour:
			return 'white'
		elif key == SettingNames.table_row_backcolour:
			return 'black'
		elif key == SettingNames.table_row_forecolour:
			return 'white'
		else:
			raise Exception(f'Default value not found for setting: [{key}]')
	
	def has_value(self, key):
		try:
			self.get_value(key)
			return True
		except Exception:
			return False

	def read(self):
		pass

	def save_if_needed(self):
		pass


class LayeredSettingsProvider(SettingsProviderBase):
	def __init__(self, settings_provider_list):
		super().__init__()
		self.__settings_provider_list = settings_provider_list

	def get_value(self, key):
		for setting_provider in self.__settings_provider_list:
			if setting_provider.has_value(key):
				return setting_provider.get_value(key)
		raise Exception(f'Value not found for setting: [{key}]')
	
	def has_value(self, key):
		for setting_provider in self.__settings_provider_list:
			if setting_provider.has_value(key):
				return True
		return False

	def read(self):
		for setting_provider in self.__settings_provider_list:
			setting_provider.read()

	def save_if_needed(self):
		for setting_provider in self.__settings_provider_list:
			setting_provider.save_if_needed()
		
	def set_value(self, key, value):
		for setting_provider in self.__settings_provider_list:
			if setting_provider.is_writable():
				setting_provider.set_value(key, value)


class IniSettingsProvider(SettingsProviderBase):
	def __init__(self, path, config=None):
		super().__init__()
		self.__category = 'general'
		self.__path = path
		if config is None:
			config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
		self.__config = config
		self.__is_dirty = False
	
	def has_value(self, key):
		return self.__config.has_option(self.__category, key)
	
	def is_writable(self):
		return True

	def set_value(self, key, value):
		self.__config[self.__category][key] = str(value)
		self.__is_dirty = True

	def get_value_boolean(self, key):
		if not self.__config.has_option(self.__category, key):
			message_format = 'Config element not found, category: [{}], key: [{}]'
			message = message_format.format(self.__category, key)
			raise Exception(message)
		return self.__config[self.__category].getboolean(key)

	def get_value_integer(self, key):
		if not self.__config.has_option(self.__category, key):
			message_format = 'Config element not found, category: [{}], key: [{}]'
			message = message_format.format(self.__category, key)
			raise Exception(message)
		return self.__config[self.__category].getint(key)

	def get_value(self, key):
		if not self.__config.has_option(self.__category, key):
			message = 'Config element not found, category: [{}], key: [{}]'
			raise Exception(message.format(self.__category, key))
		return self.__config[self.__category][key]

	def read(self):
		if not os.path.isfile(self.__path):
			self._logger.debug('Config file does not exist: [%s]', self.__path)
			self.__is_dirty = True
		else:
			try:
				self.__config.read(self.__path)
				self.__is_dirty = False
				self._logger.debug('Read config from file: [%s]', self.__path)
			except Exception as ex:
				raise Exception('Failed to read config from file: [{}]'.format(self.__path)) from ex

	def save_if_needed(self):
		if self.__is_dirty:
			self.__save()

	def __save(self):
		try:
			with open(self.__path, 'w') as config_file:
				self.__config.write(config_file, space_around_delimiters=False)
			self._logger.debug('Wrote config to file: [%s]', self.__path)
		except Exception as ex:
			raise Exception('Failed to write config to file: [{}]'.format(self.__path)) from ex
