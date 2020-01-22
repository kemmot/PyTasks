class TypeFactory:
    def __init__(self, base_class):
        self._types = []
        self._base_class = base_class
    
    @property
    def types(self):
        return self._types

    def register_known_types(self):
        for cla in self._base_class.__subclasses__():
            self.register_type(cla())

    def register_type(self, cla):
        self._types.append(cla)
