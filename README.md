# PyTasks
A command line application for managing a task list.

-----------------------------------------------------------------------------------------------------

# Usage
The application offers multiple operations as sub commands of the application with each exposing different parameters.

The following shows the general usage of the application.

```
./tasks.sh <command> [command options]
```

The following commands are available:

* [add](#add-command)
* [done](#done-command)
* [list](#list-command)

To display command help, the following can be used.
```
./tasks.sh -h
./tasks.sh --help
```

* See [here](#exit-codes) for exit codes.

-----------------------------------------------------------------------------------------------------

## Add Command
Adds a task.

```
usage: tasks add [-h] name [name ...]
```

Positional arguments:

|Name|Description|
|:---|:----------|
|name|The name of the new item.|

Optional arguments:

|Name      |Description|
|:---------|:----------|
|-h, --help|Show help message and exit.|

-------------------------------------------------------------------------------------------------

## Done Command
Marks a task as complete.

```
usage: tasks done [-h] filter
```

positional arguments:

|Name  |Description|
|:-----|:----------|
|filter|The task filter.|

Optional arguments:

|Name      |Description|
|:---------|:----------|
|-h, --help|Show help message and exit.|

-----------------------------------------------------------------------------------------------------

## List Command
Lists existing tasks.

```
usage: tasks list [-h]
```

Optional arguments:

|Name      |Description|
|:---------|:----------|
|-h, --help|Show help message and exit.|

-----------------------------------------------------------------------------------------------------

# Exit Codes
The following is a description of the exit codes that the application can produce.

|Code|Description|
|---:|:----------|
|   0|Command executed successfully.|
|  99|Unknown error.                |
