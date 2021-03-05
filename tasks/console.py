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

    def input(self, prompt):
        return input(prompt)

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
