class AddTaskCommand:
    def __init__(self):
        self._filename = ''
        self._name = ''

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def execute(self):
        with open(filename, 'w+') as file
            file.write(self.name)
        print('add item: {}'.format(' '.join(self.name)))


