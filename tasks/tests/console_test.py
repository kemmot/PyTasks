import unittest
from unittest import mock
from unittest.mock import patch

import console


class ConsoleTests(unittest.TestCase):
    def test_constructor_succeeds(self):
        test_console = console.Console()
        self.assertEqual(test_console.background_colour, console.ConsoleColours.BACKGROUND_BLACK)
        self.assertEqual(test_console.foreground_colour, console.ConsoleColours.FOREGROUND_WHITE)

    def test_background_colour_setter_succeeds(self):
        test_console = console.Console()
        self.assertEqual(test_console.background_colour, console.ConsoleColours.BACKGROUND_BLACK)
        test_console.background_colour = console.ConsoleColours.BACKGROUND_YELLOW
        self.assertEqual(test_console.background_colour, console.ConsoleColours.BACKGROUND_YELLOW)

    def test_foreground_colour_setter_succeeds(self):
        test_console = console.Console()
        self.assertEqual(test_console.foreground_colour, console.ConsoleColours.FOREGROUND_WHITE)
        test_console.foreground_colour = console.ConsoleColours.FOREGROUND_GREEN
        self.assertEqual(test_console.foreground_colour, console.ConsoleColours.FOREGROUND_GREEN)

    @patch('console.input', return_value='yes')
    def test_input(self, mock_input):
        self.assertEqual(console.Console().input('this is the prompt'), 'yes')
        mock_input.assert_called_once_with('this is the prompt')

    @patch('console.print')
    def test_print_lines(self, mock_print):
        lines = []
        lines.append('line 1')
        lines.append('line 2')
        lines.append('line 3')
        lines.append('line 4')
        alt_prefix = '\33[41m\33[32m'
        alt_suffix = '\33[34m\33[46m'
        test_console = console.Console()
        test_console.background_colour = console.ConsoleColours.BACKGROUND_CYAN
        test_console.foreground_colour = console.ConsoleColours.FOREGROUND_BLUE
        test_console.print_lines(lines, \
            alt_background_colour=console.ConsoleColours.BACKGROUND_RED, \
            alt_foregound_colour=console.ConsoleColours.FOREGROUND_GREEN)
        expected_calls = [
            mock.call('line 1'),
            mock.call(alt_prefix + 'line 2' + alt_suffix),
            mock.call('line 3'),
            mock.call(alt_prefix + 'line 4' + alt_suffix)
            ]
        self.assertEqual(expected_calls, mock_print.mock_calls)

    @patch('console.print')
    def test_print_without_colours(self, mock_print):
        console.Console().print('uncoloured output')
        mock_print.assert_called_once_with('uncoloured output')

    @patch('console.print')
    def test_print_with_foreground_colour(self, mock_print):
        test_console = console.Console()
        test_console.foreground_colour = console.ConsoleColours.FOREGROUND_BEIGE
        test_console.print('purple text output', foreground_colour=console.ConsoleColours.FOREGROUND_PURPLE)
        mock_print.assert_called_once_with('\33[35mpurple text output\33[36m')

    @patch('console.print')
    def test_print_with_background_colour(self, mock_print):
        test_console = console.Console()
        test_console.background_colour = console.ConsoleColours.BACKGROUND_RED
        test_console.print('green backed output', background_colour=console.ConsoleColours.BACKGROUND_GREEN)
        mock_print.assert_called_once_with('\33[42mgreen backed output\33[41m')

    @patch('console.print')
    def test_print_with_foreground_and_background_colour(self, mock_print):
        test_console = console.Console()
        test_console.background_colour = console.ConsoleColours.BACKGROUND_BLUE
        test_console.foreground_colour = console.ConsoleColours.FOREGROUND_YELLOW
        test_console.print('this is the output', \
            background_colour=console.ConsoleColours.BACKGROUND_YELLOW, \
            foreground_colour=console.ConsoleColours.FOREGROUND_BLUE)
        mock_print.assert_called_once_with('\33[43m\33[34mthis is the output\33[33m\33[44m')

    def test_parse_backcolour(self):
        mappings = {
            # lower case
            'black': console.ConsoleColours.BACKGROUND_BLACK,
            'red': console.ConsoleColours.BACKGROUND_RED,
            'green': console.ConsoleColours.BACKGROUND_GREEN,
            'yellow': console.ConsoleColours.BACKGROUND_YELLOW,
            'blue': console.ConsoleColours.BACKGROUND_BLUE,
            'purple': console.ConsoleColours.BACKGROUND_PURPLE,
            'cyan': console.ConsoleColours.BACKGROUND_CYAN,
            'white': console.ConsoleColours.BACKGROUND_WHITE,
            # upper case
            'BLACK': console.ConsoleColours.BACKGROUND_BLACK,
            'RED': console.ConsoleColours.BACKGROUND_RED,
            'GREEN': console.ConsoleColours.BACKGROUND_GREEN,
            'YELLOW': console.ConsoleColours.BACKGROUND_YELLOW,
            'BLUE': console.ConsoleColours.BACKGROUND_BLUE,
            'PURPLE': console.ConsoleColours.BACKGROUND_PURPLE,
            'CYAN': console.ConsoleColours.BACKGROUND_CYAN,
            'WHITE': console.ConsoleColours.BACKGROUND_WHITE,
            # mixed case
            'BlacK': console.ConsoleColours.BACKGROUND_BLACK,
            'Red': console.ConsoleColours.BACKGROUND_RED,
            'gReeN': console.ConsoleColours.BACKGROUND_GREEN,
            'YellOW': console.ConsoleColours.BACKGROUND_YELLOW,
            'blUe': console.ConsoleColours.BACKGROUND_BLUE,
            'purplE': console.ConsoleColours.BACKGROUND_PURPLE,
            'CyAn': console.ConsoleColours.BACKGROUND_CYAN,
            'wHITe': console.ConsoleColours.BACKGROUND_WHITE,
        }
        for key in mappings:
            result = console.Console().parse_backcolour(key)
            self.assertEqual(mappings[key], result)

    def test_parse_backcolour_invalid_input(self):
        with self.assertRaises(Exception):
            console.Console().parse_backcolour('not a colour')

    def test_parse_forecolour(self):
        mappings = {
            # lower case
            'black': console.ConsoleColours.FOREGROUND_BLACK,
            'red': console.ConsoleColours.FOREGROUND_RED,
            'green': console.ConsoleColours.FOREGROUND_GREEN,
            'yellow': console.ConsoleColours.FOREGROUND_YELLOW,
            'blue': console.ConsoleColours.FOREGROUND_BLUE,
            'purple': console.ConsoleColours.FOREGROUND_PURPLE,
            'beige': console.ConsoleColours.FOREGROUND_BEIGE,
            'white': console.ConsoleColours.FOREGROUND_WHITE,
            # upper case
            'BLACK': console.ConsoleColours.FOREGROUND_BLACK,
            'RED': console.ConsoleColours.FOREGROUND_RED,
            'GREEN': console.ConsoleColours.FOREGROUND_GREEN,
            'YELLOW': console.ConsoleColours.FOREGROUND_YELLOW,
            'BLUE': console.ConsoleColours.FOREGROUND_BLUE,
            'PURPLE': console.ConsoleColours.FOREGROUND_PURPLE,
            'BEIGE': console.ConsoleColours.FOREGROUND_BEIGE,
            'WHITE': console.ConsoleColours.FOREGROUND_WHITE,
            # mixed case
            'BlacK': console.ConsoleColours.FOREGROUND_BLACK,
            'Red': console.ConsoleColours.FOREGROUND_RED,
            'gReeN': console.ConsoleColours.FOREGROUND_GREEN,
            'YellOW': console.ConsoleColours.FOREGROUND_YELLOW,
            'blUe': console.ConsoleColours.FOREGROUND_BLUE,
            'purplE': console.ConsoleColours.FOREGROUND_PURPLE,
            'BeiGe': console.ConsoleColours.FOREGROUND_BEIGE,
            'wHITe': console.ConsoleColours.FOREGROUND_WHITE,
        }
        for key in mappings:
            result = console.Console().parse_forecolour(key)
            self.assertEqual(mappings[key], result)

    def test_parse_forecolour_invalid_input(self):
        with self.assertRaises(Exception):
            console.Console().parse_forecolour('not a colour')
