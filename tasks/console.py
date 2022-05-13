import enum
import os
import sys

import rich.console
import rich.table


class ConsoleColours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    FOREGROUND_BLACK = '\33[30m'
    FOREGROUND_RED = '\33[31m'
    FOREGROUND_GREEN = '\33[32m'
    FOREGROUND_YELLOW = '\33[33m'
    FOREGROUND_BLUE = '\33[34m'
    FOREGROUND_PURPLE = '\33[35m'
    FOREGROUND_BEIGE = '\33[36m'
    FOREGROUND_WHITE = '\33[37m'

    BACKGROUND_BLACK = '\33[40m'
    BACKGROUND_RED = '\33[41m'
    BACKGROUND_GREEN = '\33[42m'
    BACKGROUND_YELLOW = '\33[43m'
    BACKGROUND_BLUE = '\33[44m'
    BACKGROUND_PURPLE = '\33[45m'
    BACKGROUND_CYAN = '\33[46m'
    BACKGROUND_WHITE = '\33[47m'


class ConsoleKeyType(enum.Enum):
    UNKNOWN = 0
    ASCII = 5
    BACKSPACE = 10
    DELETE = 15
    DOWN_ARROW = 20
    ESCAPE = 30
    LEFT_ARROW = 40
    RIGHT_ARROW = 50
    RETURN = 60
    UP_ARROW = 70


class ConsoleKey:
    def __init__(self):
        self.__key_type = ConsoleKeyType.UNKNOWN
        self.__raw_value_count = 0
        self.__raw_value_1 = -1
        self.__raw_value_2 = -1
    
    @property
    def key_type(self):
        return self.__key_type
    
    @key_type.setter
    def key_type(self, value):
        self.__key_type = value

    @property
    def raw_value_count(self):
        return self.__raw_value_count
    
    @raw_value_count.setter
    def raw_value_count(self, value):
        self.__raw_value_count = value

    @property
    def raw_value_1(self):
        return self.__raw_value_1
    
    @raw_value_1.setter
    def raw_value_1(self, value):
        self.__raw_value_1 = value

    @property
    def raw_value_2(self):
        return self.__raw_value_2
    
    @raw_value_2.setter
    def raw_value_2(self, value):
        self.__raw_value_2 = value
    
    def __str__(self):
        description = str(self.key_type)
        if self.key_type == ConsoleKeyType.UNKNOWN:
            description+= ' '
            description += str(self.raw_value_1)
            if self.raw_value_count > 1:
                description += str(self.raw_value_2)
        return description


class ConsoleFactory:
    def get_console(self):
        try:
            con = WindowsConsole()
        except ImportError:
            try:
                con = MacCarbonConsole()
            except(AttributeError, ImportError):
                con = UnixConsole()
        return con


