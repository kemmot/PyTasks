import configparser
import logging
import os


class SettingException(Exception):
	def __init__(self, message='',):
		Exception.__init__(self, message)


class SettingNames:
	command_add_format = 'command.add.format'
	command_add_next_key_id = 'command.add.next_key_id'
	command_add_next_key_id = 'command.add.next_key_id'
	command_annotate_confirm = 'command.annotate.confirm'
	command_context_define_confirm = 'command.context.define.confirm'
	command_context_delete_confirm = 'command.context.delete.confirm'
	command_default = 'command.default'
	command_default_zero_items = 'command.default.zero_items'
	command_default_one_item = 'command.default.one_item'
	command_default_multi_items = 'command.default.multi_items'
	command_done_confirm = 'command.done.confirm'
	command_edit_editor = 'command.edit.editor'
	command_modify_confirm = 'command.modify.confirm'
	command_modify_summary = 'command.modify.summary'
	command_start_confirm = 'command.start.confirm'
	command_stop_confirm = 'command.stop.confirm'
	command_undo_confirm = 'command.undo.confirm'
	context = 'context'
	data_done_filename = 'data.done.filename'
	data_location = 'data.location'
	data_pending_filename = 'data.pending.filename'
	data_undo_filename = 'data.undo.filename'
	filter_attribute_case_sensitive = 'filter.attribute.case_sensitive'
	report_list_columns = 'report.list.columns'
	report_list_max_annotation_count = 'report.list.max_annotation_count'
	report_next_columns = 'report.next.columns'
	report_next_max_annotation_count = 'report.next.max_annotation_count'
	table_column_separator = 'table.column.separator'
	table_header_underline = 'table.header.underline'
	table_row_alt_backcolour = 'table.row.alt_backcolour'
	table_row_alt_forecolour = 'table.row.alt_forecolour'
	table_row_backcolour = 'table.row.backcolour'
	table_row_forecolour = 'table.row.forecolour'


class ReportSettings:
	def __init__(self):
		self.__columns = ''
		self.__filter = ''
		self.__max_annotation_count = 0
		self.__name = ''
		self.__sort = ''

	@property
	def columns(self):
		return self.__columns

	@columns.setter
	def columns(self, value):
		self.__columns = value

	@property
	def filter(self):
		return self.__filter

	@filter.setter
	def filter(self, value):
		self.__filter = value

	@property
	def max_annotation_count(self):
		return self.__max_annotation_count

	@max_annotation_count.setter
	def max_annotation_count(self, value):
		self.__max_annotation_count = value

	@property
	def name(self):
		return self.__name

	@name.setter
	def name(self, value):
		self.__name = value

	@property
	def sort(self):
		return self.__sort

	@sort.setter
	def sort(self, value):
		self.__sort = value


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
	def command_context_define_confirm(self):
		return self.__settings_provider.get_value_boolean(SettingNames.command_context_define_confirm)

	@property
	def command_context_delete_confirm(self):
		return self.__settings_provider.get_value_boolean(SettingNames.command_context_delete_confirm)

	@property
	def command_done_confirm(self):
		return self.__settings_provider.get_value_boolean(SettingNames.command_done_confirm)

	@property
	def command_edit_editor(self):
		return self.__settings_provider.get_value(SettingNames.command_edit_editor)

	@property
	def command_modify_confirm(self):
		return self.__settings_provider.get_value_boolean(SettingNames.command_modify_confirm)

	@property
	def command_modify_summary(self):
		return self.__settings_provider.get_value_boolean(SettingNames.command_modify_summary)

	@property
	def command_start_confirm(self):
		return self.__settings_provider.get_value_boolean(SettingNames.command_start_confirm)

	@property
	def command_stop_confirm(self):
		return self.__settings_provider.get_value_boolean(SettingNames.command_stop_confirm)

	@property
	def command_undo_confirm(self):
		return self.__settings_provider.get_value_boolean(SettingNames.command_undo_confirm)

	@property
	def context(self):
		return self.__settings_provider.get_value(SettingNames.context)

	@context.setter
	def context(self, value):
		self.__settings_provider.set_value(SettingNames.context, value)

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
	def data_undo_filename(self):
		return self.__settings_provider.get_value(SettingNames.data_undo_filename)

	@property
	def filter_attribute_case_sensitive(self):
		return self.__settings_provider.get_value_boolean(SettingNames.filter_attribute_case_sensitive)

	@property
	def report_list_columns(self):
		return self.__settings_provider.get_value(SettingNames.report_list_columns)

	@property
	def report_list_max_annotation_count(self):
		return self.__settings_provider.get_value_integer(SettingNames.report_list_max_annotation_count)

	@property
	def report_next_columns(self):
		return self.__settings_provider.get_value(SettingNames.report_next_columns)

	@property
	def report_next_max_annotation_count(self):
		return self.__settings_provider.get_value_integer(SettingNames.report_next_max_annotation_count)

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

	def create_context(self, name, definition):
		setting_name = self.__get_context_setting_name(name)
		self.__settings_provider.set_value(setting_name, definition)

	def delete_context(self, name):
		setting_name = self.__get_context_setting_name(name)
		self.__settings_provider.remove_value(setting_name)

	def __get_context_setting_name(self, context_name):
		return 'context.{}'.format(context_name)

	def get_active_context(self):
		for context_name,definition,is_active in self.get_contexts():
			if is_active:
				return context_name,definition
		return None,None

	def get_contexts(self):
		active_context = self.context
		contexts = []
		for key in sorted(self.__settings_provider.get_keys()):
			if key.startswith('context.'):
				context_name = key.split('.')[1]
				definition = self.__settings_provider.get_value(key)
				is_active = context_name == active_context
				contexts.append([context_name, definition, is_active])
		return contexts

	def get_reports(self):
		reports = {}
		for key in sorted(self.__settings_provider.get_keys()):
			if key.startswith('report.'):
				config_parts = key.split('.')
				if len(config_parts) < 3:
					raise Exception('Invalid report config: {}'.format(key))

				report_name = config_parts[1]
				if report_name in reports:
					report = reports[report_name]
				else:
					report = ReportSettings()
					report.name = report_name
					reports[report_name] = report

				value = self.__settings_provider.get_value(key)
				if config_parts[2] == 'columns':
					report.columns = value
				elif config_parts[2] == 'filter':
					report.filter = value
				elif config_parts[2] == 'max_annotation_count':
					report.max_annotation_count = int(value)
				elif config_parts[2] == 'sort':
					report.sort = value

		return reports.values()

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

	def get_keys(self):
		return []

	def get_value(self, key):
		raise Exception(f'get_value not implemented in {__class__.__name__}')

	def get_value_boolean(self, key):
		value = self.get_value(key).upper()
		if value in ['TRUE', 'YES']:
			return True
		elif value in ['FALSE', 'NO']:
			return False
		else:
			raise Exception('Could not parse value as boolean: [{}]'.format(value))

	def get_value_integer(self, key):
		return int(self.get_value(key))

	def has_value(self, key):
		raise Exception(f'has_value not implemented in {__class__.__name__}')

	def is_writable(self):
		return False

	def read(self):
		raise Exception(f'read not implemented in {__class__.__name__}')

	def remove_value(self, key):
		pass

	def save_if_needed(self):
		raise Exception(f'save_if_needed not implemented in {__class__.__name__}')

	def save_value(self, key, value):
		raise Exception(f'save_value not implemented in {__class__.__name__}')


