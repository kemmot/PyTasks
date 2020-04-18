class CommandContext:
    def __init__(self, settings, storage, filter_factory):
        self._settings = settings
        self._storage = storage
        self._filter_factory = filter_factory

    @property
    def filter_factory(self):
        return self._filter_factory

    @property
    def settings(self):
        return self._settings

    @property
    def storage(self):
        return self._storage
