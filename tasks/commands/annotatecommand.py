import commands.commandbase as commandbase
import entities
import filters.allbatchfilter as allbatchfilter
import filters.confirmfilter as confirmfilter


class AnnotateCommand(commandbase.FilterCommandBase):
    def __init__(self, context, batch_filter):
        super().__init__(context, batch_filter)
        self._message = None

    @property
    def message(self):
        '''
        The annotation message to add.
        '''
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        tasks = self.get_filtered_tasks()
        for task in tasks:
            annotation = entities.TaskAnnotation(self.message)
            task.annotations.append(annotation)
            print('Task annotated: {}'.format(task.index))
        self.context.storage.update(tasks)


class AnnotateCommandParser(commandbase.CommandParserBase):
    def parse(self, context, filter_factory, args):
        if len(args) >= 3 and args[1] == 'annotate':
            batch_filter = allbatchfilter.AllBatchFilter()
            batch_filter.add_filter(filter_factory.parse(args[0]))

            if context.settings.command_annotate_confirm:
                batch_filter.add_filter(confirmfilter.ConfirmFilter('Annotate'))

            command = AnnotateCommand(context, batch_filter)
            command.message = ' '.join(args[2:])
        else:
            command = None
        return command
