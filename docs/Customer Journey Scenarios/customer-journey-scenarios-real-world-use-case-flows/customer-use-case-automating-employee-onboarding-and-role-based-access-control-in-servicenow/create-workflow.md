---
title: Create WorkFlow
excerpt: Initiate a Workflow in ServiceNow Triggered by New Employee Records
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Creating a flow in ServiceNow involves using the Flow Designer, a powerful tool that enables you to automate processes and tasks within your ServiceNow environment without the need for extensive coding. Flows can consist of triggers, actions, and logic to perform a wide range of automated tasks, from simple notifications to complex orchestration of cross-application processes. Below is a step-by-step guide on how to create a flow in ServiceNow.

# Step 1: Access the Flow Designer

- Log in to your ServiceNow instance.
- In the Navigation Filter box, type Flow Designer.
- Click on Flow Designer to open the Flow Designer interface.

![](https://files.readme.io/f03a210-Screenshot_2024-02-29_at_19.35.24.png)

# Step 2: Create a New Flow

- In the Flow Designer interface, click on the New button to create a new flow.

![](https://files.readme.io/5c2279c-Screenshot_2024-02-29_at_19.36.45.png)

![](https://files.readme.io/71ddc55-Screenshot_2024-02-29_at_19.37.01.png)

- You'll be prompted to enter some initial details about your flow:
  - **Name**: Give your flow a descriptive name.
  - **Description (Optional)**: Provide a brief description of what your flow does.
  - **Application**: Select the application scope in which your flow will be created. This determines which data and actions your flow can access.

![](https://files.readme.io/e60c566-Screenshot_2024-02-29_at_19.38.08.png)

# Step 3: Define the Trigger

- Every flow starts with a trigger—what event will cause this flow to run. Click on Add Trigger.

![](https://files.readme.io/d0eb533-Screenshot_2024-02-29_at_19.38.45.png)

- Choose the type of trigger for your flow. Options typically include:
  - Record: Triggers the flow when a record is created, updated, or deleted.
  - Scheduled: Runs the flow at specified times.
  - Event: Triggers the flow based on ServiceNow events.

![](https://files.readme.io/39c6279-Screenshot_2024-02-29_at_19.39.31.png)

![](https://files.readme.io/f389112-Screenshot_2024-02-29_at_19.39.51.png)

![](https://files.readme.io/dad9f93-Screenshot_2024-02-29_at_19.40.01.png)

![](https://files.readme.io/a09d2f1-Screenshot_2024-02-29_at_19.40.30.png)

# Step 4: Add Actions

- With your trigger defined, you can start adding actions that the flow will execute.
- Click on Add Action in the main flow canvas.
- Browse or search for the action you want to add. 

![](https://files.readme.io/bafbf12-Screenshot_2024-02-29_at_19.44.33.png)

![](https://files.readme.io/9882831-Screenshot_2024-02-29_at_19.45.17.png)



# Step 5: Map Record Columns to Action Inputs



- With the action selected in your flow, look to the configuration panel on the right side of the screen. Here, you will see fields for each input of your action.
- Map each input to the corresponding column of the updated record by clicking on the input field. This opens a selection window where you can choose data pills.
- The data pills represent the fields of the record that triggered the flow. Drag and drop the appropriate data pill into the input field. For example, if you have an input named auth_name, find the Auth Name field from the list of available data pills (which represent the columns of the triggering record) and drop it into the auth_name input field.

![](https://files.readme.io/f7fbd9d-Screenshot_2024-02-29_at_19.46.45.png)

![](https://files.readme.io/57d766f-Screenshot_2024-02-29_at_19.47.03.png)

![](https://files.readme.io/ac3d885-Screenshot_2024-02-29_at_19.47.22.png)

![](https://files.readme.io/4a1c326-Screenshot_2024-02-29_at_19.48.03.png)



# Step 6: Test Your Flow

- Before using your flow in a production environment, it's important to test it to ensure it behaves as expected.
- Use the Test feature in Flow Designer to run your flow in a controlled environment. You can simulate the trigger and inspect the outcomes of each action.

![](https://files.readme.io/b58f04b-Screenshot_2024-02-29_at_19.49.09.png)



# Step 7: Activate Your Flow

- Once you're satisfied with the flow's performance during testing, you can activate it. An active flow will run according to its trigger conditions within your ServiceNow environment.

![](https://files.readme.io/ae78a9a-Screenshot_2024-02-29_at_19.49.19.png)

![](https://files.readme.io/ffa9a83-Screenshot_2024-02-29_at_19.49.27.png)

![](https://files.readme.io/8a48abc-Screenshot_2024-02-29_at_19.49.40.png)