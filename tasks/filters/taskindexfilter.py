class TaskIndexFilter:
    def __init__(self, index):
        self._index = index

    def is_match(self, task):
        return task.index == self._index