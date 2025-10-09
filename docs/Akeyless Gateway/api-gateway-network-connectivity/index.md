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
> Available explicit tenants are: `us`,`eu` .

The following table describes the main functionality of Akeyless microservices in the global environment:

<Table align={["left","left","left","left","left"]}>
  <thead>
    <tr>
      <th style={{ textAlign: "left" }}>
        Service
      </th>

      <th style={{ textAlign: "left" }}>
        Endpoints
      </th>

      <th style={{ textAlign: "left" }}>
        IP
      </th>

      <th style={{ textAlign: "left" }}>
        Port
      </th>

      <th style={{ textAlign: "left" }}>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{ textAlign: "left" }}>
        Console
      </td>

      <td style={{ textAlign: "left" }}>
        `https://console.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128
      </td>

      <td style={{ textAlign: "left" }}>
        443
      </td>

      <td style={{ textAlign: "left" }}>
        Akeyless SaaS platform
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Vault
      </td>

      <td style={{ textAlign: "left" }}>
        `https://vault.akeyless.io`, `https://vault-ro.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128
      </td>

      <td style={{ textAlign: "left" }}>
        443
      </td>

      <td style={{ textAlign: "left" }}>
        User Account Management (UAM), managing user accounts, items, and roles
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Auth
      </td>

      <td style={{ textAlign: "left" }}>
        `https://auth.akeyless.io`, `https://auth-ro.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128
      </td>

      <td style={{ textAlign: "left" }}>
        443
      </td>

      <td style={{ textAlign: "left" }}>
        Akeyless Authentication service
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Certificate Auth
      </td>

      <td style={{ textAlign: "left" }}>
        `https://auth-cert.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        18.189.176.104
      </td>

      <td style={{ textAlign: "left" }}>
        443
      </td>

      <td style={{ textAlign: "left" }}>
        Relevant only for Certificate Based Auth
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Audit
      </td>

      <td style={{ textAlign: "left" }}>
        `https://audit.akeyless.io`, `https://audit-ro.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128
      </td>

      <td style={{ textAlign: "left" }}>
        443
      </td>

      <td style={{ textAlign: "left" }}>
        Audit log main service, enables log forwarding from GW & Bastion
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        BIS
      </td>

      <td style={{ textAlign: "left" }}>
        `https://bis.akeyless.io`, `https://bis-ro.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        52.223.11.194, 35.71.185.167
      </td>

      <td style={{ textAlign: "left" }}>
        443
      </td>

      <td style={{ textAlign: "left" }}>
        Billing Infrastructure Service (BIS)
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Gator
      </td>

      <td style={{ textAlign: "left" }}>
        `https://gator.akeyless.io`,
        `https://gator-ro.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128
      </td>

      <td style={{ textAlign: "left" }}>
        443
      </td>

      <td style={{ textAlign: "left" }}>
        Main service to sync gateways instances, and connections with Akeyless SaaS
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        MQ
      </td>

      <td style={{ textAlign: "left" }}>
        `amqps://mq.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        52.223.11.194, 35.71.185.167
      </td>

      <td style={{ textAlign: "left" }}>
        5671
      </td>

      <td style={{ textAlign: "left" }}>
        Message queue between Akeyless micro-services
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        KFM
      </td>

      <td style={{ textAlign: "left" }}>
        `https://kfm1.akeyless.io`,
        `https://kfm1-ro.akeyless.io`,
        `https://kfm2.akeyless.io`,
        `https://kfm2-ro.akeyless.io`,
        `https://kfm3.akeyless.io`,
        `https://kfm3-ro.akeyless.io`,
        `https://kfm4.akeyless.io`,
        `https://kfm4-ro.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128, 34.120.160.242
      </td>

      <td style={{ textAlign: "left" }}>
        443
      </td>

      <td style={{ textAlign: "left" }}>
        Key Fragments Services, enabling full DFC encryption
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Public Gateway
      </td>

      <td style={{ textAlign: "left" }}>
        `https://rest.akeyless.io`, `https://api.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        15.197.223.248, 3.33.244.138
      </td>

      <td style={{ textAlign: "left" }}>
        443
      </td>

      <td style={{ textAlign: "left" }}>
        _Optional_* Public Gateway rest API v1\v2
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Public HVP
      </td>

      <td style={{ textAlign: "left" }}>
        `https://hvp.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        15.197.223.248, 3.33.244.138
      </td>

      <td style={{ textAlign: "left" }}>
        443
      </td>

      <td style={{ textAlign: "left" }}>
        _Optional_* Public HVP endpoint
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Logs
      </td>

      <td style={{ textAlign: "left" }}>
        `tcp://log.akeyless.io:9997`, `tcp://log.akeyless.io:9443`
      </td>

      <td style={{ textAlign: "left" }}>
        35.192.171.171
      </td>

      <td style={{ textAlign: "left" }}>
        9997, 9443
      </td>

      <td style={{ textAlign: "left" }}>
        GW logs, mainly to be reflected during failure scenarios
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        CLI S3 Bucket
      </td>

      <td style={{ textAlign: "left" }}>
        `https://akeyless-cli.s3.us-east-2.amazonaws.com`
      </td>

      <td style={{ textAlign: "left" }}>
        N\A
      </td>

      <td style={{ textAlign: "left" }}>
        443
      </td>

      <td style={{ textAlign: "left" }}>
        S3 bucket to download & update Akeyless CLI versions
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Services S3 Bucket
      </td>

      <td style={{ textAlign: "left" }}>
        `https://akeylessservices.s3.us-east-2.amazonaws.com`
      </td>

      <td style={{ textAlign: "left" }}>
        N\A
      </td>

      <td style={{ textAlign: "left" }}>
        443
      </td>

      <td style={{ textAlign: "left" }}>
        S3 bucket to download & update Akeyless official binaries. e.g. `Gateway`
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Artifacts Endpoint
      </td>

      <td style={{ textAlign: "left" }}>
        `https://artifacts.site2.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        34.149.100.205
      </td>

      <td style={{ textAlign: "left" }}>
        443
      </td>

      <td style={{ textAlign: "left" }}>
        _Optional_* Akeyless official artifacts endpoint. Relevant when working with whitelisted IP range
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
