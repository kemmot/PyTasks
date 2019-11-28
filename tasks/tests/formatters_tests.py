import unittest

import formatters
import entities


class TaskWarriorFormatterTests(unittest.TestCase):
    def test_format_gives_correct_output(self):
        task = entities.Task()
        task.name = 'task name'

        expected = '[description:"'
        expected += task.name
        expected += '"]'

        formatter = formatters.TaskWarriorFormatter()
        actual = formatter.format(task)

        self.assertEqual(expected, actual)

