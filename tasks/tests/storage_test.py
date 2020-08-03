import datetime
import os
import unittest
import unittest.mock as mock
import uuid

import __main__
import entities
import storage


class Empty:
    pass


class TaskWarriorFormatterTests(unittest.TestCase):
    def test_format_gives_correct_output_with_started(self):
        self.output_test(True)

    def test_format_gives_correct_output_without_started(self):
        self.output_test(False)

    def output_test(self, include_started):
        task = entities.Task()
        annotation1_date = datetime.datetime(2019, 12, 1, 20, 59, 18)
        annotation2_date = datetime.datetime(2019, 12, 2, 20, 59, 18)
        annotation1 = entities.TaskAnnotation('annotation 1', annotation1_date)
        annotation2 = entities.TaskAnnotation('annotation 2', annotation2_date)
        task.annotations.append(annotation1)
        task.annotations.append(annotation2)
        task.attributes['project'] = 'project 1'
        task.attributes['priority'] = 'high'
        task.created_time = datetime.datetime(2019, 11, 29, 20, 59, 18)
        task.id_number = uuid.UUID('a0bde7e1-21b5-4378-9e06-1f72e0336c28')
        task.name = 'task name'
        task.status = 'pending'
        if include_started:
            task.started_time = datetime.datetime(2019, 11, 29, 20, 59, 18)

        expected = '['
        expected += 'annotation_1575233958:"annotation 1"'
        expected += ' annotation_1575320358:"annotation 2"'
        expected += ' description:"task name"'
        expected += ' entry:"1575061158"'
        expected += ' priority:"high"'
        expected += ' project:"project 1"'
        if include_started:
            expected += ' start:"1575061158"'
        expected += ' status:"pending"'
        expected += ' uuid:"' + str(task.id_number) + '"'
        expected += ']'

        formatter = storage.TaskWarriorFormatter()
        actual = formatter.format(task)

        self.assertEqual(expected, actual)

    def test_parse_parses_details_with_started(self):
        self.parse_test(True)

    def test_parse_parses_details_without_started(self):
        self.parse_test(False)

    def parse_test(self, include_started):
        line = '['
        line += 'annotation_1575233958:"annotation 1"'
        line += ' annotation_1575320358:"annotation 2"'
        line += ' description:"new"'
        line += ' entry:"1575061158"'
        line += ' priority:"low"'
        line += ' project:"project 2"'
        if include_started:
            line += ' start:"1575061158"'
        line += ' status:"pending"'
        line += ' uuid:"43462153-2313-4fc0-b1a4-f6c4b1501d8f"'
        line += ']'
        formatter = storage.TaskWarriorFormatter()
        task = formatter.parse(1, line)
        self.assertIsNotNone(task)
        self.assertIsInstance(task, entities.Task)
        self.assertEqual(task.index, 1)
        self.assertEqual(task.name, 'new')
        self.assertEqual(task.status, 'pending')
        self.assertEqual(task.created_time, datetime.datetime(2019, 11, 29, 20, 59, 18))
        self.assertEqual(task.id_number, '43462153-2313-4fc0-b1a4-f6c4b1501d8f')
        self.assertEqual(len(task.annotations), 2)
        self.assertEqual(task.annotations[0].created, datetime.datetime(2019, 12, 1, 20, 59, 18))
        self.assertEqual(task.annotations[0].message, 'annotation 1')
        self.assertEqual(task.annotations[1].created, datetime.datetime(2019, 12, 2, 20, 59, 18))
        self.assertEqual(task.annotations[1].message, 'annotation 2')
        self.assertEqual(len(task.attributes), 2)
        self.assertTrue('project' in task.attributes)
        self.assertEqual(task.attributes['project'], 'project 2')
        self.assertTrue('priority' in task.attributes)
        self.assertEqual(task.attributes['priority'], 'low')
        if include_started:
            self.assertEqual(task.started_time, datetime.datetime(2019, 11, 29, 20, 59, 18))
        else:
            self.assertIsNone(task.started_time)


