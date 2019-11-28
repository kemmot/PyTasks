import unittest
import uuid

import formatters
import entities


class TaskWarriorFormatterTests(unittest.TestCase):
    def test_format_gives_correct_output(self):
        task = entities.Task()
        task.id_number = uuid.UUID('a0bde7e1-21b5-4378-9e06-1f72e0336c28')
        task.name = 'task name'
        task.status = 'pending'

        expected = '['
        expected += 'description:"' + task.name + '"'
        expected += ' status:"' + task.status + '"'
        expected += ' uuid:"' + str(task.id_number) + '"'
        expected += ']'

        formatter = formatters.TaskWarriorFormatter()
        actual = formatter.format(task)

        self.assertEqual(expected, actual)
