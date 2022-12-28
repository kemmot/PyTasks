# Annotate Command

Adds an annotation comment to a task.

## Usage

```bash
tasks <filter> annotate <comment> [comment ...] [attribute:value ...]
```

## Positional Arguments

|Name     |Description|
|:--------|:----------|
|filter   |The filter that identifies the task or tasks to apply the change to.|
|comment  |The annotation comment to add to the tasks.|
|attribute|Attribute key value pairs.|

Note: multiple comments are concatenated together with spaces.

## Supported Attributes

Note that these are annotation attributes rather than task attributes.
The following values are supported.

|Name   |Description|
|:------|:----------|
|created|The date to use for the annotation creation date.  If not provided then the current date and time is used.|

## Applicable Settings

* [command.annotate.confirm](settings.md#commandannotateconfirm)

## Examples

Example 1: add an annotation to task 4.

```bash
tasks 4 annotate this is a multi-word annotation
```