class TextFileStorageTests(unittest.TestCase):
    def setUp(self):
        self._formatter = mock.Mock()
        self._formatter.parse = mock.Mock()

    def test_constructor_sets_pproperties(self):
        test_path = '/d/temp.dat'
        target = storage.TextFileStorage(test_path, self._formatter)
        self.assertEqual(test_path, target.path)
        self.assertEqual(self._formatter, target.formatter)

    @mock.patch('storage.os.path')
    @mock.patch('storage.os')
    def test_delete_deletes_correct_task(self, mock_os, mock_path):
        tasks = self._create_tasks(3)

        self._formatter.format = mock.Mock(return_value='')
        self._formatter.parse.side_effect = tasks

        target = storage.TextFileStorage('test file', self._formatter)

        mock_path.isfile.return_value = True
        mock_open = mock.mock_open(read_data='task1\ntask2\ntask3\n')
        with mock.patch('storage.open', mock_open):
            target.delete(tasks[1])
        handle = mock_open()
        calls = [mock.call(tasks[0]), mock.call(tasks[2])]
        self.assertEqual(calls, self._formatter.format.mock_calls)
        handle.write.assert_called()
        handle.__exit__.assert_called()

    def test_read_all_does_not_open_file_if_not_exists(self):
        target = storage.TextFileStorage('test file', self._formatter)
        mock_isfile = mock.Mock(return_value=False)
        with mock.patch('os.path.isfile', mock_isfile):
            results = target.read_all()
        self.assertEqual(0, len(results))

    def test_read_all_opens_and_closes_file(self):
        target = storage.TextFileStorage('/d/test/file.dat', self._formatter)

        mock_isfile = mock.Mock(return_value=True)
        with mock.patch('os.path.isfile', mock_isfile):
            mock_open = mock.mock_open()
            with mock.patch('storage.open', mock_open):
                target.read_all()

        mock_open.assert_called_once_with('/d/test/file.dat', 'r')
        mock_open().__exit__.assert_called()

    def test_read_all_reads_file(self):
        target = storage.TextFileStorage('test file', self._formatter)

        mock_isfile = mock.Mock(return_value=True)
        with mock.patch('os.path.isfile', mock_isfile):
            mock_open = mock.mock_open()
            with mock.patch('storage.open', mock_open):
                target.read_all()

            mock_open().readlines.assert_called_once()

    def test_read_all_calls_parse(self):
        task = self._create_task()

        self._formatter.parse = mock.MagicMock(return_value=task)

        target = storage.TextFileStorage('test file', self._formatter)

        read_data = 'task1'
        mock_isfile = mock.Mock(return_value=True)
        with mock.patch('os.path.isfile', mock_isfile):
            mock_open = mock.mock_open(read_data=read_data)
            with mock.patch('storage.open', mock_open):
                target.read_all()

        self._formatter.parse.assert_called_once_with(1, read_data)

    def test_read_all_returns_correct_values(self):
        task = self._create_task()

        self._formatter.parse = mock.MagicMock(return_value=task)

        target = storage.TextFileStorage('test path', self._formatter)

        mock_isfile = mock.Mock(return_value=True)
        with mock.patch('os.path.isfile', mock_isfile):
            mock_open = mock.mock_open(read_data='task1\ntask2\n')
            with mock.patch('storage.open', mock_open):
                result = target.read_all()

        self.assertIsNotNone(result)
        self.assertEqual(2, len(result))
        self.assertEqual(result[0], task)
        self.assertEqual(result[1], task)

    @mock.patch('storage.os.path')
    @mock.patch('storage.os')
    def test_update_updates_correct_task(self, mock_os, mock_path):
        tasks = self._create_tasks(3)
        new_task = mock.Mock()
        new_task.id_number = tasks[1].id_number

        self._formatter.format = mock.Mock(return_value='')
        self._formatter.parse.side_effect = tasks

        target = storage.TextFileStorage('test file', self._formatter)

        mock_path.isfile.return_value = True
        mock_open = mock.mock_open(read_data='task1\ntask2\ntask3\n')
        with mock.patch('storage.open', mock_open):
            target.update([new_task])
        handle = mock_open()
        calls = [mock.call(tasks[0]), mock.call(new_task), mock.call(tasks[2])]
        self.assertEqual(calls, self._formatter.format.mock_calls)
        handle.write.assert_called()
        handle.__exit__.assert_called()

    @mock.patch('storage.os.path')
    @mock.patch('storage.os')
    def test_write_writes_to_file(self, mock_os, mock_path):
        expected_output = 'testing 1 2 3'

        self._formatter.format = mock.MagicMock(return_value=expected_output)

        task = entities.Task()
        task.created = datetime.datetime.now()

        test_data_location = '/tmp'
        test_pending_filename = 'test.dat'
        test_path = '/tmp/test.dat'
        temp_path = '/tmp/test.dat.tmp'
        mock_path.isfile.return_value = True
        mock_path.join.return_value = test_path
        mock_settings = Empty()
        mock_settings.data_location = test_data_location
        mock_settings.data_pending_filename = test_pending_filename
        mock_open = mock.mock_open()
        with mock.patch('storage.open', mock_open):
            target = storage.TextFileStorage(test_path, self._formatter)
            target.write(task)

        calls = [mock.call(test_path), mock.call(temp_path), mock.call(test_path)]
        self.assertEqual(calls, mock_path.isfile.mock_calls)

        calls = [mock.call(temp_path), mock.call(test_path)]
        self.assertEqual(calls, mock_os.remove.mock_calls)

        mock_open.assert_called_with(temp_path, 'w+')
        handle = mock_open()
        handle.write.assert_called_once_with(expected_output + '\n')
        handle.__exit__.assert_called()
        mock_os.rename.assert_called_with(temp_path, test_path)

    def _create_tasks(self, count):
        tasks = []
        for task_index in range(1, count+1):
            tasks.append(self._create_task(task_index))
        return tasks

    def _create_task(self, task_index=1):
        task = mock.Mock()
        task.index = task_index
        task.id_number = uuid.uuid4()
        return task


