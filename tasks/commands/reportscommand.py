import functools

import commands.commandbase as commandbase
import entities as entities
import filters.allbatchfilter as allbatchfilter


class ReportCommand(commandbase.ReportCommandBase):
    '''
    A command that will run a config driven report.
    '''

    def __init__(self, context, report_config, command_filter=None):
        super().__init__(context, command_filter)
        self.__report_config = report_config
    
    def get_annotation_count(self):
        return self.__report_config.max_annotation_count

    def get_columns(self):
        return self.__report_config.columns.split(',')

    def filter_tasks(self, tasks):
        batch_filter = self.__get_filters()
        return self.apply_filter(tasks, batch_filter)
    
    def __get_filters(self):
        self._logger.debug('Getting filters for report: {}, filter: {}'.format(self.__report_config.name, self.__report_config.filter))
        filter_parts = self.__report_config.filter.split(' ')
        batch_filter = allbatchfilter.AllBatchFilter(self.context)
        for filter_part in filter_parts:
            filter = self.context.filter_factory.parse(self.context, filter_part)
            self._logger.debug('Parsed report filter: {}'.format(filter))
            batch_filter.add_filter(filter)
        return batch_filter

    def sort_tasks(self, tasks):
        self._logger.debug('Getting sort for report: {}, sort: {}'.format(self.__report_config.name, self.__report_config.sort))
        self.__sort_fields = self.__report_config.sort.split(',')
        self.__retriever = entities.TaskAttributeRetriever()
        task_sort_by_key = functools.cmp_to_key(self.__task_sort)
        tasks.sort(key=task_sort_by_key)

    def __task_sort(self, a, b):
        result = 0
        for sort_field in self.__sort_fields:
            if sort_field[-1] == '-':
                sort_ascending = False
                sort_field = sort_field[0:-1]
            elif sort_field[-1] == '+':
                sort_ascending = True
                sort_field = sort_field[0:-1]
            else:
                sort_ascending = True

            if result == 0:
                result = self.__task_sort_by_field(a, b, sort_field, sort_ascending)
        return result

    def __task_sort_by_field(self, a, b, sort_field, sort_ascending):
        a_value = self.__retriever.get_value(a, sort_field)
        b_value = self.__retriever.get_value(b, sort_field)
        a_has_attribute = a_value != '' and a_value != None
        b_has_attribute = b_value != '' and b_value != None
        if a_has_attribute:
            if b_has_attribute:
                if sort_field == 'priority':
                    a_value = self.__convert_priority_letter_to_number(a_value)
                    b_value = self.__convert_priority_letter_to_number(b_value)
                
                if a_value < b_value:
                    result = -1
                elif a_value > b_value:
                    result = 1
                else:
                    result = 0
                
                if not sort_ascending:
                    result *= -1
            else:
                result = -1
        else:
            if b_has_attribute:
                result = 1
            else:
                result = 0
        #print('id:{}:{}, result: {}, value:{}:{}, field: {}, asc: {}'.format(a.index, b.index, result, a_value, b_value, sort_field, sort_ascending))
        return result
    
    def __convert_priority_letter_to_number(self, letter):
        if letter == 'H':
            value = 3
        elif letter == 'M':
            value = 2
        else:
            value = 1
        return value


class ReportsCommand(commandbase.CommandBase):
    def execute(self):
        for report in self.context.settings.get_reports():
            self.context.console.print('{}'.format(report.name))


class ReportsCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'reports'

    def __init__(self, report_config=None):
        if report_config:
            super().__init__(report_config.name)
        else:
            super().__init__(ReportsCommandParser.COMMAND_NAME)
        self.__report_config = report_config

    @property
    def report_config(self):
        return self.__report_config

    def parse(self, context, args):
        if self.__report_config:
            return ReportCommand(context, self.__report_config)
        return ReportsCommand(context)
