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
* [columns](#columns-command)
* [done](#done-command)
* [help](#help-command)
* [info](#info-command)
* [list](#list-command)
* [modify](#modify-command)
* [shell](#shell-command)
* [start](#start-command)
* [stop](#stop-command)

The following additional information is available.

* See [here](#exit-codes) for exit codes.
* See [here](#filters) for filters (note that not all commands support filters).
* See [here](#settings) for settings.
* See [here](#supported-columns) for supported columns.

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

### Applicable Settings

* [command.add.format](#commandaddformat)
* [command.add.next_key_id](#commandaddnext_key_id)

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
tasks <filter> annotate <comment> [comment ...] [attribute:value ...]
```

### Positional Arguments

|Name     |Description|
|:--------|:----------|
|filter   |The filter that identifies the task or tasks to apply the change to.|
|comment  |The annotation comment to add to the tasks.|
|attribute|Attribute key value pairs.|

Note: multiple comments are concatenated together with spaces.

### Supported Attributes
Note that these are annotation attributes rather than task attributes.
The following values are supported.

|Name   |Description|
|:------|:----------|
|created|The date to use for the annotation creation date.  If not provided then the current date and time is used.|

### Applicable Settings

* [command.annotate.confirm](#commandannotateconfirm)

### Examples
Example 1: add an annotation to task 4.
```
tasks 4 annotate this is a multi-word annotation
```

-------------------------------------------------------------------------------------------------

## Columns Command
Lists the columns available to display including custom task attributes.

### Usage
```
tasks <filter> columns
```
### Positional Arguments

|Name  |Description|
|:-----|:----------|
|filter|The task filter.|

Note that the filter argument filters the tasks that are examined for custom attributes rather than being based on the names of the columns.

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

### Applicable Settings

* [table.column.separator](#tablecolumnseparator)
* [table.header.underline](#tableheaderunderline)
* [table.row.alt_backcolour](#tablerowalt_backcolour)
* [table.row.alt_forecolour](#tablerowalt_forecolour)
* [table.row.backcolour](#tablerowbackcolour)
* [table.row.forecolour](#tablerowforecolour)


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

## Shell Command
Enters an interactive prompt allowing for multiple commands to be entered without being prefixed with
the application name.

### Usage
```
tasks shell
```

### Positional Arguments
None.

### Applicable Settings
None.

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
|   4|Configuration error           |
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

## Task Index Range Filter
A numeric range filter will be recognised as a task index filter and will match
the index of a task in the range reported by the list command.

### Examples
Example 1: complete tasks 3, 4 and 5.
```
task 3-5 done
```

Example 2: list all tasks with an index higher than 7.
```
task 7- list
```

Example 3: start all tasks with an index less than 5.
```
task -5 start
```

Example 3: stop a collection of ranges of tasks.
```
task 1,3-5,7- stop
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

## command.add.format
The format of the name of the text.

The following substitution properties are available:
* key_id: an auto incrementing ID stored in the command.add.next_key_id setting.
* name: the name entered.

The following example will prefix the name with an incrementing key ID.
```
FEAT-{key_id:04}: {name}
```

## command.add.next_key_id
An auto incrementing key ID for use with the command.add.format setting.

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

## report.list.columns
The comma delimited list of columns to show when displaying the list report.

Default value: id,status,description

See [supported columns](#supported-columns) for the columns available in this setting.

## table.column.separator
The string to use to separate columns when printing tables.  Any double quotes will be stripped to allow leading and trailing spaces.

Default value: " | "

## table.header.underline
Whether to underline table headers to separate them from the rows.

Default value: True

## table.row.alt_backcolour
The background colour of alternating table rows.
See [background colours](#supported-background-colours) for options.

Default value: Black

## table.row.alt_forecolour
The foreground colour of alternating table rows.
See [foreground colours](#supported-foreground-colours) for options.

Default value: White

## table.row.backcolour
The background colour of table rows.
See [background colours](#supported-background-colours) for options.

Default value: Black

## table.row.forecolour
The foreground colour of table rows.
See [foreground colours](#supported-foreground-colours) for options.

Default value: White

# Supported Columns
The following columns are supported:

|Name       |Description                        |
|----------:|:----------------------------------|
|description|The description of the task.       |
|id         |The index ID of the task.          |
|start      |The time that the task was started.|
|status     |The current task status.           |
|wait       |The target wait time for the task. |

# Supported Date Formats

|Name    |Example   |
|--------|----------|
|iso     |2021-04-17|
|relative|-4d       |

Relative date formats consist of a direction, value and unit.
The direction can be '+' for a future date from now or '-' for a past date.
The value can be any numeric value.
The unit can be one of the following:
* d: days.

# Supported Colours

## Supported Foreground Colours
The following colours are supported as foreground colours.

* Beige
* Black
* Blue
* Purple
* Green
* Red
* White
* Yellow

## Supported Background Colours
The following colours are supported as background colours.

* Black
* Blue
* Cyan
* Green
* Purple
* Red
* White
* Yellow
