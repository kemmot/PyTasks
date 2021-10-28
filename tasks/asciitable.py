class DataTable:
    def __init__(self):
        self._columns = []
        self._rows = []
    
    @property
    def columns(self):
        return self._columns
    
    @property
    def rows(self):
        return self._rows

    def add_column(self, name):
        self._columns.append(name)

    def add_row(self, *row_values):
        self._rows.append(row_values)


class AsciiTable:
    def __init__(self):
        self._add_header_underline = False
        self._column_separator = ' '
        self._columns = []
        self._row_separator = '\n'
        self._rows = []

    @property
    def add_header_underline(self):
        return self._add_header_underline

    @add_header_underline.setter
    def add_header_underline(self, value):
        self._add_header_underline = value

    @property
    def column_separator(self):
        return self._column_separator

    @column_separator.setter
    def column_separator(self, value):
        self._column_separator = value

    def add_column(self, name):
        self._columns.append(name)

    def add_row(self, *row_values):
        self._rows.append(row_values)

    def create_output(self):
        output = ''
        for line in self.create_output_lines():
            if output:
                output += self._row_separator
            output += line
        return output

    def create_output_lines(self):
        lines = []
        column_widths = self._calculate_column_widths()
        lines.append(self._create_column_header(column_widths))
        if self._rows:
            if self.add_header_underline:
                lines.append(self._create_line(column_widths))
            for line in self._create_rows_output_lines(column_widths):
                lines.append(line)
        return lines

    def _calculate_column_widths(self):
        column_widths = []

        for column in self._columns:
            column_widths.append(len(column))

        for row in self._rows:
            column_index = 0
            for cell in row:
                row_value_length = len(str(cell))
                if column_index < len(column_widths):
                    if row_value_length > column_widths[column_index]:
                        column_widths[column_index] = row_value_length
                else:
                    column_widths.append(row_value_length)
                column_index += 1

        return column_widths

    def _create_column_header(self, column_widths):
        output = ''
        column_index = 0
        for column_width in column_widths:
            if output:
                output += self._column_separator
            if column_index < len(self._columns):
                column_header = self._columns[column_index]
            else:
                column_header = ''
            output += column_header.ljust(column_width)
            column_index += 1
        return output

    def _create_line(self, column_widths):
        return '-' * self._calculate_line_width(column_widths)

    def _calculate_line_width(self, column_widths):
        line_width = 0
        for column_width in column_widths:
            if line_width > 0:
                line_width += len(self._column_separator)
            line_width += column_width
        return line_width

    def _create_rows_output_lines(self, column_widths):
        lines = []
        for row in self._rows:
            lines.append(self._create_row_output_line(row, column_widths))
        return lines

    def _create_row_output_line(self, row, column_widths):
        output = ''
        column_index = 0
        for column_width in column_widths:
            if output:
                output += self._column_separator
            if column_index < len(row):
                cell = str(row[column_index])
            else:
                cell = ''
            output += cell.ljust(column_width)
            column_index += 1
        return output
