# Add Command
Adds a task.

## Usage
```
tasks add <name> [name ...] [attribute:value ...]
```

## Positional Arguments

|Name     |Description|
|:--------|:----------|
|attribute|Any number of optional attribute key value pairs.|
|name     |The name of the new item.|

Note: multiple names are concatenated together with spaces.

## Applicable Settings

* [command.add.format](#commandaddformat)
* [command.add.next_key_id](#commandaddnext_key_id)

## Examples
Example 1: add a task.
```
tasks add This is a new task
```