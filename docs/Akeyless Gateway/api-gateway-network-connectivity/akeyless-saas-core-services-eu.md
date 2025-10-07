---
title: EU SaaS Core Services
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
The following table describes the main functionality of Akeyless microservices in the **EU** environment:

<Table align={["left","left","left","left"]}>
  <thead>
    <tr>
      <th style={{ textAlign: "left" }}>
        **Service**
      </th>

      <th style={{ textAlign: "left" }}>
        **IP**
      </th>

      <th style={{ textAlign: "left" }}>
        **Port**
      </th>

      <th style={{ textAlign: "left" }}>
        **Description**
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{ textAlign: "left" }}>
        **Console:**

        [https://console.eu.akeyless.io](https://console.eu.akeyless.io)
      </td>

      <td style={{ textAlign: "left" }}>
        13.248.216.215,
        76.223.80.182
      </td>

      <td style={{ textAlign: "left" }}>
        443
      </td>

      <td style={{ textAlign: "left" }}>
        Akeyless SaaS Platform
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        **Vault:**

        [https://vault.eu.akeyless.io](https://vault.eu.akeyless.io)
        [https://vault-ro.eu.akeyless.io](https://vault-ro.eu.akeyless.io)
      </td>

      <td style={{ textAlign: "left" }}>
        3.33.166.129,
        15.197.166.202
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
        **Auth:**

        [https://auth.eu.akeyless.io](https://auth.eu.akeyless.io)
        [https://auth-ro.eu.akeyless.io](https://auth-ro.eu.akeyless.io)
      </td>

      <td style={{ textAlign: "left" }}>
        3.33.166.129,
        15.197.166.202,
        13.248.216.215,
        76.223.80.182
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
        **Certificate Auth:**

        [https://auth-cert.eu.akeyless.io](https://auth-cert.eu.akeyless.io)
      </td>

      <td style={{ textAlign: "left" }}>
        18.158.96.32,
        3.68.125.9,
        52.28.6.110
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
        **Audit:**

        [https://audit.eu.akeyless.io](https://audit.eu.akeyless.io)
        [https://audit-ro.eu.akeyless.io](https://audit-ro.eu.akeyless.io)
      </td>

      <td style={{ textAlign: "left" }}>
        15.197.166.202,
        3.33.166.129,
        13.248.216.215,
        76.223.80.182
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
        **BIS:**

        [https://bis.eu.akeyless.io](https://bis.eu.akeyless.io)
        [https://bis-ro.eu.akeyless.io](https://bis-ro.eu.akeyless.io)
      </td>

      <td style={{ textAlign: "left" }}>
        15.197.166.202,
        3.33.166.129
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
        **Gator:**

        [https://gator.eu.akeyless.io](https://gator.eu.akeyless.io)
        [https://gator-ro.eu.akeyless.io](https://gator-ro.eu.akeyless.io)
      </td>

      <td style={{ textAlign: "left" }}>
        3.33.166.129,
        15.197.166.202,
        76.223.80.182,
        13.248.216.215
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
        **MQ:**

        amqps://mq.eu.akeyless.io
      </td>

      <td style={{ textAlign: "left" }}>
        15.197.166.202,
        3.33.166.129
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
        **KFM:**

        [https://kfm1.eu.akeyless.io](https://kfm1.eu.akeyless.io),
        [https://kfm1-ro.eu.akeyless.io](https://kfm1-ro.eu.akeyless.io),
        [https://kfm2.eu.akeyless.io](https://kfm2.eu.akeyless.io),
        [https://kfm2-ro.eu.akeyless.io](https://kfm2-ro.eu.akeyless.io),
        [https://kfm3.eu.akeyless.io](https://kfm3.eu.akeyless.io),
        [https://kfm3-ro.eu.akeyless.io](https://kfm3-ro.eu.akeyless.io),
        [https://kfm4.eu.akeyless.io](https://kfm4.eu.akeyless.io),
        [https://kfm4-ro.eu.akeyless.io](https://kfm4-ro.eu.akeyless.io)
      </td>

      <td style={{ textAlign: "left" }}>
        3.33.166.129,
        15.197.166.202,
        76.223.80.182,
        13.248.216.215
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
        **Public Gateway:**

        [https://rest.eu.akeyless.io](https://rest.eu.akeyless.io)
        [https://api.eu.akeyless.io](https://api.eu.akeyless.io)
      </td>

      <td style={{ textAlign: "left" }}>
        3.33.196.150,
        15.197.225.215
      </td>

      <td style={{ textAlign: "left" }}>
        443
      </td>

      <td style={{ textAlign: "left" }}>
        Optional Public Gateway rest API v1\v2
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        **Public HVP:**

        [https://hvp.eu.akeyless.io](https://hvp.eu.akeyless.io)
      </td>

      <td style={{ textAlign: "left" }}>
        3.33.196.150,
        15.197.225.215
      </td>

      <td style={{ textAlign: "left" }}>
        443
      </td>

      <td style={{ textAlign: "left" }}>
        Optional Public HVP endpoint
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        **Logs:**

        tcp://log.eu.akeyless.io:9997 tcp://log.eu.akeyless.io:9443
      </td>

      <td style={{ textAlign: "left" }}>
        3.124.145.245
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
        [https://akeyless-cli.s3.us-east-2.amazonaws.com](https://akeyless-cli.s3.us-east-2.amazonaws.com)
      </td>

      <td style={{ textAlign: "left" }}>
        N/A
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
        [https://akeylessservices.s3.us-east-2.amazonaws.com](https://akeylessservices.s3.us-east-2.amazonaws.com)
      </td>

      <td style={{ textAlign: "left" }}>
        N/A
      </td>

      <td style={{ textAlign: "left" }}>
        443
      </td>

      <td style={{ textAlign: "left" }}>
        S3 bucket to download & update Akeyless official binaries. e.g. `Gateway`
      </td>
    </tr>
  </tbody>
</Table>

> 👍 Note
>
> When using proxy services, you can use **[https://sqs.eu-central-1.amazonaws.com](https://sqs.eu-central-1.amazonaws.com)** instead of classic MQ services. In case you are not working with proxy service, and still want to utilize SQS instead of classic MQ, set your **Gateway**  deployment with the `SQS_NO_PROXY="true"` environment variable.