class DefaultSettingsProvider(SettingsProviderBase):
	def get_value(self, key):
		if key == SettingNames.command_add_format:
			return '{name}'
		elif key == SettingNames.command_add_next_key_id:
			return '1'
		elif key == SettingNames.command_annotate_confirm:
			return 'True'
		elif key == SettingNames.command_context_define_confirm:
			return 'True'
		elif key == SettingNames.command_context_delete_confirm:
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
		elif key == SettingNames.command_edit_editor:
			return 'vim'
		elif key == SettingNames.command_modify_confirm:
			return 'True'
		elif key == SettingNames.command_modify_summary:
			return 'True'
		elif key == SettingNames.command_start_confirm:
			return 'True'
		elif key == SettingNames.command_stop_confirm:
			return 'True'
		elif key == SettingNames.command_undo_confirm:
			return 'True'
		elif key == SettingNames.context:
			return 'none'
		elif key == SettingNames.data_done_filename:
			return 'completed.data'
		elif key == SettingNames.data_location:
			return '~\.task'
		elif key == SettingNames.data_pending_filename:
			return 'pending.data'
		elif key == SettingNames.data_undo_filename:
			return 'undo.data'
		elif key == SettingNames.filter_attribute_case_sensitive:
			return 'True'
		elif key == SettingNames.report_list_columns:
			return 'id,status,project,priority,description'
		elif key == SettingNames.report_list_max_annotation_count:
			return '3'
		elif key == SettingNames.report_next_columns:
			return 'id,status,project,priority,description'
		elif key == SettingNames.report_next_max_annotation_count:
			return '3'
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
			raise SettingException(f'Default value not found for setting: [{key}]')
	
	def has_value(self, key):
		try:
			self.get_value(key)
			return True
		except SettingException as ex:
			return False

	def read(self):
		pass

	def save_if_needed(self):
		pass


class LayeredSettingsProvider(SettingsProviderBase):
	def __init__(self, settings_provider_list):
		super().__init__()
		self.__settings_provider_list = settings_provider_list

	def get_keys(self):
		keys = []
		for setting_provider in self.__settings_provider_list:
			for key in setting_provider.get_keys():
				if not key in keys:
					keys.append(key)
		return keys

	def get_value(self, key):
		for setting_provider in self.__settings_provider_list:
			has_value = setting_provider.has_value(key)
			if has_value:
				value = setting_provider.get_value(key)
			else:
				value = ''
			self._logger.debug(f'Provider [{setting_provider}], setting [{key}], found: {has_value}, value: {value}')
			if has_value:
				return value
		raise Exception(f'Value not found for setting: [{key}]')
	
	def has_value(self, key):
		for setting_provider in self.__settings_provider_list:
			if setting_provider.has_value(key):
				return True
		return False

	def read(self):
		for setting_provider in self.__settings_provider_list:
			setting_provider.read()

	def remove_value(self, key):
		for setting_provider in self.__settings_provider_list:
			setting_provider.remove_value(key)

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

	def get_keys(self):
		return self.__config[self.__category].keys()

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

	def remove_value(self, key):
		self.__config.remove_option(self.__category, key)
		self.__is_dirty = True

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
	
	def __str__(self):
		return '{}({})'.format(self.__class__.__name__, self.__path)
