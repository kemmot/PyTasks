class CommandContext:
    def __init__(self, settings, storage, filter_factory):
        self._settings = settings
        self._storage = storage
        self._filter_factory = filter_factory
        self._command_factory = None
    
    @property
    def command_factory(self):
        return self._command_factory
    
    @command_factory.setter
    def command_factory(self, value):
        self._command_factory = value

    @property
    def filter_factory(self):
        return self._filter_factory

    @property
    def settings(self):
        return self._settings

    @property
    def storage(self):
        return self._storage
