import logging
import entities
import filters.filterbase as filterbase


class TaskTagFilter(filterbase.FilterBase):
    def __init__(self, context, tag_name, tag_present):
        super().__init__(context)
        self._tag_name = tag_name
        self._tag_present = tag_present
        self._logger = logging.getLogger(__class__.__name__)
    
    @property
    def filter_group(self):
        return 'tags'

    @property
    def tag_name(self):
        return self._tag_name

    @property
    def tag_present(self):
        return self._tag_present

    def is_match(self, task):
        if self.tag_name in task.tags:
            if self.tag_present:
                result = True 
                reason = 'tag exists and should'
            else:
                result = False
                reason = 'tag exists and should not'
        else:
            if self.tag_present:
                result = False 
                reason = 'tag does not exist and should'
            else:
                result = True
                reason = 'tag does not exist and should not'

        self._logger.debug('is_match: {}, reason: {}, task: [{}]'.format(result, reason, task))
        return result
    
    def __str__(self):
        if self.tag_present:
            prefix = '+'
        else:
            prefix = '-'
        return 'TaskTagFilter({}{})'.format(prefix, self.tag_name)


class TaskTagFilterParser(filterbase.FilterParserBase):
    def __init__(self):
        super().__init__(filterbase.FilterParserPriority.MEDIUM)

    def parse(self, context, arg):
        if arg[0] == '+':
            tag_name = arg[1:]
            task_filter = TaskTagFilter(context, tag_name, True)
        elif arg[0] == '-':
            tag_name = arg[1:]
            task_filter = TaskTagFilter(context, tag_name, False)
        else:
            task_filter = None
        return task_filter
