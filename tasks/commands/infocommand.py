import commands.commandbase as commandbase
import entities as entities
import storage as storage


class InfoCommand(commandbase.FilterCommandBase):
    def __init__(self, context, batch_filter=None):
        super().__init__(context, batch_filter)

    def execute_tasks(self, tasks):
        '''
        Executes the logic of this command.
        '''
        for task in tasks:
            values = dict()
            values['ID'] = task.index
            values['Description'] = task.name
            values['Status'] = task.status
            values['Entered'] = task.created_time
            values['UUID'] = task.id_number
            values['Wait'] = task.wait_time
            
            tag_string = entities.TaskAttributeRetriever().get_value(task, entities.TaskAttributeName.TAGS)
            if tag_string:
                values['Tags'] = tag_string

            for attribute_name, attribute_value in task.attributes.items():
                values[attribute_name] = attribute_value

            max_attribute_name_length = 0
            for attribute_name, attribute_value in values.items():
                if len(attribute_name) > max_attribute_name_length:
                    max_attribute_name_length = len(attribute_name)
            self.context.console.print('{} Value'.format('Name'.ljust(max_attribute_name_length)))
            for attribute_name, attribute_value in values.items():
                self.context.console.print('{} {}'.format(attribute_name.ljust(max_attribute_name_length), attribute_value))

            if task.annotations:
                self.context.console.print('')
                self.context.console.print('Date             Modification')
                for annotation in task.annotations:
                    date = annotation.created.strftime('%Y-%m-%d %H:%M')
                    self.context.console.print('{} {}'.format(date, annotation.message))


class InfoCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'info'

    def __init__(self):
        super().__init__(InfoCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return InfoCommand(context)
