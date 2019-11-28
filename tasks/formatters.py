'''
A module containing task formatter classes.
'''

class TaskWarriorFormatter:
    '''
    A formatter matching task warriors internal file format.
    '''
    def format(self, task):
        '''
        Formats the task.
        '''
        output = '[description:"{}"]'.format(task.name)
        return output
