# Context Command

Contexts allow the same tags and attributes to be used implicitly with all commands.
This can make it easier to work with different subsets of tasks.

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

Any new tasks added will be added with the following metadata and any task retrieval will use these as filters (in additiona to any supplied with each command):

* the 'home' tag.
* the 'priority' attribute with the 'H' value.
* the 'project' attribute with the 'diy' value.

For example, if that context were active then the next add command will add a task with the following metadata:

* the 'home' tag.
* the 'shopping' tag.
* the 'priority' attribute with the 'H' value.
* the 'project' attribute with the 'diy' value.
* the 'due' attribute with a date 2 days from now.

```bash
tasks add buy paint +shopping due:+2d
```

For reference, each context definition will create a setting of the format:

```text
context.<name>
```

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
