---
title: Akeyless SaaS Core Services
deprecated: false
hidden: false
link:
  new_tab: false
metadata:
  title: ''
  description: ''
  robots: index
---
The Akeyless Gateway is a stateless Docker container, provided as a standalone or as a cluster. To function correctly, it requires public network connectivity to the Akeyless SaaS core services (see the table below).

A basic Gateway deployment requires a server with a Docker engine installed. You may download the latest Docker engine on [Docker website](https://docs.docker.com/get-docker/). You'll need public network access enabled on port 443 to pull a Docker image from the `hub.docker.com`.

> 📘 Tenant Environments
>
> Accounts that were created on specific environments should modify the services endpoints according to the relevant environments. e.g. for `eu`  `https://vault.eu.akeyless.io`  etc.
>
> Available explicit tenates are: `us`,`eu` .

The following table describes the main functionality of Akeyless microservices in the global environment:

<Table align={["left","left","left","left","left"]}>
  <thead>
    <tr>
      <th>
        Service
      </th>
      <th>
        URLs
      </th>
      <th>
        IP
      </th>
      <th>
        Port
      </th>
      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        **Console**
      </td>
      <td>
        [https://console.akeyless.io](https://console.akeyless.io)
      </td>
      <td>
        52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128
      </td>
      <td>
        443
      </td>
      <td>
        Akeyless SaaS platform
      </td>
    </tr>

    <tr>
      <td>
        **Vault**
      </td>
      <td>
        [https://vault.akeyless.io](https://vault.akeyless.io)  
        [https://vault-ro.akeyless.io](https://vault-ro.akeyless.io)
      </td>
      <td>
        52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128
      </td>
      <td>
        443
      </td>
      <td>
        User Account Management (UAM), managing user accounts, items, and roles
      </td>
    </tr>

    <tr>
      <td>
        **Auth**
      </td>
      <td>
        [https://auth.akeyless.io](https://auth.akeyless.io)  
        [https://auth-ro.akeyless.io](https://auth-ro.akeyless.io)
      </td>
      <td>
        52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128
      </td>
      <td>
        443
      </td>
      <td>
        Akeyless Authentication service
      </td>
    </tr>

    <tr>
      <td>
        **Certificate Auth**
      </td>
      <td>
        [https://auth-cert.akeyless.io](https://auth-cert.akeyless.io)
      </td>
      <td>
        18.189.176.104
      </td>
      <td>
        443
      </td>
      <td>
        Relevant only for Certificate Based Auth
      </td>
    </tr>

    <tr>
      <td>
        **Audit**
      </td>
      <td>
        [https://audit.akeyless.io](https://audit.akeyless.io)  
        [https://audit-ro.akeyless.io](https://audit-ro.akeyless.io)
      </td>
      <td>
        52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128
      </td>
      <td>
        443
      </td>
      <td>
        Audit log main service, enables log forwarding from GW & Bastion
      </td>
    </tr>

    <tr>
      <td>
        **BIS**
      </td>
      <td>
        [https://bis.akeyless.io](https://bis.akeyless.io)  
        [https://bis-ro.akeyless.io](https://bis-ro.akeyless.io)
      </td>
      <td>
        52.223.11.194, 35.71.185.167
      </td>
      <td>
        443
      </td>
      <td>
        Billing Infrastructure Service (BIS)
      </td>
    </tr>

    <tr>
      <td>
        **Gator**
      </td>
      <td>
        [https://gator.akeyless.io](https://gator.akeyless.io)  
        [https://gator-ro.akeyless.io](https://gator-ro.akeyless.io)
      </td>
      <td>
        52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128
      </td>
      <td>
        443
      </td>
      <td>
        Main service to sync gateways instances, and connections with Akeyless SaaS
      </td>
    </tr>

    <tr>
      <td>
        **MQ**
      </td>
      <td>
        amqps://mq.akeyless.io
      </td>
      <td>
        52.223.11.194, 35.71.185.167
      </td>
      <td>
        5671
      </td>
      <td>
        Message queue between Akeyless micro-services
      </td>
    </tr>

    <tr>
      <td>
        **KFM**
      </td>
      <td>
        [https://kfm1.akeyless.io](https://kfm1.akeyless.io),  
        [https://kfm1-ro.akeyless.io](https://kfm1-ro.akeyless.io),
        [https://kfm2.akeyless.io](https://kfm2.akeyless.io),  
        [https://kfm2-ro.akeyless.io](https://kfm2-ro.akeyless.io),
        [https://kfm3.akeyless.io](https://kfm3.akeyless.io),  
        [https://kfm3-ro.akeyless.io](https://kfm3-ro.akeyless.io),
        [https://kfm4.akeyless.io](https://kfm4.akeyless.io),  
        [https://kfm4-ro.akeyless.io](https://kfm4-ro.akeyless.io)
      </td>
      <td>
        52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128, 34.120.160.242
      </td>
      <td>
        443
      </td>
      <td>
        Key Fragments Services, enabling full DFC encryption
      </td>
    </tr>

    <tr>
      <td>
        **Public Gateway**
      </td>
      <td>
        [https://rest.akeyless.io](https://rest.akeyless.io)  
        [https://api.akeyless.io](https://api.akeyless.io)
      </td>
      <td>
        15.197.223.248, 3.33.244.138
      </td>
      <td>
        443
      </td>
      <td>
        * _Optional_* Public Gateway rest API v1\v2
      </td>
    </tr>

    <tr>
      <td>
        **Public HVP**
      </td>
      <td>
        [https://hvp.akeyless.io](https://hvp.akeyless.io)
      </td>
      <td>
        15.197.223.248, 3.33.244.138
      </td>
      <td>
        443
      </td>
      <td>
        * _Optional_* Public HVP endpoint
      </td>
    </tr>

    <tr>
      <td>
        **Logs**
      </td>
      <td>
        tcp://log.akeyless.io:9997  
        tcp://log.akeyless.io:9443
      </td>
      <td>
        35.192.171.171
      </td>
      <td>
        9997, 9443
      </td>
      <td>
        GW logs, mainly to be reflected during failure scenarios
      </td>
    </tr>

    <tr>
      <td>
        **CLI S3 Bucket**
      </td>
      <td>
        [https://akeyless-cli.s3.us-east-2.amazonaws.com](https://akeyless-cli.s3.us-east-2.amazonaws.com)
      </td>
      <td>
        N\A
      </td>
      <td>
        443
      </td>
      <td>
        S3 bucket to download & update Akeyless CLI versions
      </td>
    </tr>

    <tr>
      <td>
        **Services S3 Bucket**
      </td>
      <td>
        [https://akeylessservices.s3.us-east-2.amazonaws.com](https://akeylessservices.s3.us-east-2.amazonaws.com)
      </td>
      <td>
        N\A
      </td>
      <td>
        443
      </td>
      <td>
        S3 bucket to download & update Akeyless official binaries. e.g. `Gateway`
      </td>
    </tr>

    <tr>
      <td>
        **Artifacts Endpoint**
      </td>
      <td>
        [https://artifacts.site2.akeyless.io](https://artifacts.site2.akeyless.io)
      </td>
      <td>
        34.149.100.205
      </td>
      <td>
        443
      </td>
      <td>
        * _Optional_* Akeyless official artifacts endpoint. Relevant when working with whitelisted IP range
      </td>
    </tr>
  </tbody>
</Table>

> 👍 Note
>
> When using proxy services, you can use `sqs.us-east-2.amazonaws.com` instead of classic MQ services. In case you are not working with proxy serivce, and still want to utilize SQS insted of classic MQ , set your **Gateway**  deployment with the `SQS_NO_PROXY="true"` environment variable.

# Working without MQ Connection

If your organization's policies restrict non-web ports, it's important to understand the potential implications of blocking the MQ connection for your Akeyless setup:

* **Cross Gateway Access**: The MQ service enables retrieving Gateways secrets and objects (i.e. Dynamic/Rotated Secrets, Classic Keys, etc.) across different Gateways and the Akeyless SaaS console. If MQ is blocked, you can still retrieve those secrets directly from their own Gateway. However, requests from other Gateways or the SaaS console will not be processed.
* **Operational Adjustments**: Without the MQ service, you will need to ensure you are working directly with the correct Gateway for each relevant item. This may require additional manual oversight and adjustments compared to a setup with MQ enabled.
* **Centralized Management**: The MQ service allows for centralized management, enabling you to perform all operations from the SaaS console. If MQ is blocked, this convenience will not be available, and you will need to interact directly with individual Gateways.
* [Event Forwarding](https://docs.akeyless.io/docs/event-center#event-forwarders) relies on the MQ service for publishing event messages to the Gateway. Blocking the MQ connection will prevent event forwarding from working.