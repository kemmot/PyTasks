#!/usr/bin/env python3

'''
The main module for the tasks program.
'''

import logging
import logging.config
import os
import sys
import yaml

import commandfactory
import commandline as cli
import storage

# modules used by reflection
import commands.addcommand
import commands.donecommand


class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """Format an exception so that it prints on a single line."""
        return ''

    def format(self, record):
        result = super(OneLineExceptionFormatter, self).format(record)
        if record.exc_text:
            result = result.replace('\n', '') + '|'
        return result


def create_app_folder_log_handler(maxBytes=10485760, backupCount=10, encoding='utf8', filename='timesheet.log', level='DEBUG'):
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, filename)
    handler = logging.handlers.RotatingFileHandler(path)
    handler.backupCount = backupCount
    handler.encoding = encoding
    handler.level = level
    handler.maxBytes = maxBytes
    return handler


def configureLogging(filename):
    if (os.path.isfile(filename)):
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
configureLogging(LOGGING_CONFIG_PATH)

logger = logging.getLogger(__name__)
logger.debug('\n')
logger.debug('Application started')
try:
    DATA_FILENAME = os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0], 'todo.txt')
    STORAGE = storage.TaskWarriorPendingStorage(DATA_FILENAME)
    COMMAND_FACTORY = commandfactory.CommandFactory(STORAGE)
    COMMAND_FACTORY.register_known_parsers()

    try:
        ARGS = cli.CommandLineParser().parse(sys.argv[1:])
        COMMAND = COMMAND_FACTORY.get_command(ARGS)
    except Exception as ex:
        raise cli.ExitCodeException(str(ex), cli.ExitCodes.command_line_argument_error) from ex

    COMMAND.execute()
    exit_code = cli.ExitCodes.success
except cli.ExitCodeException as ex:
    logger.error(str(ex), exc_info=True)
    exit_code = ex.exit_code
except Exception as ex:
    logger.error(str(ex), exc_info=True)
    exit_code = cli.ExitCodes.unknown_error

exit_code_description = cli.ExitCodes.get_description(exit_code)
logger.debug('Application stopped with exit code: {} ({})'.format(exit_code, exit_code_description))
exit(exit_code)