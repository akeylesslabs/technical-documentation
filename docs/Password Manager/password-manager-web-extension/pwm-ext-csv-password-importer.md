---
title: CSV Password Importer

slug: pwm-ext-csv-password-importer
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
The CSV Password Import feature allows users to import passwords from a CSV file directly through the web extension. Passwords can be imported into the Personal or Corporate area, depending on account permissions.

The importer uses the current account configuration when a new import session starts.

## How to Use the CSV Password Import Feature

## Step 1: Access the Web Extension Settings

* Open the web extension from your browser toolbar.
* Navigate to the 'Settings' option within the extension menu.

![Settings option in the web extension menu](https://files.readme.io/522836b-Screenshot_2024-07-01_at_16.09.35.png)

## Step 2: Initiate the Import Process

* In the Settings menu, locate and click on the "Import from CSV" button to start the import procedure.

## Step 3: Define CSV File Format

* Ensure your CSV file is prepared according to the required format. The standard format should include columns such as 'Account Name', 'Username', 'Password', and other necessary details.

## Step 4: Select the CSV File

* Click on the file selection button to browse and choose the desired CSV file from your local storage.

## Step 5: Choose Import Location

* Select where the passwords will be imported: choose either the Personal or Corporate area in Password Manager.
* If the Personal area is not available for the account, import into the Corporate area.

## Step 6: Create a Dedicated Folder

* Specify if you wish to create a dedicated folder within the target location by entering a folder name in the 'Target Folder Field'.

![Target Folder field in the CSV import screen](https://files.readme.io/8898628-Screenshot_2024-06-04_at_14.52.18.png)

## Step 7: Submit the Import

* Once all settings are configured and the file is ready, click the 'Submit' button to finalize the import process.

## Import Behavior

The extension improves import consistency in these areas:

* Import settings are refreshed when a new import session starts.
* Current account configuration is reflected in the import flow before submission.
* Imported items follow the active destination and account defaults selected during import.

## Import Progress

The extension can display import progress while CSV import is running.

During import, the status view can show:

* The number of completed items.
* The total number of items in the import batch.
* A progress bar for the current import operation.

![CSV import progress screen](https://files.readme.io/97988b1-Screenshot_2024-06-04_at_14.52.11.png)
