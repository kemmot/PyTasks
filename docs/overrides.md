# Overrides

Settings can be overriden on the command line by using a post verb property setter that starts with 'rc.'.

The following example shows how to override a default setting value to suppress a confirmation prompt.

```bash
tasks 1 start rc.command.start.confirm:false
```

Shortcuts are available for reports so that the fully qualified report setting name doesn't have to be typed.
The following example shows how to override the default sort value for the current report.

```bash
tasks list rc.sort:project
```
