import asciitable as asciitable
import console as console
import entities as entities
import commands.commandbase as commandbase
import filters.confirmfilter as confirmfilter


class UndoCommand(commandbase.CommandBase):
    def __init__(self, context):
        super().__init__(context)

    def execute(self):
        '''
        Executes the logic of this command.
        '''

        # TODO: get most recent undo entry
        change = self.context.storage.undo_log.get_most_recent_change()
        #print(change)
        #print(change.attributes['__change_date__'])
        #print(change.attributes['__change_type__'])

        # TODO: find affected tasks
        all_tasks = self.context.storage.read_all()
        for task in all_tasks:
            if task.id_number == change.id_number:
                print('The last modification was made {}'.format(change.attributes['__change_date__']))

                retriever = entities.TaskAttributeRetriever()
                table = asciitable.DataTable()
                table.add_column('')
                table.add_column('Prior Values')
                table.add_column('Current Values')
                for name in entities.TaskAttributeName.get_names():
                    prior_value = retriever.get_value(change, name)
                    current_value = retriever.get_value(task, name)
                    if name != entities.TaskAttributeName.ID and prior_value != current_value:
                        row_values = []
                        row_values.append(name)
                        row_values.append(str(prior_value))
                        row_values.append(str(current_value))
                        table.add_row(*row_values)
                
                # TODO: add custom attributes

                # TODO: add annotations

                #self.print_table(table)
                c = console.ConsoleFactory().get_console()
                c.print_table(table, self.context.settings.table_row_alt_forecolour, self.context.settings.table_row_alt_backcolour)

                # TODO: request confirmation
                print('The undo command is not reversible.  Are you sure you want to revert to the previous state? (yes/no)')

        # TODO: save changes
        #self.context.storage.update(tasks)

        # TODO: remove actioned undo entry

        pass


class UndoCommandParser(commandbase.CommandParserBase):
    COMMAND_NAME = 'undo'

    def __init__(self):
        super().__init__(UndoCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return UndoCommand(context)

    def get_confirm_filter(self, context):
        if context.settings.command_undo_confirm:
            return confirmfilter.ConfirmFilter(context, 'Undo')
        return None
