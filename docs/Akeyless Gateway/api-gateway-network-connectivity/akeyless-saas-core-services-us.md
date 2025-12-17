---
title: US SaaS Core Services
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
The following table describes the main functionality of Akeyless microservices in the **US** environment:

<Table align={["left","left","left","left","left"]}>
  <thead>
    <tr>
      <th style={{ textAlign: "left" }}>
        Service
      </th>

      <th style={{ textAlign: "left" }}>
        Endpoint
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
        `https://console.us.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        4.242.224.82
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
        Vault
      </td>

      <td style={{ textAlign: "left" }}>
        `https://vault.us.akeyless.io`,
        `https://vault-ro.us.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        68.154.26.48,
        4.242.224.82
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
        `https://auth.us.akeyless.io`, `https://auth-ro.us.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        68.154.26.48, 4.242.224.82
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
        `https://auth-cert.us.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        172.206.81.32
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
        `https://audit.us.akeyless.io`, `https://audit-ro.us.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        68.154.26.48, 4.242.224.82
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
        `https://bis.us.akeyless.io`, `https://bis-ro.us.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        68.154.26.48, 4.242.224.82
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
        `https://gator.us.akeyless.io`, `https://gator-ro.us.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        68.154.26.48, 4.242.224.82
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
        `amqps://mq.us.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        172.177.144.122
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

        [https://kfm1.us.akeyless.io](https://kfm1.us.akeyless.io),
        [https://kfm1-ro.us.akeyless.io](https://kfm1-ro.us.akeyless.io),
        [https://kfm2.us.akeyless.io](https://kfm2.us.akeyless.io),
        [https://kfm2-ro.us.akeyless.io](https://kfm2-ro.us.akeyless.io),
        [https://kfm3.us.akeyless.io](https://kfm3.us.akeyless.io),
        [https://kfm3-ro.us.akeyless.io](https://kfm3-ro.us.akeyless.io),
        [https://kfm4.us.akeyless.io](https://kfm4.us.akeyless.io),
        [https://kfm4-ro.us.akeyless.io](https://kfm4-ro.us.akeyless.io)
      </td>

      <td style={{ textAlign: "left" }}>

      </td>

      <td style={{ textAlign: "left" }}>
        68.154.26.48,
        4.242.224.82
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
        `https://rest.us.akeyless.io`, `https://api.us.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        68.154.26.48,
        4.242.224.82
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
        Public HVP
      </td>

      <td style={{ textAlign: "left" }}>
        `https://hvp.us.akeyless.io`
      </td>

      <td style={{ textAlign: "left" }}>
        68.154.26.48
      </td>

      <td style={{ textAlign: "left" }}>

      </td>

      <td style={{ textAlign: "left" }}>
        Optional Public HVP endpoint
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
        N/A
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
        Akeyless CLI
      </td>

      <td style={{ textAlign: "left" }}>
        `https://akeyless-cli.s3.us-east-2.amazonaws.com`
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
        Akeyless Binaries
      </td>

      <td style={{ textAlign: "left" }}>
        `https://akeylessservices.s3.us-east-2.amazonaws.com`
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

<br />
