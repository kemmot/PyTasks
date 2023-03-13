import logging
import entities
import filters.filterbase as filterbase


class TaskAttributeFilter(filterbase.FilterBase):
    def __init__(self, context, attribute_name, attribute_value):
        super().__init__(context)
        self._attribute_name = attribute_name
        self._attribute_value = attribute_value
        self._logger = logging.getLogger(__class__.__name__)

    @property
    def attribute_name(self):
        return self._attribute_name

    @property
    def attribute_value(self):
        return self._attribute_value
    
    @property
    def filter_group(self):
        return self.attribute_name

    def is_match(self, task):
        retriever = entities.TaskAttributeRetriever()
        value = retriever.get_value(task, self.attribute_name)
        task_has_attribute = value != '' and value != None
        if self.attribute_value == '':
            if task_has_attribute:
                result = False 
                reason = 'attribute exists when filter requested it not to value'
            else:
                result = True
                reason = 'attribute does not exist as searched for'
        elif task_has_attribute:
            if value.startswith(self.attribute_value):
                result = True
                reason = 'attribute value matches'
            else:
                result = False
                reason = 'attribute value does not match'
        else:
            result = False
            reason = 'attribute does not exist'

        self._logger.debug('is_match: {}, reason: {}, task: [{}]'.format(result, reason, task))
        return result
    
    def __str__(self):
        return 'TaskAttributeFilter({}:{})'.format(self.attribute_name, self.attribute_value)


class TaskAttributeFilterParser(filterbase.FilterParserBase):
    def __init__(self):
        super().__init__(filterbase.FilterParserPriority.MEDIUM)

    def parse(self, context, arg):
        if arg and ':' in arg:
            attribute_parts = arg.split(':')
            attribute_name = attribute_parts[0]
            attribute_value = attribute_parts[1]
            task_filter = TaskAttributeFilter(context, attribute_name, attribute_value)
        else:
            task_filter = None
        return task_filter
