import datetime
import unittest
import uuid

import formatters
import entities


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

        formatter = formatters.TaskWarriorFormatter()
        actual = formatter.format(task)

        self.assertEqual(expected, actual)

    def test_parse_parses_details(self):
        line = '['
        line += 'description:"new"'
        line += ' entry:"1575063536"'
        line += ' status:"pending"'
        line += ' uuid:"43462153-2313-4fc0-b1a4-f6c4b1501d8f"'
        line += ']'
        formatter = formatters.TaskWarriorFormatter()
        task = formatter.parse(1, line)
        self.assertIsNotNone(task)
        self.assertIsInstance(task, entities.Task)
        self.assertEqual(task.index, 1)
        self.assertEqual(task.name, 'new')
        self.assertEqual(task.status, 'pending')
        self.assertEqual(task.created, '1575063536')
        self.assertEqual(task.id_number, '43462153-2313-4fc0-b1a4-f6c4b1501d8f')
