# Settings

The following settings are available:

* [command.add.format](#commandaddformat)
* [command.add.next_key_id](#commandaddnext_key_id)
* [command.annotate.confirm](#commandannotateconfirm)
* [command.default](#commanddefault)
* [command.done.confirm](#commanddoneconfirm)
* [command.edit.editor](#commandediteditor)
* [command.modify.confirm](#commandmodifyconfirm)
* [command.modify.summary](#commandmodifysummary)
* [command.start.confirm](#commandstartconfirm)
* [command.stop.confirm](#commandstopconfirm)
* [context](#context)
* [data.location](#datalocation)
* [data.done.filename](#datadonefilename)
* [data.pending.filename](#datapendingfilename)
* [report.list.columns](#reportlistcolumns)
* [report.list.max_annotation_count](#reportlistmax_annotation_count)
* [report.next.columns](#reportnextcolumns)
* [report.next.max_annotation_count](#reportnextmax_annotation_count)
* [table.column.separator](#tablecolumnseparator)
* [table.header.underline](#tableheaderunderline)
* [table.row.alt_backcolour](#tablerowalt_backcolour)
* [table.row.alt_forecolour](#tablerowalt_forecolour)
* [table.row.backcolour](#tablerowbackcolour)
* [table.row.forecolour](#tablerowforecolour)

## command.add.format

The format of the name of the text.

The following substitution properties are available:

* key_id: an auto incrementing ID stored in the command.add.next_key_id setting.
* name: the name entered.

The following example will prefix the name with an incrementing key ID.

```text
FEAT-{key_id:04}: {name}
```

## command.add.next_key_id

An auto incrementing key ID for use with the command.add.format setting.

## command.annotate.confirm

Whether the annotate command should request confirmation before making changes.

Possible values

* False
* True

Default value: True

## command.default

If no parameters are specified then these will be used.

Possible values are any valid parameter set.

Default value: list

## command.done.confirm

Whether the done command should request confirmation before making changes.

Possible values

* False
* True

Default value: True

## command.edit.editor

The editor to use with the edit command.
If not specified, the EDITOR environmental variable will be used.

Default value: vim

## command.modify.confirm

Whether the modify command should request confirmation before making changes.

Possible values

* False
* True

Default value: True

## command.modify.summary

Whether the modify command should output a summary of changes.

Possible values

* False
* True

Default value: True

## command.start.confirm

Whether the start command should request confirmation before making changes.

Possible values

* False
* True

Default value: True

## command.stop.confirm

Whether the stop command should request confirmation before making changes.

Possible values

* False
* True

Default value: True

## context

The name of the currently active context.

Default value: ```<empty string>```

This value shouldn't be set manually.
Instead, the [context](command-context.md) command should be used.

## data.location

The folder to use when looking for data files.

Default value: ..

## data.done.filename

The filename to use for done tasks.  Appended to data.location.

Default value: done.txt

## data.pending.filename

The filename to use for in-progress tasks.  Appended to data.location.

Default value: todo.txt

## report.list.columns

The comma delimited list of columns to show when displaying the list report.

Default value: id,status,description

See [supported columns](columns.md) for the columns available in this setting.

## report.list.max_annotation_count

The maximum number of annotations to display with each task in the 'list' report.

Setting to 0 (zero) or less causes no annotations to be displayed.

If there are more annotations on a task than this number, only the most recent will be displayed.

Default value: 3.

## report.next.columns

The comma delimited list of columns to show when displaying the next report.

Default value: id,status,description

See [supported columns](columns.md) for the columns available in this setting.

## report.next.max_annotation_count

The maximum number of annotations to display with each task in the 'next' report.

Setting to 0 (zero) or less causes no annotations to be displayed.

If there are more annotations on a task than this number, only the most recent will be displayed.

Default value: 3.

## table.column.separator

The string to use to separate columns when printing tables.  Any double quotes will be stripped to allow leading and trailing spaces.

Default value: " | "

## table.header.underline

Whether to underline table headers to separate them from the rows.

Default value: True

## table.row.alt_backcolour

The background colour of alternating table rows.
See [background colours](colours.md#supported-background-colours) for options.

Default value: Black

## table.row.alt_forecolour

The foreground colour of alternating table rows.
See [foreground colours](colours.md#supported-foreground-colours) for options.

Default value: White

## table.row.backcolour

The background colour of table rows.
See [background colours](colours.md#supported-background-colours) for options.

Default value: Black

## table.row.forecolour

The foreground colour of table rows.
See [foreground colours](colours.md#supported-foreground-colours) for options.

Default value: White
