# Context Command

Contexts allow the same tags and attributes to be used implicitly with report commands.

The following sub commands are available for working with contexts:

* [defining](#defining-contexts)
* [activating](#activating-contexts)
* [deactivating](#deactivating-contexts)
* [listing](#listing-contexts)
* [showing](#showing-contexts)
* [deleting](#deleting-contexts)

## Defining Contexts

Contexts must be defined before they can be activated.

### Usage

```bash
tasks context define <name> <definition [attribute:value ...] [+tag ...]>
```

### Positional Arguments

|Name     |Description             |
|:--------|:-----------------------|
|name     |The name of the context.|

Note that the following values cannot be used as context names:

* define
* delete
* list
* none
* show

### Example

The following example creates a context called 'hidiy'.

```bash
tasks context hidiy +home project:diy priority:H
```

This context would causes reports to filter tasks on the following:

* The 'home' tag.
* The 'diy' value for the 'project' attribute.
* the 'H' value for the 'priority' attribute.

## Activating Contexts

Once contexts have been defined, they can then be activated.

### Usage

```bash
tasks context <name>
```

### Positional Arguments

|Name     |Description                         |
|:--------|:-----------------------------------|
|name     |The name of the context to activate.|

## Deactivating Contexts

### Usage

```bash
tasks context none
```

## Deleting Contexts

### Usage

```bash
tasks context delete <name>
```

### Positional Arguments

|Name     |Description                       |
|:--------|:---------------------------------|
|name     |The name of the context to delete.|

## Listing Contexts

### Usage

```bash
tasks context list
```

## Showing Contexts

Shows the currently active context.

### Usage

```bash
tasks context show
```

## Applicable Settings

* [command.context.define.confirm](settings.md#commandcontextdefineconfirm)
* [command.context.delete.confirm](settings.md#commandcontextdeleteconfirm)
* [context](settings.md#context)

## Implementation Details

Each context definition will create a setting of the format:

```text
context.<name>
```
