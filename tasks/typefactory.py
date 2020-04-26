class TypeFactory:
    def __init__(self, base_class):
        self._types = []
        self._base_class = base_class

    @property
    def types(self):
        return self._types

    def register_known_types(self):
        self._register_known_types(self._base_class)

    def _register_known_types(self, specific_base_class):
        for cla in specific_base_class.__subclasses__():
            if len(cla.__subclasses__()) > 0:
                self._register_known_types(cla)
            else:
                try:
                    self.register_type(cla())
                except Exception as ex:
                    raise Exception('Failed registering type {}'.format(cla)) from ex

    def register_type(self, cla):
        self._types.append(cla)
