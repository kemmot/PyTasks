from tkinter import *
import tkinter as ttk

import commands.commandbase as commandbase


class GuiCommand(commandbase.CommandBase):
    '''
    A command that will display command help.
    '''
    def execute(self):
        window = ttk.Tk()
        tv = ttk.Treeview(window, columns=(1, 2, 3), show='headings', height=8)
        tv.pack()

        tv.heading(1, text="name")
        tv.heading(2, text="eid")
        tv.heading(3, text="Salary")

        tv.insert(parent='', index=0, iid=0, values=("vineet", "e11", 1000000.00))
        Button(window, text='Refresh').pack()

        style = ttk.Style()
        style.theme_use("default")
        style.map("Treeview")

        #greeting = ttk.Label(text="Hello, Tkinter")
        #greeting.pack()
        window.mainloop()


class GuiCommandParser(commandbase.CommandParserBase):
    COMMAND_NAME = 'gui'

    def __init__(self):
        super().__init__(GuiCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return GuiCommand(context)
