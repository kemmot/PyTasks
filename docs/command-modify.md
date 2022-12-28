# Modify Command

Modifies an existing command.

## Usage

```bash
tasks <filter> modify <name> [name ...] [attribute:value ...] [+tag_to_add ...] [-tag_to_remove ...]
```

## Positional Arguments

|Name     |Description                                      |
|:--------|:------------------------------------------------|
|attribute|Any number of optional attribute key value pairs.|
|filter   |The optional task filter.                        |
|name     |The new name of the item.                        |

To remove dependencies, list them as negative numbers.

## Applicable Settings

* [command.modify.confirm](settings.md#commandmodifyconfirm)
* [command.modify.summary](settings.md#commandmodifysummary)

## Examples

Example 1: add 'new' tag and remove 'old' tag from task 1.

```bash
task 1 modify +new -old
```

Example 2: modify task 10 to add 3 as a dependant task and remove 5 as a dependant task.

```bash
task 10 modfy depends:3,-5
```
