import logging


class TypeFactory:
    def __init__(self, base_class, register_name_property=''):
        self._types = {}
        self._base_class = base_class
        self._register_name_property = register_name_property
        self._logger = logging.getLogger(__class__.__name__)

    @property
    def types(self):
        return self._types

    def register_known_types(self):
        self._register_known_types(self._base_class)

    def _register_known_types(self, specific_base_class):
        for cla in specific_base_class.__subclasses__():
            if cla.__subclasses__():
                self._register_known_types(cla)
            else:
                try:
                    object = cla()
                    if self._register_name_property and hasattr(object, self._register_name_property):
                        register_name = getattr(object, self._register_name_property)
                    else:
                        register_name = cla.__name__,
                    self.register_type(register_name, object)
                except Exception as ex:
                    raise Exception('Failed registering type {}'.format(cla)) from ex

    def register_type(self, name, cla):
        self._types[name] = cla
        self._logger.debug('Type [%s] registered: [%s]', name, str(cla))
