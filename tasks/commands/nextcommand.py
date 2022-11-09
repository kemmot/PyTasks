import functools

import commands.commandbase as commandbase


class NextTaskCommand(commandbase.ReportCommandBase):
    '''
    A command that will list tasks.
    '''
    def __init__(self, context, command_filter=None):
        super().__init__(context, command_filter)
    
    def get_annotation_count(self):
        return self.context.settings.report_next_max_annotation_count

    def get_columns(self):
        return self.context.settings.report_next_columns.split(',')
    
    def filter_tasks(self, tasks):
        return [t for t in tasks if not t.is_ended and not t.is_waiting]
    
    def sort_tasks(self, tasks):
        task_sort_by_key = functools.cmp_to_key(NextTaskCommand.__task_sort)
        tasks.sort(key=task_sort_by_key)

    def __task_sort(a, b):
        result = NextTaskCommand.__task_sort_by_started(a, b)
        if result == 0:
            result = NextTaskCommand.__task_sort_by_blocked(a, b)
        if result == 0:
            result = NextTaskCommand.__task_sort_by_due(a, b)
        if result == 0:
            result = NextTaskCommand.__task_sort_by_priority(a, b)
        return result
    
    def __task_sort_by_blocked(a, b):
        if a.is_blocked:
            if b.is_blocked:
                result = 0
            else:
                result = -1
        elif b.is_blocked:
            result = 1
        else:
            result = 0
        return result * -1
    
    def __task_sort_by_started(a, b):
        if a.is_started:
            if b.is_started:
                result = 0
            else:
                result = -1
        elif b.is_started:
            result = 1
        else:
            result = 0
        return result
    
    def __task_sort_by_due(a, b):
        key = 'due'
        if key in a.attributes:
            if key in b.attributes:
                a_value = a.attributes[key]
                b_value = b.attributes[key]
                if a_value < b_value:
                    result = -1
                elif a_value > b_value:
                    result = 1
                else:
                    result = 0
            else:
                result = -1
        elif key in b.attributes:
            result = 1
        else:
            result = 0
        return result
    
    def __task_sort_by_priority(a, b):
        key = 'priority'
        if key in a.attributes:
            if key in b.attributes:
                a_value = NextTaskCommand.__convert_priority_letter_to_number(a.attributes[key])
                b_value = NextTaskCommand.__convert_priority_letter_to_number(b.attributes[key])
                if a_value < b_value:
                    result = 1
                elif a_value > b_value:
                    result = -1
                else:
                    result = 0
            else:
                result = -1
        elif key in b.attributes:
            result = 1
        else:
            result = 0
        return result
    
    def __convert_priority_letter_to_number(letter):
        if letter == 'H':
            value = 3
        elif letter == 'M':
            value = 2
        else:
            value = 1
        return value


class NextTaskCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'next'

    def __init__(self):
        super().__init__(NextTaskCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return NextTaskCommand(context)
