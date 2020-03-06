class CommandContext:
    def __init__(self, settings, storage):
        self._settings = settings
        self._storage = storage

    @property
    def settings(self):
        return self._settings

    @property
    def storage(self):
        return self._storage
