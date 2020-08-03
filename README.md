# PyTasks
A command line application for managing a task list.

-----------------------------------------------------------------------------------------------------

# Usage
The application offers multiple operations as sub commands of the application with each exposing different parameters.

The following shows the general usage of the application.
```
./tasks.sh [filter] <command> [command options]
```

The following commands are available:

* [add](#add-command)
* [annotate](#annotate-command)
* [done](#done-command)
* [help](#help-command)
* [info](#info-command)
* [list](#list-command)
* [modify](#modify-command)
* [start](#start-command)
* [stop](#stop-command)

The following additional information is available.

* See [here](#exit-codes) for exit codes.
* See [here](#filters) for filters (note that not all commands support filters).
* See [here](#settings) for settings.

-----------------------------------------------------------------------------------------------------

## Add Command
Adds a task.

### Usage
```
tasks add <name> [name ...]
```

### Positional Arguments

|Name|Description|
|:---|:----------|
|name|The name of the new item.|

Note: multiple names are concatenated together with spaces.

### Examples
Example 1: add a task.
```
tasks add This is a new task
```

-------------------------------------------------------------------------------------------------

## Annotate Command
Adds an annotation comment to a task.

### Usage
```
tasks <filter> annotate <comment> [comment ...]
```

### Positional Arguments

|Name   |Description|
|:------|:----------|
|filter |The filter that identifies the task or tasks to apply the change to.|
|comment|The annotation comment to add to the tasks.|

Note: multiple comments are concatenated together with spaces.

### Applicable Settings

* [command.annotate.confirm](#commandannotateconfirm)

### Examples
Example 1: add an annotation to task 4.
```
tasks 4 annotate this is a multi-word annotation
```

-------------------------------------------------------------------------------------------------

## Done Command
Marks a task as complete.

### Usage
```
tasks <filter> done
```

### Positional Arguments

|Name  |Description|
|:-----|:----------|
|filter|The task filter.|

### Applicable Settings

* [command.done.confirm](#commanddoneconfirm)

-----------------------------------------------------------------------------------------------------

## Help Command
Lists usage of available commands.

### Usage
```
tasks help
```

-----------------------------------------------------------------------------------------------------

## Info Command
Displays all information for a task or tasks.

### Usage
```
tasks [filter] info
```

-----------------------------------------------------------------------------------------------------

## List Command
Lists existing tasks.

### Usage
```
tasks [filter] list
```

### Positional Arguments

|Name  |Description|
|:-----|:----------|
|filter|The optional task filter.|

-----------------------------------------------------------------------------------------------------

## Modify Command
Modifies an existing command.

### Usage
```
tasks <filter> modify <name> [name ...] [attribute:value ...]
```

### Positional Arguments

|Name     |Description|
|:--------|:----------|
|attribute|Any number of optional attribute key value pairs.|
|filter   |The optional task filter.|
|name     |The new name of the item.|

### Applicable Settings

* [command.modify.confirm](#commandmodifyconfirm)

-----------------------------------------------------------------------------------------------------

## Start Command
Sets the start time of existing tasks.

### Usage
```
tasks <filter> start
```

### Positional Arguments

|Name     |Description|
|:--------|:----------|
|filter   |The optional task filter.|

### Applicable Settings

* [command.start.confirm](#commandstartconfirm)

-----------------------------------------------------------------------------------------------------

## Stop Command
Clears the start time of existing tasks.

### Usage
```
tasks <filter> stop
```

### Positional Arguments

|Name     |Description|
|:--------|:----------|
|filter   |The optional task filter.|

### Applicable Settings

* [command.stop.confirm](#commandstopconfirm)

-----------------------------------------------------------------------------------------------------

# Exit Codes
The following is a description of the exit codes that the application can produce.

|Code|Description|
|---:|:----------|
|   0|Command executed successfully.|
|   1|Command line argument error.  |
|   2|No command specified.         |
|   3|Unknown command.              |
|  99|Unknown error.                |

-----------------------------------------------------------------------------------------------------

# Filters
The following filters are available.

-----------------------------------------------------------------------------------------------------

## Task Index Filter
A numeric filter will be recognised as a task index filter and will match
the index of a task reported by the list command.

### Examples
Example 1: complete task 3.
```
task 3 done
```

-----------------------------------------------------------------------------------------------------

## Task Name Filter
A non-numeric filter will be recognised as a task name filter and will match
any tasks who's name contains the text.  Tested without case sensitivity.

If the filter text is surrounded by forward slashes, they will be ignored but 
allows filtering on either a number in the name or a word that could be identified
as a command name.

### Examples
Example 1: list any tasks containing the word 'project'.
```
tasks project list
```

Example 2: list tasks with '14' in the name.
(note the slashes to ensure that task index 14 isn't listed)
```
tasks /14/ list
```

Example 3: list tasks with 'add' in the name
(note the slashes to ensure that a task called 'list' isn't added).
```
tasks /add/ list
```

-----------------------------------------------------------------------------------------------------

# Settings

## command.annotate.confirm
Whether the annotate command should request confirmation before making changes.

Possible values

* False
* True

Default value: True

## command.default
If no parameters are specified then these will be used.

Possible values are any valid parameter set.

Default value: list

## command.done.confirm
Whether the done command should request confirmation before making changes.

Possible values

* False
* True

Default value: True

## command.modify.confirm
Whether the modify command should request confirmation before making changes.

Possible values

* False
* True

Default value: True

## command.start.confirm
Whether the start command should request confirmation before making changes.

Possible values

* False
* True

Default value: True

## command.stop.confirm
Whether the stop command should request confirmation before making changes.

Possible values

* False
* True

Default value: True

## data.location
The folder to use when looking for data files.

Default value: ..

## data.done.filename
The filename to use for done tasks.  Appended to data.location.

Default value: done.txt

## data.pending.filename
The filename to use for in-progress tasks.  Appended to data.location.

Default value: todo.txt
