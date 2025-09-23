---
title: 'Customer Use Case: Automated Onboarding'
excerpt: Automating Employee Onboarding and Role-Based Access Control in ServiceNow
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
## Background

A rapidly growing company requires an efficient and secure system to manage new employee onboarding, specifically focusing on authentication and access control within their ServiceNow environment. To address this, the company plans to leverage Akeyless API to automate the creation of new authentication methods for each employee and assign them to predefined access roles based on their job function, directly within ServiceNow.

## Requirements

### Akeyless Account and API Access

- A valid Akeyless account with administrative privileges to generate API keys and manage access roles.
- API keys, allowing ServiceNow to securely communicate with Akeyless services.

For detailed instructions on configuring your Akeyless API keys, please refer to our [Akeyless API Key Configuration Guide](https://docs.akeyless.io/docs/api-key).

## ServiceNow Requirements

### ServiceNow Instance and Administrator Access

- An active ServiceNow instance with administrative access to create custom tables, define business rules or workflows, and configure REST API integrations.

### REST API Integration Capabilities

- The ability to make outbound REST API calls to Akeyless for creating and managing authentication methods and access roles.
- Support for securely storing API credentials and handling API responses within ServiceNow.

### Custom Table and Workflow Configuration

- Tools and permissions to create custom tables for storing new employee records.
- Capabilities to develop custom workflows or business rules that trigger upon the addition of a new employee record, integrating with Akeyless APIs.

### Role-Based Access Control Management

- The ability to dynamically assign and manage access roles within ServiceNow, potentially using information from Akeyless to determine the appropriate roles based on the authentication method or policy.

### Implementation

- **[Establish a New Employee Table in ServiceNow's Global Scope](https://docs.akeyless.io/docs/establish-a-new-employee-table-in-servicenows-global-scope):** Set up a dedicated table within the global scope of ServiceNow to house new employee records.
- **[Define Table Fields](https://docs.akeyless.io/docs/establish-a-new-employee-table-in-servicenows-global-scope#fields-for-authentication-method-creation): **Specify and create the necessary fields within the new employee table to capture essential employee information.
- **[Create a Table Form for New Record Entries](https://docs.akeyless.io/docs/create-a-table-form-for-new-record-entries):** Develop a user-friendly form in ServiceNow that facilitates the entry of new employee details into the dedicated employee table. This form is crucial for populating the table with the necessary information to trigger the automated workflow for authentication and access role configuration.
- **[Develop a Custom Action in ServiceNow for Akeyless API Requests](https://docs.akeyless.io/docs/custom-action-in-servicenow): **Implement a custom action within the ServiceNow platform designed to initiate POST requests to the Akeyless API.
  - **[Integrate Script for ServiceNow-to-Akeyless Communication](https://docs.akeyless.io/docs/custom-action-in-servicenow#step-5-add-a-script-step-for-the-post-request):** Include a script within the custom action to facilitate the direct communication between ServiceNow and Akeyless.
  - **[Set Up Input Parameters for the ServiceNow Custom Action](https://docs.akeyless.io/docs/custom-action-in-servicenow#step-4-configure-the-action-inputs): **Configure the necessary input parameters within the custom action to accurately send data to the Akeyless API.
- **[Initiate a Workflow in ServiceNow Triggered by New Employee Records](https://docs.akeyless.io/docs/create-workflow):** Craft a workflow within ServiceNow that automatically activates upon the addition of a new record to the employee table.
- **[Link the Custom Action to the Workflow](https://docs.akeyless.io/docs/create-workflow#step-4-add-actions):** Ensure the previously created custom action is connected to the workflow to enable automated processing.
- **[Align Parameters Between the Custom Action and the Workflow](https://docs.akeyless.io/docs/create-workflow#step-5-map-record-columns-to-action-inputs):** Map the input parameters from the custom action to the corresponding elements in the workflow to ensure seamless data transfer and execution.

Once all implementation steps are finalized, should you add a new record to the employee table (either through the appropriate form or directly within the table itself), the system will automatically generate a corresponding authentication method for the newly added employee and link it to the appropriate access role.

![](https://files.readme.io/a06b926-Screenshot_2024-02-29_at_19.57.53.png)

![](https://files.readme.io/073480a-Screenshot_2024-02-29_at_19.58.46.png)