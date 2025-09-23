---
title: Create a Table in ServiceNow
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
Creating a table in ServiceNow involves defining a new data structure to store information relevant to your business processes. ServiceNow tables can hold data for various purposes, such as tracking incidents, managing assets, or custom applications data. Here's a step-by-step guide to creating a table in ServiceNow:

# Step 1: Access Table Creation

- Log in to your ServiceNow instance as an administrator or with a role that has permissions to create and manage tables.
- Navigate to System Definition > Tables in the Application Navigator on the left side of the screen.

![](https://files.readme.io/71cd2e2-Screenshot_2024-03-05_at_12.24.04.png)



# Step 2: Create New Table

- Click on the New button to start creating a new table.
- You will be presented with a form to fill out details for your new table.

![](https://files.readme.io/84236ea-Screenshot_2024-03-05_at_12.24.19.png)



# Step 3: Define Table Details

![](https://files.readme.io/16e88a1-Screenshot_2024-03-05_at_12.24.30.png)



# Step 4: Configure Table Columns (Fields)

- After defining the basic table details, you'll need to add fields (columns) to your table. Each field represents a piece of information you want to store in each record.
- You can add fields by clicking on the Add Column button and specifying the field type (e.g., string, choice, reference, date/time), name, and other properties.

![](https://files.readme.io/cf02d50-Screenshot_2024-03-05_at_12.24.46.png)



# Step 5: Save the Table

- Once you've configured your table and added the desired fields, click the Submit button to save your new table.  
  Your new table will now be created in the database, and you can start adding or importing records.

# Step 6: Accessing and Using Your New Table

- If you opted to create a module for the table, you would find it in the Application Navigator under the application you specified during creation.
- You can access the table to add, view, or modify records. Additionally, you can configure form layouts, create business rules, and set up access controls to manage how data in the table is used and accessed.

![](https://files.readme.io/fdc444c-Screenshot_2024-03-05_at_12.30.36.png)