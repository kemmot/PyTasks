# Task Attribute Filter

A filter containing a colon (:) will be recognised as an attribute filter and will match tasks that have the matching attribute value.

## Examples

Example 1: list tasks with the 'personal' project attribute.

```bash
task project:personal list
```

Example 2: modify all tasks without a priority.

```bash
task priority: modify wait:+10d
```
