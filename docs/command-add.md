# Add Command

Adds a task.

## Usage

```bash
tasks add <name> [name ...] [attribute:value ...]
```

## Positional Arguments

|Name     |Description|
|:--------|:----------|
|attribute|Any number of optional attribute key value pairs.|
|name     |The name of the new item.|

Note: multiple names are concatenated together with spaces.

## Applicable Settings

* [command.add.format](settings.md#commandaddformat)
* [command.add.next_key_id](settings.md#commandaddnext_key_id)

## Examples

Example 1: add a task.

```bash
tasks add This is a new task
```
