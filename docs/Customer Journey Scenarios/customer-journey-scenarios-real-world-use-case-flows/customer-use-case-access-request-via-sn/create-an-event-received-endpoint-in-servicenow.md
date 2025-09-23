---
title: Create an "Event Received" Endpoint in ServiceNow
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
A Scripted REST API in ServiceNow is a powerful way to create custom REST APIs according to your specific business requirements. It allows you to define your own endpoints, request methods, and scripts to process incoming requests and send responses. This customization capability enables you to extend ServiceNow's functionality, integrate with external systems, and handle complex data transformations or business logic not covered by out-of-the-box REST APIs. Here’s a detailed explanation of key components and how to set up a Scripted REST API in ServiceNow:

# Key Components of Scripted REST APIs

- **API**: Represents the overall API you're creating. It serves as a container for your resources.
- **Resource**: Each API can have multiple resources. A resource represents a specific URL pattern and method (GET, POST, PUT, DELETE) combination. It’s where you define the logic for handling requests and sending responses.
- **Script**: Attached to a resource, this is where you implement the logic to process the incoming request, interact with the ServiceNow database or other APIs, and determine the response to send back.

# Creating a Scripted REST API

To create a Scripted REST API in ServiceNow, follow these general steps:

Navigate to Scripted REST APIs

- In your ServiceNow instance, go to System Web Services > Scripted REST APIs.

![](https://files.readme.io/284702a-Screenshot_2024-03-05_at_12.14.39.png)

Create a New API

- Click New to start defining your API. Provide a name and, optionally, a base API path. The base path is a URL segment unique to your API that precedes any resources you define.

![](https://files.readme.io/bf01c74-Screenshot_2024-03-05_at_12.15.47.png)

Add a Resource

- Within your API, you'll need at least one resource. Click New to create a resource. Here, you define the resource name, HTTP method (e.g., GET for retrieving data, POST for creating data), and the URL suffix (path) that, combined with the base path, defines the full URL to access the resource.

![](https://files.readme.io/f5c135f-Screenshot_2024-03-05_at_12.16.08.png)

Implement the Resource Script

- The most crucial part of your resource is the script that executes when the resource's URL and method are matched by a request. In the script, you use the request object to access request data (headers, query parameters, body) and the response object to set the response status, headers, and body.
- Your script might query or update records in the ServiceNow database, call other REST APIs, perform calculations, or execute any other logic required for your integration or application.

![](https://files.readme.io/bcd2ffe-Screenshot_2024-03-05_at_12.16.25.png)