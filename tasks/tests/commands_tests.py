import unittest
from unittest import mock

import commands as commands


class AddTaskCommandTests(unittest.TestCase):
    def test_execute_writes_to_file(self):
        test_path = 'test path'
        test_name = 'test name'
        expected_output = '[description:"test name"]'
        m = mock.mock_open()
        location = 'commands.open'
        with mock.patch(location, m) as mock_open:
            command = commands.AddTaskCommand()
            command.filename = test_path
            command.name = test_name
            command.execute()
        m.assert_called_once_with(test_path, 'a+')
        handle = m()
        handle.write.assert_called_once_with(expected_output + '\n')
        handle.__exit__.assert_called()

