# Reports

Creating a report can be done in configuration and the reports will be accessible as if they were built in commands.

## Usage

```bash
tasks [filter] <report name>
```

## Positional Arguments

|Name  |Description                   |
|:-----|:-----------------------------|
|filter|The optional task filter.     |
|name  |The name of the report to run.|

## Built In Reports

The following are the built in reports.  These can be customized in the same way as adding a new custom report by adding the relevant configuration.

* list
* next

## Customizing and Adding Reports

* report.<name>.columns: a comma delimited list of attributes to display.
* report.<name>.filter: the filter to apply to the task list before displaying them.
* report.<name>.max_annotation_count
* report.<name>.sort: a comma delimited list of attributes showing the order in which to display the tasks. A '+' suffix means ascending order, a '-' suffix means descending order. If neither is sepecified then ascending order is used.

## Applicable Settings

* [table.column.separator](settings.md#tablecolumnseparator)
* [table.header.underline](settings.md#tableheaderunderline)
* [table.row.alt_backcolour](settings.md#tablerowalt_backcolour)
* [table.row.alt_forecolour](settings.md#tablerowalt_forecolour)
* [table.row.backcolour](settings.md#tablerowbackcolour)
* [table.row.forecolour](settings.md#tablerowforecolour)
