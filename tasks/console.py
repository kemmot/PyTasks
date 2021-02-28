class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'


class Console:
    def __init__(self):
        self._background_colour = bcolors.CBLACK
        self._foreground_colour = bcolors.CWHITE
    
    def input(self, prompt):
        return input(prompt)
    
    def print_lines(self, lines, alt_foregound_colour=None):
        line_number = 0
        for line in lines:
            if line_number % 2 == 1:
                foreground_colour = alt_foregound_colour
            else:
                foreground_colour = None
            self.print(line, foreground_colour)
            line_number += 1

    def print(self, text, foreground_colour=None):
        output = ''
        if foreground_colour:
            output += foreground_colour
        output += text
        if foreground_colour:
            output += self._foreground_colour
        print(output)