class TaskWarriorStorageTests(unittest.TestCase):
    def test_constructor_sets_properties(self):
        mock_pending_storage = mock.Mock()
        mock_done_storage = mock.Mock()
        target = storage.TaskWarriorStorage(mock_pending_storage, mock_done_storage)
        self.assertEqual(mock_pending_storage, target.pending_storage)
        self.assertEqual(mock_done_storage, target.done_storage)

    def test_delete_calls_write_on_done_storage(self):
        mock_pending_storage = mock.Mock()
        mock_pending_storage.delete = mock.MagicMock()
        mock_done_storage = mock.Mock()
        mock_done_storage.write = mock.MagicMock()
        mock_task = mock.Mock()
        target = storage.TaskWarriorStorage(mock_pending_storage, mock_done_storage)
        target.delete(mock_task)
        mock_done_storage.write.assert_called_once_with(mock_task)

    def test_delete_calls_delete_on_pending_storage(self):
        mock_pending_storage = mock.Mock()
        mock_pending_storage.delete = mock.MagicMock()
        mock_done_storage = mock.Mock()
        mock_task = mock.Mock()
        target = storage.TaskWarriorStorage(mock_pending_storage, mock_done_storage)
        target.delete(mock_task)
        mock_pending_storage.delete.assert_called_once_with(mock_task)

    def test_read_all_calls_read_all_on_pending_storage(self):
        tasks = [mock.Mock(), mock.Mock()]
        mock_pending_storage = mock.Mock()
        mock_pending_storage.read_all = mock.MagicMock(return_value=tasks)
        mock_done_storage = mock.Mock()
        target = storage.TaskWarriorStorage(mock_pending_storage, mock_done_storage)
        result = target.read_all()
        self.assertEqual(tasks, result)

    def test_update_calls_update_on_pending_storage(self):
        mock_pending_storage = mock.Mock()
        mock_pending_storage.update = mock.MagicMock()
        mock_done_storage = mock.Mock()
        mock_task = mock.Mock()
        target = storage.TaskWarriorStorage(mock_pending_storage, mock_done_storage)
        target.update(mock_task)
        mock_pending_storage.update.assert_called_once_with(mock_task)

    def test_write_calls_write_on_pending_storage(self):
        mock_pending_storage = mock.Mock()
        mock_pending_storage.write = mock.MagicMock()
        mock_done_storage = mock.Mock()
        mock_task = mock.Mock()
        target = storage.TaskWarriorStorage(mock_pending_storage, mock_done_storage)
        target.write(mock_task)
        mock_pending_storage.write.assert_called_once_with(mock_task)


class TaskWarriorStorageCreatorTests(unittest.TestCase):
    def test_constructor_sets_absolute_path_without_alteration(self):
        mock_settings = mock.Mock()
        mock_settings.data_location = '/d/test/'
        mock_settings.data_pending_filename = 'pending.dat'
        mock_settings.data_done_filename = 'done.dat'
        result = storage.TaskWarriorStorageCreator().create(mock_settings)
        self.assertIsInstance(result, storage.TaskWarriorStorage)
        self.assertEqual('/d/test/pending.dat', result.pending_storage.path)

    def test_constructor_sets_path_relative_to_main(self):
        mock_settings = mock.Mock()
        mock_settings.data_location = 'test'
        mock_settings.data_pending_filename = 'pending.dat'
        mock_settings.data_done_filename = 'done.dat'
        result = storage.TaskWarriorStorageCreator().create(mock_settings)
        full_test_path = os.path.join(os.path.dirname(__main__.__file__), 'test')
        full_test_path = os.path.join(full_test_path, 'pending.dat')
        self.assertIsInstance(result, storage.TaskWarriorStorage)
        self.assertEqual(full_test_path, result.pending_storage.path)
