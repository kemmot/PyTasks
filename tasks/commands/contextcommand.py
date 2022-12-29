import asciitable
import commands.commandbase as commandbase
import filters.confirmfilter as confirmfilter
import console


class ActivateContextCommand(commandbase.CommandBase):
    '''
    A command that will activate a context.
    '''

    def __init__(self, context):
        super().__init__(context)
        self._context_name = ''

    @property
    def context_name(self):
        return self._context_name

    @context_name.setter
    def context_name(self, value):
        self._context_name = value

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        self.context.settings.context = self.context_name
        self.context.console.print('Context ''{}'' set. Use ''task context none'' to remove'.format(self.context_name))


class DeactivateContextCommand(commandbase.CommandBase):
    '''
    A command that will deactivate a context.
    '''

    def __init__(self, context):
        super().__init__(context)

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        self.context.settings.context = 'none'
        self.context.console.print('Context unset.')


class DefineContextCommand(commandbase.CommandBase):
    '''
    A command that will define a context.
    '''

    def __init__(self, context):
        super().__init__(context)
        self._confirm_filter = None
        self._context_name = ''
        self._task = None

    @property
    def confirm_filter(self):
        return self._confirm_filter

    @confirm_filter.setter
    def confirm_filter(self, value):
        self._confirm_filter = value

    @property
    def context_name(self):
        return self._context_name

    @context_name.setter
    def context_name(self, value):
        self._context_name = value

    @property
    def task(self):
        '''
        The task to add.
        '''
        return self._task

    @task.setter
    def task(self, value):
        self._task = value

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        can_execute = True
        if self.confirm_filter:
            can_execute = self.confirm_filter.query()
        
        if can_execute:
            definition = ''

            for tag in self.task.tags:
                if definition: definition += ' '
                definition += '+{}'.format(tag)

            for key in self.task.attributes:
                value = self.task.attributes[key]
                if definition: definition += ' '
                definition += '{}:{}'.format(key, value)

            self.context.settings.create_context(self.context_name, definition)
            self.context.console.print('Context created: {}'.format(self.context_name))


class DeleteContextCommand(commandbase.CommandBase):
    '''
    A command that will deactivate a context.
    '''

    def __init__(self, context):
        super().__init__(context)
        self._confirm_filter = None
        self._context_name = ''

    @property
    def confirm_filter(self):
        return self._confirm_filter

    @confirm_filter.setter
    def confirm_filter(self, value):
        self._confirm_filter = value

    @property
    def context_name(self):
        return self._context_name

    @context_name.setter
    def context_name(self, value):
        self._context_name = value

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        can_execute = True
        if self.confirm_filter:
            can_execute = self.confirm_filter.query()
        
        if can_execute:
            self.context.settings.delete_context(self.context_name)
            self.context.console.print('Context deleted: {}'.format(self.context_name))


class ListContextCommand(commandbase.CommandBase):
    '''
    A command that will deactivate a context.
    '''

    def __init__(self, context):
        super().__init__(context)

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        table = asciitable.DataTable()
        table.add_column('Name')
        table.add_column('Definition')
        table.add_column('Active')

        for name,definition,is_active in self.context.settings.get_contexts():
            table.add_row(name, definition, str(is_active))
            
        c = console.ConsoleFactory().get_console()
        c.foreground_colour = self.context.settings.table_row_forecolour
        c.background_colour = self.context.settings.table_row_backcolour
        c.print_table(table, self.context.settings.table_row_alt_forecolour, self.context.settings.table_row_alt_backcolour)


class ShowContextCommand(commandbase.CommandBase):
    '''
    A command that will deactivate a context.
    '''

    def __init__(self, context):
        super().__init__(context)

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        self.context.console.print(self.context.settings.context)


class ContextCommandParser(commandbase.CommandParserBase):
    COMMAND_NAME = 'context'

    def __init__(self):
        super().__init__(ContextCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        if not args:
            raise Exception('Context command required arguments')

        if args[0] == 'define':
            command = DefineContextCommand(context)
            command.context_name = args[1]
            command.task = self.parse_template_task(args[2:])
            if context.settings.command_context_define_confirm:
                prompt = 'Define context "{}"'.format(command.context_name)
                command.confirm_filter  = confirmfilter.ConfirmFilter(context, prompt)
            return command
        elif args[0] == 'delete':
            command = DeleteContextCommand(context)
            command.context_name = args[1]
            if context.settings.command_context_delete_confirm:
                prompt = 'Delete context "{}"'.format(command.context_name)
                command.confirm_filter = confirmfilter.ConfirmFilter(context, prompt)
            return command
        elif args[0] == 'list':
            return ListContextCommand(context)
        elif args[0] == 'none':
            return DeactivateContextCommand(context)
        elif args[0] == 'show':
            command = ShowContextCommand(context)
            return command
        else:
            command = ActivateContextCommand(context)
            command.context_name = args[0]
            return command

    def get_usage(self):
        usage = 'tasks {} define <name> <attributes>'.format(self.command_name)
        usage += '\r\ntasks {} delete <name>'.format(self.command_name)
        usage += '\r\ntasks {} list'.format(self.command_name)
        usage += '\r\ntasks {} none'.format(self.command_name)
        usage += '\r\ntasks {} show'.format(self.command_name)
        usage += '\r\ntasks {} <name>'.format(self.command_name)
        return usage
