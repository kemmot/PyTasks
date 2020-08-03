import datetime
import unittest
from unittest import mock

import entities


class TaskTests(unittest.TestCase):
    def test_constructor_sets_properties(self):
        test_start_time = datetime.datetime.now()
        task = entities.Task()
        self.assertIsNotNone(task.created)
        self.assertGreater(task.created, test_start_time)
    
    def test_start_sets_started_field(self):
        test_start_time = datetime.datetime.now()
        task = entities.Task()
        task.start()
        self.assertIsNotNone(task.started)
        self.assertGreater(task.started, test_start_time)
    
    def test_stop_clears_started_field(self):
        test_start_time = datetime.datetime.now()
        task = entities.Task()
        task.stop()
        self.assertIsNone(task.started)
