import calendar
import datetime
import re


class DateTimeParser:
    def __init__(self, start_date=None):
        if not start_date:
            # NOTE: doing this as a default argument value lazy evaluates
            self._start_date = datetime.datetime.now()
        else:
            self._start_date = start_date

    @property
    def start_date(self):
        return self._start_date

    def parse(self, date_time_string):
        date = self.parse_special_date(date_time_string)
        if date:
            return date

        date = self.parse_absolute_date(date_time_string)
        if date:
            return date
        
        date = self.parse_relative_date(date_time_string)
        if date:
            return date

        raise ValueError('Date format not recognised: [{}]'.format(date_time_string))

    def parse_special_date(self, date_time_string):
        if date_time_string == 'today':
            return datetime.datetime.today()
        elif date_time_string == 'tomorrow':
            return datetime.datetime.today() + datetime.timedelta(days=1)
        else:
            return None

    def parse_absolute_date(self, date_time_string):
        match = re.search('\d{4}-\d{2}-\d{2}', date_time_string)
        if not match:
            return None

        date = datetime.datetime.strptime(date_time_string, '%Y-%m-%d')
        return date

    def parse_relative_date(self, date_time_string):
        regex = re.compile('(?P<direction>[+-])(?P<value>\d+)(?P<unit>[dmwy])', re.IGNORECASE)
        match = regex.search(date_time_string)
        if not match:
            return None
        
        direction = match.group('direction')
        value = int(match.group('value'))
        unit = match.group('unit')
        
        if unit.upper() == 'D':
            day_count = int(match.group('value'))
            if direction == '-':
                day_count *= -1
            return self.__add_days(self.start_date, day_count)
        
        if unit.upper() == 'M':
            month_count = int(match.group('value'))
            year = self.start_date.year
            month = self.start_date.month
            day = self.start_date.day
            month += month_count
            while month > 12:
                year += 1
                month -= 12
            first_weekday,days_in_month = calendar.monthrange(year, month)
            if day > days_in_month:
                day = days_in_month
            date = datetime.date(year, month, day)
            return datetime.datetime.combine(date, datetime.datetime.min.time())
        
        if unit.upper() == 'W':
            week_count = int(match.group('value'))
            day_count = week_count * 7
            if direction == '-':
                day_count *= -1
            return self.__add_days(self.start_date, day_count)
        
        if unit.upper() == 'Y':
            year_count = int(match.group('value'))
            year = self.start_date.year
            month = self.start_date.month
            day = self.start_date.day
            year += year_count
            date = datetime.date(year, month, day)
            return datetime.datetime.combine(date, datetime.datetime.min.time())
        
        raise ValueError('Unrecognised date unit: [{}]'.format(unit))
    
    def __add_days(self, date, day_count):
        delta = datetime.timedelta(days=day_count)
        date = date + delta
        date = datetime.datetime.combine(date, datetime.datetime.min.time())
        return date
