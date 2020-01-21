class TaskIndexFilter:
    def __init__(self, index):
        self._index = index
    
    @property
    def index(self):
        return self._index

    def is_match(self, task):
        return task.index == self._index