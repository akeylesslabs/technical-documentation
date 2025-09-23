---
title: Establish a New Employee Table in ServiceNow's Global Scope
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
To create a new employee table in ServiceNow's global scope with specific fields tailored for automating authentication method creation and associating access roles, along with additional employee information, you will need to define the following fields during the table creation process:

To ensure that you are creating your new employee table in the global scope within ServiceNow, follow these guidelines. The global scope allows the table and its data to be accessible across multiple applications, which is essential for broad-based functionality and integration capabilities within the ServiceNow platform.

# Ensure Global Scope Selection:

* **Application Field:** Look for an application field or dropdown in the table creation form. The option to select "Global" may vary based on the version and configuration of your ServiceNow instance. If you see an option to select "Global," ensure it is chosen. If there is no specific dropdown or if you are unsure, leaving this field blank or following the default settings typically assigns the table to the global scope.
* **Scope Confirmation:** After filling out the form and before saving, verify if there's an indicator or a field that confirms the scope of the table. Some interfaces may explicitly show the scope as "Global" before finalizing the table creation.

![](https://files.readme.io/c8447a0-Screenshot_2024-02-29_at_13.30.15.png)

![](https://files.readme.io/0260919-Screenshot_2024-02-29_at_13.30.27.png)

# Navigate to the Table Creation Interface:

* Access the ServiceNow dashboard.
* Go to System Definition > Tables. This section allows you to manage and create new tables within the platform.

![](https://files.readme.io/baf3b31-Screenshot_2024-02-29_at_13.27.37.png)

# Start the Table Creation Process:

* Click on the New button to begin creating a new table.
* This action opens a form where you can enter details about the new table you want to create.

![](https://files.readme.io/4552a07-Screenshot_2024-02-29_at_13.28.14.png)

# Specify Table Details:

* In the table creation form, fill out the necessary details for your table, such as Name, Label, and Plural Label.
* For fields that specifically relate to the scope, such as Application, ensure that the application field is either set to "Global" or left blank. In ServiceNow, if no specific application is selected, the table defaults to the global scope, making it accessible across all applications.

![](https://files.readme.io/ed7a394-Screenshot_2024-02-29_at_13.29.28.png)

# Fields for Authentication Method Creation

**Auth Name:** A string field to store the name or title of the authentication method assigned to the employee. This could be a descriptive name indicating the type of authentication (e.g., "OAuth Token", "Biometric").

**Metadata URL:** A URL field to store the address of a metadata resource or an endpoint that contains additional information about the authentication method. This URL could link to documentation or APIs related to the auth method.

**Unique Identifier:** A string or unique identifier field intended to store a value that uniquely identifies the employee within the authentication system. This could be an employee ID, a UUID, or any other unique identifier that ties the authentication method to the specific employee.

# Fields for Associating Access Roles

**Access Role:** A choice or reference field to associate the employee with specific access roles within the system. This field would likely reference a predefined list or table of roles, allowing for the selection of one or more roles that the employee should be granted based on their position or duties.

# Additional Employee Information Fields

**First Name:** A string field to store the employee's first name. This is a basic field for personal identification and communication purposes.

**Last Name:** A string field to store the employee's last name. Along with the first name, it helps in uniquely identifying and addressing the employee within the organization.

**Email**: An email field to store the employee's email address. This field is crucial for communication and may also serve as an identifier for various system integrations or authentication methods.

![](https://files.readme.io/7178332-Screenshot_2024-02-29_at_13.33.47.png)
