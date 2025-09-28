---
title: ServiceNow Integration
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
## Introduction

> 👍 Note
>
> These instructions were created using the Vancouver release of ServiceNow. Newer versions may have a different UI.

### Centralized Access Request Record

Each access request triggers the creation of a dedicated record in ServiceNow Akeyless Application. This record captures essential details such as the requestor's identity and the specific item for which access is sought, providing admins with a comprehensive overview of each request and the ability to approve or decline the access request via ServiceNow instance.

[Download Akeyless Access Manager from the ServiceNow Store.](https://store.servicenow.com/sn_appstore_store.do#!/store/application/3f29fbc887f83d1009f27487cebb357a)

<Image border={false} src="https://files.readme.io/31626841ec2855f6ac1f288ff83e52946292d0fe7e55b3e6ba638dcacf6ea362-Screenshot_2024-09-20_at_6.32.09.png" />

<br />

### Prompt Admin Notification

System administrators receive immediate email or notification alerts upon new access requests. This notification mechanism ensures that requests are promptly reviewed and evaluated, minimizing delays in access provisioning.

**Note:** Notifications will need to be configured by ServiceNow Admin on the instance level for recorded addition or record update of the Akeyless ServiceNow application "access request" table.

### Streamlined Approval/Decline Process

Admins can conveniently view, evaluate, and take action on access requests directly within the ServiceNow instance. The approval or decline decision can be made with a single click, streamlining the approval process.

### Granular Control with Termination Option

Administrators maintain complete control over access requests, with the ability to terminate requests at any time. This termination option enhances security by ensuring that access privileges are revoked when they are no longer required.

### Automated Temporary Access Creation

Upon approval, ServiceNow Akeyless integration seamlessly generates temporary access for the specific item.

### Comprehensive Requestor Notification

Requestors receive timely notifications regarding the status of their access requests. This communication keeps users informed and enhances their overall experience with the access management process.

**Note:** Notifications will need to be configured by ServiceNow Admin on the instance level for recorded addition or record update of the Akeyless ServiceNow application "access request" table.

## Required Configuration on Akeyless System

To utilize the Akeyless ServiceNow App, an Access Role must be created. [This guide (Role-based Access Control (RBAC))](https://docs.akeyless.io/docs/rbac) outlines the steps for creating an Access Role in Akeyless.

Please configure the following permissions:

* Create/Read/Update role under /Access Requests/*

<Image border={false} src="https://files.readme.io/a2c79e6-image-20230206-103449.png" />

* List/Read for Auth methods under path

<Image border={false} src="https://files.readme.io/004d7ba-image-20230205-095303.png" />

* Read/Update/Delete (this is a set of actions that the user can request access for) for static secrets/targets under the path that item exists that the user can request access for (note, that path is case-sensitive)

<Image border={false} src="https://files.readme.io/92425b3-image-20230205-100518.png" />

## Required Configuration on ServiceNow System

Creating basic auth credentials via ServiceNow instance.

* Locate credentials in ServiceNow instance "All" menu
  * Click on "All" and enter "credentials" in the search field

<Image border={false} src="https://files.readme.io/518fa68-image-20221129-151725.png" />

<Image border={false} src="https://files.readme.io/ef0ecf7-Screenshot_2023-11-29_at_13.47.58.png" />

* Click "New" and locate the "Basic Auth Credentials" option

<Image border={false} src="https://files.readme.io/6e7a131-Screenshot_2023-11-29_at_13.50.06.png" />

* In “Basic Auth Credentials” Form, insert name (e.g. “akeyless_basic_auth_creds”), insert the access-id as the User name, and the access-key as the Password, and submit:

<Image border={false} src="https://files.readme.io/91cfd9b-Screenshot_2024-07-14_at_15.12.03.png" />

<br />

* In the "Name" field write "akeyless_basic_auth_creds"
* Add "User Name" & "Password" / [API key credentials](https://tutorials.akeyless.io/docs/authentication-methods-and-api-key-authentication#create-an-api-key-via-the-ui).

<Image border={false} src="https://files.readme.io/b11a153-Screenshot_2024-07-14_at_15.10.31.png" />

<br />

Add Jwt authentication in ServiceNow:

* Create certificate.
  (example: openssl req -new -x509 -key service_now.pem -out service_now_cert.pem -days 30)
* Store the certificate in ServiceNow:

  * Open “X.509 Certificate” table.
  * Insert name, paste the certificate in field “PEM Certificate”, ensure “Active” is set, and Submit.

  <Image border={false} src="https://files.readme.io/b60bfff-Screenshot_2024-07-14_at_15.17.26.png" />

  <br />
* Create oAuth Application Registry:
  * Choose the option "Create an OAuth JWT API endpoint for external clients":

<Image border={false} src="https://files.readme.io/25c6457-Screenshot_2024-07-14_at_15.21.19.png" />

<br />

* Insert name, choose “User field” (email is default), ensure “Active” and “Enable JTI Verification“ are set, and Submit.

<Image border={false} src="https://files.readme.io/5d06013-Screenshot_2024-07-14_at_15.25.52.png" />

* After created, copy the Client ID and the Client Secret.

<Image border={false} src="https://files.readme.io/c1d69ce-Screenshot_2024-07-14_at_15.33.14.png" />

* Scroll down to “Jwt Verifier Maps”, press New.

<Image border={false} src="https://files.readme.io/8af87f5-Screenshot_2024-07-14_at_15.33.39.png" />

* Insert name, find the certificate in “Sys certificate“ list, and Submit.

<Image border={false} src="https://files.readme.io/d32f15b-Screenshot_2024-07-14_at_15.36.45.png" />

<br />

* Create user with akeyless role:
  * Create user in “Users” table:

<Image border={false} src="https://files.readme.io/b22ab87-Screenshot_2024-07-14_at_15.45.00.png" />

* Scroll down to Roles and press Edit:

<Image border={false} src="https://files.readme.io/010f9ce-Screenshot_2024-07-14_at_15.49.21.png" />

* Pick role “x_akse_akeyless_sa_akeyless_access_request” from the collection, and Save:

<Image border={false} src="https://files.readme.io/e47d4a5-Screenshot_2024-07-14_at_15.49.00.png" />

<br />

* Configure ServiceNow Event Forwarder in Akeyless:
  * Create new event forwarder:

<Image border={false} src="https://files.readme.io/b1a5f9b-Screenshot_2024-07-14_at_15.56.29.png" />

Insert the details. It is recommended to choose Auth type “JWT”. Insert the private key used to sign the certificate. Insert the user created in ServiceNow. Insert the client-id and client-secret from the oAuth Application in ServiceNow.

<Image border={false} src="https://files.readme.io/d383a3d-Screenshot_2024-07-14_at_16.01.06.png" />

<br />

### Approving Access Request via ServiceNow Instance

* Locate "akeyless_access_request" table in ServiceNow instance "All" menu
  * Click on "All" and enter "akeyless_access_request" in the search field
  * Click on the table name

<Image border={false} src="https://files.readme.io/2b9f76f-Screenshot_2023-11-29_at_17.10.35.png" />

* Once an access request is created via Akeyless system a new record will appear

<Image border={false} src="https://files.readme.io/7417bb1-image-20230206-132008_1.png" />

* Admin users of the ServiceNow intense will be able to approve or decline the access request by updating the "Dession" field.

<Image border={false} src="https://files.readme.io/f337a71-image-20230206-132144.png" />

* Upon approval within the ServiceNow Akeyless app, a request is sent to Akeyless systems to generate temporary access for the specific item.

### Notifications

Admins and users (requestors) can receive notifications when certain actions are performed on the "akeyless_access_request" table in the ServiceNow instance.

Admins can receive notifications when a new access request record is created, while users (requestors) can receive notifications when their access request is approved.

These notifications can be configured based on specific actions, such as when a new record is added or when a record is updated by an admin user of the ServiceNow instance.

[Refer to the ServiceNow documentation on push notifications.](https://docs.servicenow.com/bundle/xanadu-platform-administration/page/administer/notification/reference/r_PushMessageArchitecture.html)
