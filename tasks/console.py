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

    def print(self, text, colour=None):
        output = ''
        if colour:
            output += colour
        output += text
        if colour:
            output += self._foreground_colour
        print(output)
