import datetime
import unittest
from unittest import mock

import entities


class TaskTests(unittest.TestCase):
    def test_constructor_sets_properties(self):
        test_start_time = datetime.datetime.now()
        task = entities.Task()
        self.assertIsNotNone(task.created_time)
        self.assertGreater(task.created_time, test_start_time)
    
    def test_is_started_correct(self):
        task = entities.Task()
        task.start()
        self.assertTrue(task.is_started)
        task.stop()
        self.assertFalse(task.is_started)
    
    def test_start_sets_started_field(self):
        test_start_time = datetime.datetime.now()
        task = entities.Task()
        task.start()
        self.assertIsNotNone(task.started_time)
        self.assertGreater(task.started_time, test_start_time)
    
    def test_stop_clears_started_field(self):
        test_start_time = datetime.datetime.now()
        task = entities.Task()
        task.stop()
        self.assertIsNone(task.started_time)
