import unittest
import uuid

import formatters
import entities


class TaskWarriorFormatterTests(unittest.TestCase):
    def test_format_gives_correct_output(self):
        name = 'task name'
        id = 'a0bde7e1-21b5-4378-9e06-1f72e0336c28'
        id_string = '{' + id + '}'
        status = 'pending'

        task = entities.Task()
        task.id = uuid.UUID(id_string)
        task.name = name
        task.status = status

        expected = '['
        expected += 'description:"' + task.name + '"'
        expected += ' status:"' + task.status + '"'
        expected += ' uuid:"' + str(task.id) + '"'
        expected += ']'

        formatter = formatters.TaskWarriorFormatter()
        actual = formatter.format(task)

        self.assertEqual(expected, actual)
