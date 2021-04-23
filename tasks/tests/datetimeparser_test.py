import datetime
import time
import unittest

import datetimeparser


class DateTimeParserTests(unittest.TestCase):
    def test_constructor_defaults_start_date(self):
        start = datetime.datetime.now()
        time.sleep(0.1)
        parser = datetimeparser.DateTimeParser()
        time.sleep(0.1)
        end = datetime.datetime.now()
        self.assertGreaterEqual(parser.start_date, start)
        self.assertLessEqual(parser.start_date, end)

    def test_constructor_sets_start_date(self):
        start = datetime.datetime(2021, 1, 1)
        parser = datetimeparser.DateTimeParser(start)
        self.assertEqual(start, parser.start_date)

    def test_parse_absolute_date_success(self):
        self.parse_date_success_test( \
            '2021-04-30', \
            datetime.datetime(2021, 4, 30))

    def test_parse_absolute_date_correct_format_invalid_date(self):
        parser = datetimeparser.DateTimeParser()
        with self.assertRaises(ValueError):
            parser.parse('2021-02-30')

    def test_parse_unrecognised_format(self):
        self.parse_date_failure_test('not a date')
        
    def test_parse_relative_date_correct_format_unrecognised_direction(self):
        self.parse_date_failure_test('~3d')
        
    def test_parse_relative_date_correct_format_unrecognised_value(self):
        self.parse_date_failure_test('-£d')
        
    def test_parse_relative_date_correct_format_unrecognised_unit(self):
        self.parse_date_failure_test('-3f')
        
    def test_parse_relative_date_negative_day_success(self):
        self.parse_date_success_test( \
            '-3d', \
            datetime.datetime(2019, 4, 19), \
            start=datetime.datetime(2019, 4, 22))
        
    def test_parse_relative_date_positive_day_success(self):
        self.parse_date_success_test( \
            '+5d', \
            datetime.datetime(2021, 6, 5), \
            start=datetime.datetime(2021, 5, 31))
        
    def test_parse_relative_date_unit_case_sensitive(self):
        self.parse_date_success_test( \
            '+5D', \
            datetime.datetime(2021, 6, 5), \
            start=datetime.datetime(2021, 5, 31))

    def parse_date_success_test(self, input, expected_result, start=None):
        parser = datetimeparser.DateTimeParser(start)
        result = parser.parse(input)
        self.assertEqual(expected_result, result)

    def parse_date_failure_test(self, input):
        with self.assertRaises(ValueError):
            datetimeparser.DateTimeParser().parse(input)

    def test_parse_handles_absolute_dates(self):
        pass

    def test_parse_handles_relative_dates(self):
        #start = datetime.datetime(2021, 5, 31)
        #parser = datetimeparser.DateTimeParser(start)
        #parser.parse()
        pass
