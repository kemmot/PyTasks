import asciitable


class CommandContext:
    def __init__(self, settings, storage, filter_factory, console):
        self._settings = settings
        self._storage = storage
        self._filter_factory = filter_factory
        self._console = console
        self._command_factory = None

    @property
    def command_factory(self):
        return self._command_factory

    @command_factory.setter
    def command_factory(self, value):
        self._command_factory = value

    @property
    def console(self):
        return self._console

    @property
    def filter_factory(self):
        return self._filter_factory

    @property
    def settings(self):
        return self._settings

    @property
    def storage(self):
        return self._storage

    def create_table(self):
        table = asciitable.AsciiTable()
        table.column_separator = self._settings.table_column_separator
        table.add_header_underline = self._settings.table_header_underline
        return table
