import os
import subprocess
import tempfile

import commands.commandbase as commandbase
import filters.confirmfilter as confirmfilter
import storage


class EditCommand(commandbase.FilterCommandBase):
    def execute_tasks(self, tasks):
        '''
        Executes the logic of this command.
        '''
        if tasks:
            first_task = tasks[0]
            filename = self._generate_filename()
            self._write_task(filename, first_task)
            if self._edit_task(filename):
                new_task = self._read_task(filename)
                new_task.id_number = first_task.id_number
                new_task.created_time = first_task.created_time
                self.context.storage.update([new_task])
            os.unlink(filename)
    
    def _generate_filename(self):
        file = tempfile.NamedTemporaryFile(delete=False)
        name = file.name
        file.close()
        return name

    def _write_task(self, filename, task):
        output = storage.EditFormatter().format(task)
        with open(filename, 'w') as output_file:
            output_file.write(output)

    def _edit_task(self, filename):
        editor = self._get_editor()
        process = subprocess.Popen([editor, filename])
        process.wait()
        success = True if process.returncode == 0 else False
        return success

    def _get_editor(self):
        editor = self.context.settings.command_edit_editor
        if not editor:
            editor_environment_variable = 'EDITOR'
            if not editor_environment_variable in os.environ:
                raise Exception(f'No editor found in settings or ''{editor_environment_variable}'' environment variable')
            editor = os.environ[editor_environment_variable]
        return editor

    def _read_task(self, filename):
        with open(filename, 'r') as input_file:
            lines = input_file.readlines()
        return storage.EditFormatter().parse(lines)


class EditCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'edit'

    def __init__(self):
        super().__init__(EditCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return EditCommand(context)

    def get_confirm_filter(self, context):
        return None
