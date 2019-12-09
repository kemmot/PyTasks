import datetime
import unittest
import unittest.mock as mock
import uuid

import entities
import storage


class TaskWarriorFormatterTests(unittest.TestCase):
    def test_format_gives_correct_output(self):
        task = entities.Task()
        task.created = datetime.datetime(2019, 11, 29, 20, 59, 18)
        task.id_number = uuid.UUID('a0bde7e1-21b5-4378-9e06-1f72e0336c28')
        task.name = 'task name'
        task.status = 'pending'

        expected = '['
        expected += 'description:"task name"'
        expected += ' entry:"1575061158"'
        expected += ' status:"pending"'
        expected += ' uuid:"' + str(task.id_number) + '"'
        expected += ']'

        formatter = storage.TaskWarriorPendingFormatter()
        actual = formatter.format(task)

        self.assertEqual(expected, actual)

    def test_parse_parses_details(self):
        line = '['
        line += 'description:"new"'
        line += ' entry:"1575063536"'
        line += ' status:"pending"'
        line += ' uuid:"43462153-2313-4fc0-b1a4-f6c4b1501d8f"'
        line += ']'
        formatter = storage.TaskWarriorPendingFormatter()
        task = formatter.parse(1, line)
        self.assertIsNotNone(task)
        self.assertIsInstance(task, entities.Task)
        self.assertEqual(task.index, 1)
        self.assertEqual(task.name, 'new')
        self.assertEqual(task.status, 'pending')
        self.assertEqual(task.created, '1575063536')
        self.assertEqual(task.id_number, '43462153-2313-4fc0-b1a4-f6c4b1501d8f')


class TaskWarriorPendingStorage(unittest.TestCase):
    def test_delete_deletes_correct_task(self):
        task1 = mock.Mock()
        task1.task_index = 1
        task2 = mock.Mock()
        task2.task_index = 2
        task3 = mock.Mock()
        task3.task_index = 3

        formatter = mock.Mock()
        formatter.format = mock.Mock(return_value='')
        formatter.parse = mock.Mock()
        formatter.parse.side_effect = [task1, task2, task3]

        target = storage.TaskWarriorPendingStorage('test path', formatter)

        mock_open = mock.mock_open(read_data='task1\ntask2\ntask3\n')
        with mock.patch('storage.open', mock_open):
            result = target.delete(task2)
        handle = mock_open()
        calls = [mock.call(task1), mock.call(task3)]
        self.assertEqual(calls, formatter.format.mock_calls)
        handle.write.assert_called()
        handle.__exit__.assert_called()

    def test_read_returns_matching_task(self):
        task1 = mock.Mock()
        task1.index = 1
        task2 = mock.Mock()
        task2.index = 2
        task3 = mock.Mock()
        task3.index = 3

        formatter = mock.Mock()
        formatter.parse = mock.Mock()
        formatter.parse.side_effect = [task1, task2, task3]

        target = storage.TaskWarriorPendingStorage('test path', formatter)

        mock_open = mock.mock_open(read_data='task1\ntask2\ntask3\n')
        with mock.patch('storage.open', mock_open):
            result = target.read(2)
        self.assertEqual(task2, result)
    
    def test_read_all_opens_and_closes_file(self):
        test_path = 'test path'
        target = storage.TaskWarriorPendingStorage(test_path)

        mock_open = mock.mock_open()
        with mock.patch('storage.open', mock_open):
            target.read_all()

        mock_open.assert_called_once_with(test_path, 'r')
        mock_open().__exit__.assert_called()

    def test_read_all_reads_file(self):
        target = storage.TaskWarriorPendingStorage('test path')

        mock_open = mock.mock_open()
        with mock.patch('storage.open', mock_open):
            target.read_all()

        mock_open().readlines.assert_called_once()
        
    def test_read_all_calls_parse(self):
        task = mock.MagicMock()

        formatter = mock.MagicMock()
        formatter.parse = mock.MagicMock(return_value=task)

        target = storage.TaskWarriorPendingStorage('test path', formatter)

        read_data = 'task1'
        mock_open = mock.mock_open(read_data=read_data)
        with mock.patch('storage.open', mock_open):
            result = target.read_all()

        formatter.parse.assert_called_once_with(1, read_data)
        
    def test_read_all_returns_correct_values(self):
        task = mock.MagicMock()

        formatter = mock.MagicMock()
        formatter.parse = mock.MagicMock(return_value=task)

        target = storage.TaskWarriorPendingStorage('test path', formatter)

        mock_open = mock.mock_open(read_data='task1\ntask2\n')
        with mock.patch('storage.open', mock_open):
            result = target.read_all()

        self.assertIsNotNone(result)
        self.assertEqual(2, len(result))
        self.assertEqual(result[0], task)
        self.assertEqual(result[1], task)

    def test_execute_writes_to_file(self):
        expected_output = 'testing 1 2 3'

        formatter = mock.MagicMock()
        formatter.format = mock.MagicMock(return_value=expected_output)

        task = entities.Task()
        task.created = datetime.datetime.now()

        test_path = 'test path'
        mock_open = mock.mock_open()
        with mock.patch('storage.open', mock_open):
            target = storage.TaskWarriorPendingStorage(test_path, formatter)
            target.write(task)
        mock_open.assert_called_once_with(test_path, 'a+')
        handle = mock_open()
        handle.write.assert_called_once_with(expected_output + '\n')
        handle.__exit__.assert_called()
