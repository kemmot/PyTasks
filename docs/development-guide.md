# Development Guide

## Adding new commands

To add a new command, the following tasks should be completed:

- Add the command and parser to tasks/commands/<command name>command.py
- Reference the new command file in tasks/__main__.py
- Add tests to tasks/tests/<command name>command_test.py
- Document the command usage in docs/command-<command name>.md

## Adding config for a command

To add configuration for a new or existing command, the following tasks should
be completed:

- Add the setting name to the SettingNames class.
- Add a property for the setting in the SettingsFacade class.
- Add a default value for the setting in the DefaultSettingsProvider class.
- Add tests for the above in settings_tests.py.
- Add usage tests for the new setting whereever appropriate.
- Add usage documentation for the setting in docs/settings.md.
- Reference the setting documentation from whereever it is used.

## Adding setting override shortcuts

For reports these should be done in the _expand_overrides method of
commandfactory.py.  The reason for this is that's where the config for custom
reports is expanded into the different report commands.


Usage for overrides can be found [here](overrides.md)
