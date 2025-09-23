---
title: 'Customer Use Case: Access Request via ServiceNow'
excerpt: >-
  Integrating Akeyless API with ServiceNow to enable direct approval or
  rejection of access requests through the ServiceNow platform.
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
# Background

In the rapidly evolving digital landscape, a leading multinational corporation recognized the need to enhance its organizational security and operational efficiency. The company faced challenges in managing access requests efficiently, often dealing with time-consuming processes and the high risk of security breaches due to manual errors.

# Challenge

The company sought a solution that could streamline the process of managing access requests, from internal systems and databases to secure remote access for offsite work. They needed a system that could automate the approval or denial of these requests, enforce strict security standards, and ensure compliance with both internal and external regulations.

# Solution

The company chose to integrate Akeyless API with the ServiceNow platform, leveraging Akeyless' expertise in secure access management solutions and ServiceNow's robust IT service management capabilities. This integration enabled seamless interactions with IT systems to manage access credentials and permissions securely.

# Implementation

With the integrated solution, IT personnel were empowered to approve or decline access requests directly within the ServiceNow platform using the Akeyless API. This direct interaction simplified the approval process, made it more efficient, and significantly reduced the likelihood of errors, thus bolstering security measures across the board.

Utilizing the security and compliance data provided by Akeyless, approvers could make informed decisions within the ServiceNow interface. They had the flexibility to approve requests, granting the necessary access permissions automatically through Akeyless, or to decline them if they did not meet the organization's stringent security standards.

# Implementation Steps for the Solution

**Prerequisites for Implementation**

Before beginning the implementation of the solution, it's essential to have the following prerequisites in place:

* **Akeyless Admin Account:** An administrative account on Akeyless is required. This account will enable access to Akeyless APIs and the management of secure access credentials and permissions.
* **ServiceNow Admin Account:** An administrative account on ServiceNow is necessary to facilitate the integration and to manage the workflows and access requests directly within the ServiceNow platform.
* **Docker:** A system with Docker installed is crucial for deploying any necessary containers that might be required for the integration or for running specific services related to Akeyless or ServiceNow. Docker will provide the flexibility and ease of deployment for various components of the solution.

To implement the integration of Akeyless with ServiceNow for managing access requests and utilizing event forwarding, follow these detailed steps:

**[Create a Gateway in Akeyless](https://docs.akeyless.io/docs/create-a-gateway-in-akeyless-system-1):** The initial step involves setting up an Akeyless gateway. This is a crucial step as having a gateway is mandatory to utilize the event forwarder functionality. The gateway serves as a bridge, facilitating secure communication between Akeyless and other systems or applications.

* [To begin constructing the Gateway, we must first set up Docker.](https://docs.akeyless.io/docs/create-a-gateway-in-akeyless-system)

**[Set Up Event Forwarder in Akeyless](https://docs.akeyless.io/docs/set-up-event-forwarder-on-akeyless-system):** Once the gateway is in place, the next step is to configure an event forwarder in Akeyless. This forwarder will be responsible for detecting and forwarding specific events (such as access requests) to the ServiceNow platform.

**[Install and Activate Event Management Plugin in ServiceNow](https://docs.akeyless.io/docs/install-and-activate-event-management-plugin-in-servicenow):** Before proceeding with the creation of an event receiver, it is necessary for the admin to install and activate the Event Management plugin within the ServiceNow system. This plugin is essential for handling the incoming events from Akeyless.

**[Create an "Event Received" Endpoint in ServiceNow](https://docs.akeyless.io/docs/create-an-event-received-endpoint-in-servicenow):** Utilizing scripted REST APIs, create an "Event Received" endpoint in ServiceNow. This endpoint will act as the receiver for events forwarded by Akeyless. This step involves writing custom scripts to define how ServiceNow processes and responds to the received events.

**[Create a Table in ServiceNow](https://docs.akeyless.io/docs/create-a-table-in-servicenow):** Create a table in ServiceNow to store the events received from Akeyless. This table will serve as a log or record, keeping track of all access request events and their details for future reference and action.

**[Develop a Script to Parse the JSON Body](https://docs.akeyless.io/docs/develop-a-script-to-parse-the-json-body):** Implement a script in ServiceNow that can accurately parse the JSON body sent by the Akeyless event forwarder. The script should be capable of extracting necessary information from the event data and storing it in the previously created table.

**[Set Up a Flow in ServiceNow](https://docs.akeyless.io/docs/set-up-a-flow-in-servicenow):** Establish a flow within ServiceNow that triggers actions based on the approval or decline of access requests. This flow will automate the process, ensuring that each event received leads to an appropriate response within the ServiceNow system.

**[Create a Script for Approval/Decline Actions](https://docs.akeyless.io/docs/create-a-script-for-approvaldecline-actions):** Finally, use a script that executes an API request to Akeyless, to either approve or decline the access request. This decision is based on the relevant fields and updated values within the ServiceNow table columns. This script ensures that the final decision made within ServiceNow is communicated back to Akeyless, completing the loop of request and action.
