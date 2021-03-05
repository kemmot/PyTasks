import datetime
import re


class DateTimeParser:
    def parse(self, date_time_string):
        match = re.search('\d{4}-\d{2}-\d{2}', date_time_string)
        if match is not None:
            date = datetime.datetime.strptime(date_time_string, '%Y-%m-%d')
            return date

        raise Exception('Date not recognised: [{}]'.format(date_time_string))
