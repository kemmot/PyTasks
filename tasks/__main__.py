#!/usr/bin/env python3

'''
The main module for the tasks program.
'''

import logging
import logging.config
import os
import sys
import yaml

import commands.commandfactory as commandfactory
import commandline as cli
import storage

# modules used by reflection
import commands.addcommand
import commands.donecommand
import commands.listcommand


class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """Format an exception so that it prints on a single line."""
        return ''

    def format(self, record):
        result = super(OneLineExceptionFormatter, self).format(record)
        if record.exc_text:
            result = result.replace('\n', '') + '|'
        return result


def create_app_folder_log_handler( \
        maxBytes=10485760, backupCount=10, encoding='utf8', \
        filename='timesheet.log', level='DEBUG'):
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, filename)
    handler = logging.handlers.RotatingFileHandler(path)
    handler.backupCount = backupCount
    handler.encoding = encoding
    handler.level = level
    handler.maxBytes = maxBytes
    return handler


def configure_logging(filename):
    if os.path.isfile(filename):
        try:
            with open(filename) as file:
                config = yaml.safe_load(file.read())
                logging.config.dictConfig(config)
        except Exception as ex:
            raise Exception('Failed processing logging config file: %s' % (filename)) from ex
    else:
        raise Exception('Logging config file does not exist: %s' % (filename))


SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_FOLDER = os.path.dirname(SCRIPT_PATH)
LOGGING_CONFIG_PATH = os.path.join(SCRIPT_FOLDER, 'tasks.logging.yaml')
configure_logging(LOGGING_CONFIG_PATH)

LOGGER = logging.getLogger(__name__)
LOGGER.debug('\n')
LOGGER.debug('Application started')
try:
    SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))
    DATA_FILENAME = os.path.join(os.path.split(SCRIPT_FOLDER)[0], 'todo.txt')
    STORAGE = storage.TaskWarriorPendingStorage(DATA_FILENAME)
    COMMAND_FACTORY = commandfactory.CommandFactory(STORAGE)
    COMMAND_FACTORY.register_known_types()

    try:
        COMMAND = COMMAND_FACTORY.get_command(sys.argv[1:])
    except cli.ExitCodeException:
        raise
    except Exception as ex:
        EXIT_CODE = cli.ExitCodes.command_line_argument_error
        raise cli.ExitCodeException(message=str(ex), exit_code=EXIT_CODE) from ex

    COMMAND.execute()
    EXIT_CODE = cli.ExitCodes.success
except cli.ExitCodeException as ex:
    LOGGER.error(str(ex), exc_info=True)
    EXIT_CODE = ex.exit_code
except Exception as ex:
    LOGGER.error(str(ex), exc_info=True)
    EXIT_CODE = cli.ExitCodes.unknown_error

EXIT_CODE_DESCRIPTION = cli.ExitCodes.get_description(EXIT_CODE)
LOGGER.debug('Application stopped with exit code: {} ({})'.format(EXIT_CODE, EXIT_CODE_DESCRIPTION))
exit(EXIT_CODE)
