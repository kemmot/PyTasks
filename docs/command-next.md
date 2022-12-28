# Next Command

Lists non-waiting tasks in priority order.

The order is based on the following...

* Started tasks first.
* Tasks with a due date with earliest due dates first.
* Tasks with a priority in order of H, then M then L.
* Blocked tasks last.

## Usage

```bash
tasks [filter] next
```

## Positional Arguments

|Name  |Description              |
|:-----|:------------------------|
|filter|The optional task filter.|

## Applicable Settings

* [report.next.columns](settings.md#reportnextcolumns)
* [report.next.max_annotation_count](settings.md#reportnextmax_annotation_count)
* [table.column.separator](settings.md#tablecolumnseparator)
* [table.header.underline](settings.md#tableheaderunderline)
* [table.row.alt_backcolour](settings.md#tablerowalt_backcolour)
* [table.row.alt_forecolour](settings.md#tablerowalt_forecolour)
* [table.row.backcolour](settings.md#tablerowbackcolour)
* [table.row.forecolour](settings.md#tablerowforecolour)
