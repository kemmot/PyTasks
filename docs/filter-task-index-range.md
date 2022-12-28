# Task Index Range Filter

A numeric range filter will be recognised as a task index filter and will match
the index of a task in the range reported by the list command.

## Examples

Example 1: complete tasks 3, 4 and 5.

```bash
task 3-5 done
```

Example 2: list all tasks with an index higher than 7.

```bash
task 7- list
```

Example 3: start all tasks with an index less than 5.

```bash
task -5 start
```

Example 3: stop a collection of ranges of tasks.

```bash
task 1,3-5,7- stop
```
