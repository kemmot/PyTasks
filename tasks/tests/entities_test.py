import datetime
import time
import unittest

import entities


class TaskTests(unittest.TestCase):
    def test_constructor_sets_properties(self):
        test_start_time = datetime.datetime.now()
        time.sleep(0.1)
        task = entities.Task()
        self.assertIsNotNone(task.created_time)
        self.assertGreater(task.created_time, test_start_time)

    def test_end_sets_ended_field(self):
        test_start_time = datetime.datetime.now()
        time.sleep(0.1)
        task = entities.Task()
        task.end()
        self.assertIsNotNone(task.end_time)
        self.assertGreater(task.end_time, test_start_time)

    def test_is_ended_correct(self):
        task = entities.Task()
        self.assertFalse(task.is_ended)
        task.end()
        self.assertTrue(task.is_ended)

    def test_is_started_correct(self):
        task = entities.Task()
        task.start()
        self.assertTrue(task.is_started)
        task.stop()
        self.assertFalse(task.is_started)

    def test_start_sets_started_field(self):
        test_start_time = datetime.datetime.now()
        time.sleep(0.1)
        task = entities.Task()
        task.start()
        self.assertIsNotNone(task.started_time)
        self.assertGreater(task.started_time, test_start_time)

    def test_stop_clears_started_field(self):
        task = entities.Task()
        task.stop()
        self.assertIsNone(task.started_time)


class TaskAttributeNameTests(unittest.TestCase):
    def test_get_names(self):
        names = entities.TaskAttributeName.get_names()
        self.assertIsNotNone(names)
        self.assertEqual(len(names), 7)
        self.assertEqual(names[0], entities.TaskAttributeName.DESCRIPTION)
        self.assertEqual(names[1], entities.TaskAttributeName.END)
        self.assertEqual(names[2], entities.TaskAttributeName.ENTRY)
        self.assertEqual(names[3], entities.TaskAttributeName.ID)
        self.assertEqual(names[4], entities.TaskAttributeName.START)
        self.assertEqual(names[5], entities.TaskAttributeName.STATUS)
        self.assertEqual(names[6], entities.TaskAttributeName.WAIT)

    def test_get_name(self):
        self.assertEqual(entities.TaskAttributeName.get_name(entities.TaskAttributeType.DESCRIPTION), 'description')
        self.assertEqual(entities.TaskAttributeName.get_name(entities.TaskAttributeType.END), 'end')
        self.assertEqual(entities.TaskAttributeName.get_name(entities.TaskAttributeType.ENTRY), 'entry')
        self.assertEqual(entities.TaskAttributeName.get_name(entities.TaskAttributeType.ID), 'id')
        self.assertEqual(entities.TaskAttributeName.get_name(entities.TaskAttributeType.START), 'start')
        self.assertEqual(entities.TaskAttributeName.get_name(entities.TaskAttributeType.STATUS), 'status')
        self.assertEqual(entities.TaskAttributeName.get_name(entities.TaskAttributeType.WAIT), 'wait')

    def test_is_name_valid(self):
        self.assertTrue(entities.TaskAttributeName.is_name_valid('description'))
        self.assertTrue(entities.TaskAttributeName.is_name_valid('end'))
        self.assertTrue(entities.TaskAttributeName.is_name_valid('entry'))
        self.assertTrue(entities.TaskAttributeName.is_name_valid('id'))
        self.assertTrue(entities.TaskAttributeName.is_name_valid('start'))
        self.assertTrue(entities.TaskAttributeName.is_name_valid('status'))
        self.assertTrue(entities.TaskAttributeName.is_name_valid('wait'))

        self.assertFalse(entities.TaskAttributeName.is_name_valid(''))
        self.assertFalse(entities.TaskAttributeName.is_name_valid('name'))
        self.assertFalse(entities.TaskAttributeName.is_name_valid('womble'))
