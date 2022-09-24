import filters.filterbase as filterbase

import typefactory


class FilterFactory(typefactory.TypeFactory):
    def __init__(self):
        super().__init__(filterbase.FilterParserBase)

    def parse(self, context, arg):
        task_filter = None
        for parser in sorted(self.types, key=lambda x: x.priority.value, reverse=True):
            task_filter = parser.parse(context, arg)
            if task_filter is not None:
                break

        if task_filter is None:
            raise Exception('Unknown filter: [{}]'.format(arg))

        return task_filter
