---
title: Set Up Event Forwarder on Akeyless System
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
Setting up an event forwarder in Akeyless is a process that enables you to automatically send events from Akeyless to another system or application, such as a logging or monitoring service. This capability is particularly useful for maintaining security and operational awareness. Here’s how to configure an event forwarder in Akeyless:

# Step 1: Access the Akeyless Console

Log In: Start by logging into your Akeyless management console. You'll need administrative access to configure event forwarders.

# Step 2: Navigate to Event Forwarders

* Click the bell icon

![](https://files.readme.io/7169d0e-Screenshot_2024-03-05_at_10.34.12.png)

* Click open event center

# Step 3: Create a New Event Forwarder

Initiate Creation: Inside the event forwarders section, there should be an option to create a new event forwarder.

* Click on “New” 

# Step 4: Configure Event Forwarder Settings

* Specify Destination: Enter the destination where you want the events to be forwarded. Choose ServiceNow.

![](https://files.readme.io/7cf76cd-Screenshot_2024-03-05_at_10.34.26.png)

* Name the event

![](https://files.readme.io/71aa6c3-Screenshot_2024-03-05_at_10.40.16.png)

* ServiceNow URL
  * Instance url = https\://{user.your_seervicenow_instance_name}.service-now\.com//
  * Api call url = for example pi/1235934/json\_reciver\_from\_akeyless/akeyless\_events, this is a path of Scripted Rest Resource path from ServiceNow admin console  

![](https://files.readme.io/5643d2b-Screenshot_2024-03-05_at_10.43.04.png)

* Must have suffix = ?api=api
* Authentication
  * For our example I am using user name / password auth
  * username = the admin user name of the instance, in case you are using the dev servicenow environment the user name called 'admin'
  * ServiceNow details can be found here:

![](https://files.readme.io/9d65bba-Screenshot_2024-03-05_at_11.11.56.png)

![](https://files.readme.io/d99c9f2-Screenshot_2024-03-05_at_11.12.28.png)

# Step 5: Register the Gateway

* Select the configured gateway 
* [Link](https://docs.akeyless.io/docs/create-a-gateway-in-akeyless-system-1) to Gateway configuration

![](https://files.readme.io/9eeb32e-Screenshot_2024-03-05_at_11.15.01.png)
