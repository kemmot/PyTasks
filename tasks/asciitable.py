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
        column_widths = self._calculate_column_widths()
        output = self._create_column_header(column_widths)
        if self._rows:
            output += self._row_separator
            if self.add_header_underline:
                output += self._create_line(column_widths)
                output += self._row_separator
            output += self._create_rows_output(column_widths)
        return output
    
    def _calculate_column_widths(self):
        column_widths = []

        for column in self._columns:
            column_widths.append(len(column))

        for row_index in range(0, len(self._rows)):
            row = self._rows[row_index]
            for column_index in range(0, len(column_widths)):
                column_width = column_widths[column_index]
                row_value_length = len(str(row[column_index]))
                if row_value_length > column_width:
                    column_widths[column_index] = row_value_length
        
        return column_widths
    
    def _create_column_header(self, column_widths):
        output = ''
        for column_index in range(0, len(column_widths)):
            if len(output) > 0:
                output += self._column_separator
            output += self._columns[column_index].ljust(column_widths[column_index])
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
    
    def _create_rows_output(self, column_widths):
        output = ''
        for row in self._rows:
            if output:
                output += self._row_separator
            output += self._create_row_output(row, column_widths)
        return output

    def _create_row_output(self, row, column_widths):
        output = ''
        for column_index in range(0, len(column_widths)):
            if len(output) > 0:
                output += self._column_separator
            output += str(row[column_index]).ljust(column_widths[column_index])
        return output
