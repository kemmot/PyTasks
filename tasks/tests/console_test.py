import unittest
from unittest import mock
from unittest.mock import MagicMock
from unittest.mock import patch

import console


class ConsoleTests(unittest.TestCase):
    def test_constructor_succeeds(self):
        c = console.Console()
        self.assertEqual(c.background_colour, console.bcolors.BACKGROUND_BLACK)
        self.assertEqual(c.foreground_colour, console.bcolors.FOREGROUND_WHITE)

    def test_background_colour_setter_succeeds(self):
        c = console.Console()
        self.assertEqual(c.background_colour, console.bcolors.BACKGROUND_BLACK)
        c.background_colour = console.bcolors.BACKGROUND_YELLOW
        self.assertEqual(c.background_colour, console.bcolors.BACKGROUND_YELLOW)

    def test_foreground_colour_setter_succeeds(self):
        c = console.Console()
        self.assertEqual(c.foreground_colour, console.bcolors.FOREGROUND_WHITE)
        c.foreground_colour = console.bcolors.FOREGROUND_GREEN
        self.assertEqual(c.foreground_colour, console.bcolors.FOREGROUND_GREEN)

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
        c = console.Console()
        c.background_colour = console.bcolors.BACKGROUND_CYAN
        c.foreground_colour = console.bcolors.FOREGROUND_BLUE
        c.print_lines(lines, \
            alt_background_colour=console.bcolors.BACKGROUND_RED, \
            alt_foregound_colour=console.bcolors.FOREGROUND_GREEN)
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
        c = console.Console()
        c.foreground_colour = console.bcolors.FOREGROUND_BEIGE
        c.print('purple text output', foreground_colour=console.bcolors.FOREGROUND_PURPLE)
        mock_print.assert_called_once_with('\33[35mpurple text output\33[36m')

    @patch('console.print')
    def test_print_with_background_colour(self, mock_print):
        c = console.Console()
        c.background_colour = console.bcolors.BACKGROUND_RED
        c.print('green backed output', background_colour=console.bcolors.BACKGROUND_GREEN)
        mock_print.assert_called_once_with('\33[42mgreen backed output\33[41m')

    @patch('console.print')
    def test_print_with_foreground_and_background_colour(self, mock_print):
        c = console.Console()
        c.background_colour = console.bcolors.BACKGROUND_BLUE
        c.foreground_colour = console.bcolors.FOREGROUND_YELLOW
        c.print('this is the output', \
            background_colour=console.bcolors.BACKGROUND_YELLOW, \
            foreground_colour=console.bcolors.FOREGROUND_BLUE)
        mock_print.assert_called_once_with('\33[43m\33[34mthis is the output\33[33m\33[44m')

    def test_parse_backcolour(self):
        mappings = {
            # lower case
            'black': console.bcolors.BACKGROUND_BLACK,
            'red': console.bcolors.BACKGROUND_RED,
            'green': console.bcolors.BACKGROUND_GREEN,
            'yellow': console.bcolors.BACKGROUND_YELLOW,
            'blue': console.bcolors.BACKGROUND_BLUE,
            'purple': console.bcolors.BACKGROUND_PURPLE,
            'cyan': console.bcolors.BACKGROUND_CYAN,
            'white': console.bcolors.BACKGROUND_WHITE,
            # upper case
            'BLACK': console.bcolors.BACKGROUND_BLACK,
            'RED': console.bcolors.BACKGROUND_RED,
            'GREEN': console.bcolors.BACKGROUND_GREEN,
            'YELLOW': console.bcolors.BACKGROUND_YELLOW,
            'BLUE': console.bcolors.BACKGROUND_BLUE,
            'PURPLE': console.bcolors.BACKGROUND_PURPLE,
            'CYAN': console.bcolors.BACKGROUND_CYAN,
            'WHITE': console.bcolors.BACKGROUND_WHITE,
            # mixed case
            'BlacK': console.bcolors.BACKGROUND_BLACK,
            'Red': console.bcolors.BACKGROUND_RED,
            'gReeN': console.bcolors.BACKGROUND_GREEN,
            'YellOW': console.bcolors.BACKGROUND_YELLOW,
            'blUe': console.bcolors.BACKGROUND_BLUE,
            'purplE': console.bcolors.BACKGROUND_PURPLE,
            'CyAn': console.bcolors.BACKGROUND_CYAN,
            'wHITe': console.bcolors.BACKGROUND_WHITE,
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
            'black': console.bcolors.FOREGROUND_BLACK,
            'red': console.bcolors.FOREGROUND_RED,
            'green': console.bcolors.FOREGROUND_GREEN,
            'yellow': console.bcolors.FOREGROUND_YELLOW,
            'blue': console.bcolors.FOREGROUND_BLUE,
            'purple': console.bcolors.FOREGROUND_PURPLE,
            'beige': console.bcolors.FOREGROUND_BEIGE,
            'white': console.bcolors.FOREGROUND_WHITE,
            # upper case
            'BLACK': console.bcolors.FOREGROUND_BLACK,
            'RED': console.bcolors.FOREGROUND_RED,
            'GREEN': console.bcolors.FOREGROUND_GREEN,
            'YELLOW': console.bcolors.FOREGROUND_YELLOW,
            'BLUE': console.bcolors.FOREGROUND_BLUE,
            'PURPLE': console.bcolors.FOREGROUND_PURPLE,
            'BEIGE': console.bcolors.FOREGROUND_BEIGE,
            'WHITE': console.bcolors.FOREGROUND_WHITE,
            # mixed case
            'BlacK': console.bcolors.FOREGROUND_BLACK,
            'Red': console.bcolors.FOREGROUND_RED,
            'gReeN': console.bcolors.FOREGROUND_GREEN,
            'YellOW': console.bcolors.FOREGROUND_YELLOW,
            'blUe': console.bcolors.FOREGROUND_BLUE,
            'purplE': console.bcolors.FOREGROUND_PURPLE,
            'BeiGe': console.bcolors.FOREGROUND_BEIGE,
            'wHITe': console.bcolors.FOREGROUND_WHITE,
        }
        for key in mappings:
            result = console.Console().parse_forecolour(key)
            self.assertEqual(mappings[key], result)

    def test_parse_forecolour_invalid_input(self):
        with self.assertRaises(Exception):
            console.Console().parse_forecolour('not a colour')