class Console:
    def __init__(self):
        self._background_colour = ConsoleColours.BACKGROUND_BLACK
        self._foreground_colour = ConsoleColours.FOREGROUND_WHITE

    @property
    def background_colour(self):
        return self._background_colour

    @background_colour.setter
    def background_colour(self, value):
        self._background_colour = value

    @property
    def foreground_colour(self):
        return self._foreground_colour

    @foreground_colour.setter
    def foreground_colour(self, value):
        self._foreground_colour = value

    @property
    def height(self):
        return os.get_terminal_size()[1]
        
    @property
    def width(self):
        return os.get_terminal_size()[0]

    def clear(self):
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

    def input(self, prompt):
        return input(prompt)
        
    def input_key(self):
        key = ConsoleKey()
        key.raw_value_1 = self.input_key_raw()
        key.raw_value_count = 1
        
        if key.raw_value_1 == b'\x1b':
            key.key_type = ConsoleKeyType.ESCAPE
        elif key.raw_value_1 == b'\r':
            key.key_type = ConsoleKeyType.RETURN
        elif key.raw_value_1 == b'\x08':
            key.key_type = ConsoleKeyType.BACKSPACE
        elif key.raw_value_1 == b'\xe0':
            key.raw_value_2 = self.input_key_raw()
            key.raw_value_count += 1
            if key.raw_value_2 == b'S':
                key.key_type = ConsoleKeyType.DELETE
            elif key.raw_value_2 == b'K':
                key.key_type = ConsoleKeyType.LEFT_ARROW
            elif key.raw_value_2 == b'P':
                key.key_type = ConsoleKeyType.DOWN_ARROW
            elif key.raw_value_2 == b'H':
                key.key_type = ConsoleKeyType.UP_ARROW
            elif key.raw_value_2 == b'M':
                key.key_type = ConsoleKeyType.RIGHT_ARROW
            else:
                key.key_type = ConsoleKeyType.UNKNOWN
        elif key.raw_value_1.isascii():
            key.key_type = ConsoleKeyType.ASCII
        else:
            key.key_type = ConsoleKeyType.UNKNOWN
        
        return key

    def input_key_raw(self):
        raise Exception('input_key_internal method should be implemented by base class')

    def print_lines(self, lines, alt_foregound_colour=None, alt_background_colour=None):
        line_number = 0
        for line in lines:
            if line_number % 2 == 1:
                foreground_colour = alt_foregound_colour
                background_colour = alt_background_colour
            else:
                foreground_colour = None
                background_colour = None
            self.print(line, foreground_colour, background_colour)
            line_number += 1

    def print(self, text, foreground_colour=None, background_colour=None):
        output = ''
        if background_colour:
            output += background_colour
        if foreground_colour:
            output += foreground_colour
        output += text
        if foreground_colour:
            output += self._foreground_colour
        if background_colour:
            output += self._background_colour
        print(output)

    def parse_backcolour(self, description):
        upper_description = description.upper()
        if upper_description == 'BLACK':
            result = ConsoleColours.BACKGROUND_BLACK
        elif upper_description == 'RED':
            result = ConsoleColours.BACKGROUND_RED
        elif upper_description == 'GREEN':
            result = ConsoleColours.BACKGROUND_GREEN
        elif upper_description == 'YELLOW':
            result = ConsoleColours.BACKGROUND_YELLOW
        elif upper_description == 'BLUE':
            result = ConsoleColours.BACKGROUND_BLUE
        elif upper_description == 'PURPLE':
            result = ConsoleColours.BACKGROUND_PURPLE
        elif upper_description == 'CYAN':
            result = ConsoleColours.BACKGROUND_CYAN
        elif upper_description == 'WHITE':
            result = ConsoleColours.BACKGROUND_WHITE
        else:
            raise Exception('Background colour not supported: {}'.format(description))

        return result

    def parse_forecolour(self, description):
        upper_description = description.upper()
        if upper_description == 'BLACK':
            result = ConsoleColours.FOREGROUND_BLACK
        elif upper_description == 'RED':
            result = ConsoleColours.FOREGROUND_RED
        elif upper_description == 'GREEN':
            result = ConsoleColours.FOREGROUND_GREEN
        elif upper_description == 'YELLOW':
            result = ConsoleColours.FOREGROUND_YELLOW
        elif upper_description == 'BLUE':
            result = ConsoleColours.FOREGROUND_BLUE
        elif upper_description == 'PURPLE':
            result = ConsoleColours.FOREGROUND_PURPLE
        elif upper_description == 'BEIGE':
            result = ConsoleColours.FOREGROUND_BEIGE
        elif upper_description == 'WHITE':
            result = ConsoleColours.FOREGROUND_WHITE
        else:
            raise Exception('Foreground colour not supported: {}'.format(description))

        return result
    
    def print_table(self, data_table, alt_foreground_colour, alt_background_colour):
        from rich.theme import Theme
        custom_theme = Theme({
            "next_row": "light_slate_grey",
            "next_row_alt": "grey39",
            "danger": "bold red"
        })
        row_style_1 = 'next_row'
        row_style_2 = 'next_row_alt'
        #row_style_1 = rich.style.Style(color=self.foreground_colour, bgcolor=self.background_colour)
        #row_style_2 = rich.style.Style(color=alt_foreground_colour, bgcolor=alt_background_colour)
        table = rich.table.Table(show_header=True, header_style="bold", row_styles=[row_style_1, row_style_2])

        for column in data_table.columns:
            table.add_column(column)
        
        for row in data_table.rows:
            table.add_row(*row)
        
        console = rich.console.Console(theme=custom_theme)
        console.print(table)

    def set_cursor_position(self, y, x):
        print("\033[%d;%dH" % (y, x))


class MacCarbonConsole(Console):
    '''
    Contains code for reading a single key from the keyboard taken from:
    https://stackoverflow.com/questions/13207678/whats-the-simplest-way-of-detecting-keyboard-input-in-a-script-from-the-termina
    '''
    
    """
    A function which returns the current ASCII key that is down;
    if no ASCII key is down, the null string is returned.  The
    page http://www.mactech.com/macintosh-c/chap02-1.html was
    very helpful in figuring out how to do this.
    """
    def __init__(self):
        import Carbon
        Carbon.Evt #see if it has this (in Unix, it doesn't)

    def input_key_raw(self):
        import Carbon
        if Carbon.Evt.EventAvail(0x0008)[0]==0: # 0x0008 is the keyDownMask
            return ''
        else:
            #
            # The event contains the following info:
            # (what,msg,when,where,mod)=Carbon.Evt.GetNextEvent(0x0008)[1]
            #
            # The message (msg) contains the ASCII char which is
            # extracted with the 0x000000FF charCodeMask; this
            # number is converted to an ASCII character with chr() and
            # returned
            #
            (what,msg,when,where,mod)=Carbon.Evt.GetNextEvent(0x0008)[1]
            return chr(msg & 0x000000FF)


class UnixConsole(Console):
    '''
    Contains code for reading a single key from the keyboard taken from:
    https://stackoverflow.com/questions/13207678/whats-the-simplest-way-of-detecting-keyboard-input-in-a-script-from-the-termina
    '''
    def __init__(self):
        import tty, sys, termios # import termios now or else you'll get the Unix version on the Mac

    def input_key_raw(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class WindowsConsole(Console):
    '''
    Contains code for reading a single key from the keyboard taken from:
    https://stackoverflow.com/questions/13207678/whats-the-simplest-way-of-detecting-keyboard-input-in-a-script-from-the-termina
    '''
    def __init__(self):
        import msvcrt

    def input_key_raw(self):
        import msvcrt
        return msvcrt.getch()
