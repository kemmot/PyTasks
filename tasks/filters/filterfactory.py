import filters.alwaysfilter as alwaysfilter
import filters.filterbase as filterbase

import typefactory


class FilterFactory(typefactory.TypeFactory):
    def __init__(self):
        super().__init__(filterbase.FilterParserBase)

    def parse(self, arg):
        filter = None
        for parser in self.types:
            filter = parser.parse(arg)
            if filter is not None:
                break

        if filter is None:
            raise Exception('Unknown filter: [{}]'.format(arg))

        return filter
