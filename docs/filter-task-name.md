# Task Name Filter

A non-numeric filter will be recognised as a task name filter and will match
any tasks who's name contains the text.  Tested without case sensitivity.

If the filter text is surrounded by forward slashes, they will be ignored but 
allows filtering on either a number in the name or a word that could be identified
as a command name.

## Examples

Example 1: list any tasks containing the word 'project'.

```bash
tasks project list
```

Example 2: list tasks with '14' in the name.
(note the slashes to ensure that task index 14 isn't listed)

```bash
tasks /14/ list
```

Example 3: list tasks with 'add' in the name
(note the slashes to ensure that a task called 'list' isn't added).

```bash
tasks /add/ list
```
