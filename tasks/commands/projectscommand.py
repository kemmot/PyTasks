import commands.commandbase as commandbase

import asciitable
import console


class ProjectsCommand(commandbase.FilterCommandBase):
    '''
    A command that will list projects.
    '''
    def __init__(self, context, command_filter=None):
        super().__init__(context, command_filter)
    
    def execute_tasks(self, tasks):
        '''
        Executes the logic of this command.
        '''
        project_counts = {}
        for task in tasks:
            if 'project' in task.attributes:
                project = task.attributes['project']
            else:
                project = '(none)'
            project_path = ''
            for project_part in project.split('.'):
                if project_path:
                    project_path += '.'
                project_path += project_part
                if project_path in project_counts:
                    count = project_counts[project_path] + 1
                else:
                    count = 1
                project_counts[project_path] = count
        
        table = asciitable.DataTable()
        table.add_column('Project')
        table.add_column('Tasks')
        for project in sorted(project_counts.keys()):
            project_parts = project.split('.')
            sub_project = '  ' * (len(project_parts) - 1)
            sub_project += project_parts[-1]
            table.add_row(sub_project, str(project_counts[project]))
        self.print_table(table)

    def print_table(self, table):
        c = console.ConsoleFactory().get_console()
        c.foreground_colour = self.context.settings.table_row_forecolour
        c.background_colour = self.context.settings.table_row_backcolour
        c.print_table(table, self.context.settings.table_row_alt_forecolour, self.context.settings.table_row_alt_backcolour)


class ProjectsCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'projects'

    def __init__(self):
        super().__init__(ProjectsCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return ProjectsCommand(context)
