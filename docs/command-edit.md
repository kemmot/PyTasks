# Edit Command

Allows a task to be editted in an external editor.

## Usage

```bash
tasks <filter> edit
```

## Positional Arguments

|Name  |Description     |
|:-----|:---------------|
|filter|The task filter.|

Note that if the filter returns more than one task, only the first will be editted.

## Applicable Settings

* [command.edit.editor](settings.md#commandediteditor)
