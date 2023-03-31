# Supported Date Formats

Dates can be specified in a number of formats:

* [absolute](#absolute-date-format)
* [literal](#literal-date-format)
* [relative](#relative-date-format)

## Absolute Date Format

Absolute date formats must be in iso format:

```text
<year>-<month>-<day>
```

Where:

* year is the 4 digit number for the year.
* month is the 2 digit number for the month.
* day is the 2 digit number for the day of the month.

## Literal Date Format

This format allows a fixed set of strings to be specified that are used to calculate a relative date.

The following are supported:

* today
* tomorrow

## Relative Date Format

The relative date format allows a simple calculation to be used to calculate a date.

The relative date format is as follows:

```text
<direction><number><unit>
```

Where:

* direction can be '+' for a future date from now or '-' for a past date.
* value can be any integer value.
* unit can be any supported unit.

The supported relative date units are:

* d: days.
* m: months.
* w: weeks.

## Examples

|Example     | Date Type | Description                  |
|------------|-----------|------------------------------|
| 2021-04-17 | iso       | 17th April 2021              |
| -4d        | relative  | 4 days in the past           |
| +2d        | relative  | 2 days in the future         |
| today      | literal   | the date the command was run |
