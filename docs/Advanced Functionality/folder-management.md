---
title: Folder Management
deprecated: false
hidden: false
metadata:
  robots: index
---
You can organize your secrets and other items in the Akeyless Console by creating folders even if they’re initially empty.

# Create a folder from the CLI

To create an empty folder from the CLI, run the following command:

```shell
akeyless folder create \
--name <Folder Name> \
--type[=items] <Folder Type> \
--accessibility[=regular] <[regular/personal]>
```

You can find the complete list of commands for managing folders in the CLI Reference.

# Create a folder in the Akeyless Console

1. Log in to the Akeyless Console, and navigate to Items.
2. Click the **New Folder** button.
3. In the dialog that appears:

* Define a Name for the folder, and specify the Location as a path to the virtual folder where you want to create the new folder, using slash (/) separators. If the specified path does not exist, it will be automatically created along with the new folder.

Once created, the folder will immediately appear in your Items list, ready for you to start adding secrets, keys, or additional subfolders.

<br />
