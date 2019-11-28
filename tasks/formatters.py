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
        output = '['
        output += 'description:"{}"'.format(task.name)
        output += ' uuid:"{}"'.format(task.id)
        output += ']'
        return output
