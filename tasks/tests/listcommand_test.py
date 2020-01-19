import unittest
from unittest import mock
from unittest.mock import MagicMock

import commands.listcommand as listcommand


class ListTaskCommandTests(unittest.TestCase):
    def test_execute_calls_read_all_on_storage(self):
        tasks = []
        tasks.append(mock.MagicMock())
        tasks.append(mock.MagicMock())

        storage = mock.MagicMock()
        storage.read_all = MagicMock(return_value=tasks)

        command = listcommand.ListTaskCommand(storage)
        command.execute()

        storage.read_all.assert_called_once()

    def test_execute_prints_content(self):
        task = mock.MagicMock()
        task.name = 'test1'
        task.status = 'pending'
        task.id_number = 0
        task.created = ''

        tasks = []
        tasks.append(task)

        storage = mock.MagicMock()
        storage.read_all = MagicMock(return_value=tasks)

        command = listcommand.ListTaskCommand(storage)

        mock_print = mock.MagicMock()
        with mock.patch('commands.listcommand.print', mock_print):
            command.execute()

        mock_print.assert_called()


class ListTaskCommandParserTests(unittest.TestCase):
    def test_parse_wrong_command(self):
        args = ['wrong']
        storage = mock.Mock()
        command = listcommand.ListTaskCommandParser().parse(storage, args)
        self.assertEqual(None, command)

    def test_parse_success(self):
        args = ['list']

        storage = mock.Mock()
        command = listcommand.ListTaskCommandParser().parse(storage, args)

        self.assertIsInstance(command, listcommand.ListTaskCommand)
        self.assertEqual(command.storage, storage)
