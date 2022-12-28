# Done Command

Marks a task as complete.

## Usage

```bash
tasks <filter> done <comment> [comment ...]
```

## Positional Arguments

|Name   |Description|
|:------|:----------|
|comment|The annotation comment to add to the tasks.|
|filter |The task filter.|

Note: multiple comments are concatenated together with spaces.

## Applicable Settings

* [command.done.confirm](settings.md#commanddoneconfirm)
