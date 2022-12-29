import commands.commandbase as commandbase


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
        return tasks

    def sort_tasks(self, tasks):
        return tasks


class ReportCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'report'

    def __init__(self, report_config=None):
        if report_config:
            super().__init__(report_config.name)
        else:
            super().__init__(ReportCommandParser.COMMAND_NAME)
        self.__report_config = report_config

    def parse(self, context, args):
        return ReportCommand(context, self.__report_config)
