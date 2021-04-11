import unittest
from unittest import mock

import asciitable as asciitable


class AsciiTableTests(unittest.TestCase):
    def test_add_header_underline_setter(self):
        table = asciitable.AsciiTable()
        self.assertEqual(False, table.add_header_underline)
        table.add_header_underline = True
        self.assertEqual(True, table.add_header_underline)

    def test_column_separator_setter(self):
        table = asciitable.AsciiTable()
        table.column_separator = 'yak'
        self.assertEqual('yak', table.column_separator)

    def test_create_output_with_no_input(self):
        table = asciitable.AsciiTable()
        result = table.create_output()
        self.assertEqual('', result)

    def test_create_output_1_column_0_rows(self):
        columns = ['column 1']
        rows = [ ]
        output = [ 'column 1' ]
        self._run_test(columns, rows, output, column_separator = ' ')

    def test_create_output_2_columns_0_rows(self):
        columns = ['column 1', 'column 2']
        rows = [ ]
        output = [ 'column 1 column 2' ]
        self._run_test(columns, rows, output, column_separator = ' ')

    def test_create_output_4_columns_0_rows_specific_column_separator(self):
        columns = ['column 1', 'column 2', 'column 3', 'column 4']
        rows = [ ]
        output = [ 'column 1 | column 2 | column 3 | column 4' ]
        self._run_test(columns, rows, output, column_separator = ' | ')
    
    def test_create_output_1_column_1_row(self):
        columns = ['column 1']
        rows = [ ['cell A'] ]
        output = [ 
            'column 1',
            'cell A  ' ]
        self._run_test(columns, rows, output)
    
    def test_create_output_1_column_2_rows(self):
        columns = ['column 1']
        rows = [
            ['cell A'],
            ['cell B']
        ]
        output = [
            'column 1',
            'cell A  ',
            'cell B  ',
        ]
        self._run_test(columns, rows, output)
        
    def test_create_output_3_column_3_rows(self):
        columns = ['column 1', 'column 2', 'column 3']
        rows = [
            ['cell A1','cell A2','cell A3'],
            ['cell B1','cell B2','cell B3'],
            ['cell C1','cell C2','cell C3']
        ]
        output = [
            'column 1 | column 2 | column 3',
            'cell A1  | cell A2  | cell A3 ',
            'cell B1  | cell B2  | cell B3 ',
            'cell C1  | cell C2  | cell C3 ',
        ]
        self._run_test(columns, rows, output, column_separator = ' | ')
        
    def test_create_output_variable_width_column_headers(self):
        columns = ['column 1', 'column 2 is longer', 'column 3']
        rows = [
            ['cell A1','cell A2','cell A3'],
            ['cell B1','cell B2','cell B3'],
            ['cell C1','cell C2','cell C3']
        ]
        output = [
            'column 1 | column 2 is longer | column 3',
            'cell A1  | cell A2            | cell A3 ',
            'cell B1  | cell B2            | cell B3 ',
            'cell C1  | cell C2            | cell C3 ',
        ]
        self._run_test(columns, rows, output, column_separator = ' | ')
        
    def test_create_output_variable_width_cells(self):
        columns = ['column 1', 'column 2', 'column 3']
        rows = [
            ['cell A1','cell A2','cell A3'],
            ['cell B1 longer','cell B2','cell B3'],
            ['cell C1','cell C2','cell C3']
        ]
        output = [
            'column 1       | column 2 | column 3',
            'cell A1        | cell A2  | cell A3 ',
            'cell B1 longer | cell B2  | cell B3 ',
            'cell C1        | cell C2  | cell C3 ',
        ]
        self._run_test(columns, rows, output, column_separator = ' | ')
        
    def test_create_output_variable_width_cells_underline(self):
        columns = ['column 1', 'column 2', 'column 3']
        rows = [
            ['cell A1','cell A2','cell A3'],
            ['cell B1 longer','cell B2','cell B3'],
            ['cell C1','cell C2','cell C3']
        ]
        output = [
            'column 1       | column 2 | column 3',
            '------------------------------------',
            'cell A1        | cell A2  | cell A3 ',
            'cell B1 longer | cell B2  | cell B3 ',
            'cell C1        | cell C2  | cell C3 ',
        ]
        self._run_test(columns, rows, output, column_separator = ' | ', add_header_underline = True)
    
    def test_more_row_cells_than_columns(self):
        columns = ['column 1', 'column 2']
        rows = [
            ['cell A1','cell A2','cell A3'],
            ['cell B1','cell B2','cell B3'],
            ['cell C1','cell C2','cell C3']
        ]
        output = [
            'column 1 | column 2 |        ',
            '-----------------------------',
            'cell A1  | cell A2  | cell A3',
            'cell B1  | cell B2  | cell B3',
            'cell C1  | cell C2  | cell C3',
        ]
        self._run_test(columns, rows, output, column_separator = ' | ', add_header_underline = True)
    
    def test_more_columns_than_row_cells(self):
        columns = ['column 1', 'column 2', 'column 3']
        rows = [
            ['cell A1','cell A2'],
            ['cell B1','cell B2'],
            ['cell C1','cell C2']
        ]
        output = [
            'column 1 | column 2 | column 3',
            '------------------------------',
            'cell A1  | cell A2  |         ',
            'cell B1  | cell B2  |         ',
            'cell C1  | cell C2  |         ',
        ]
        self._run_test(columns, rows, output, column_separator = ' | ', add_header_underline = True)

    def _run_test(self, columns, rows, output, column_separator = ' ', add_header_underline = False):
        table = asciitable.AsciiTable()
        table.add_header_underline = add_header_underline
        table.column_separator = column_separator
        for column in columns:
            table.add_column(column)
        for row in rows:
            table.add_row(*row)
        result = table.create_output()
        result_lines = result.split('\n')
        self.assertEqual(len(output), len(result_lines))
        for output_index in range(0, len(output)):
            self.assertEqual(output[output_index], result_lines[output_index])
