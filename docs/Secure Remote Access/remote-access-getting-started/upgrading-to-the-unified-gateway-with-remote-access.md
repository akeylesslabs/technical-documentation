---
title: Upgrading to the Unified Gateway with Remote Access
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
The new, unified version of the Akeyless Gateway introduces significant improvements in deployment, configuration, and capabilities, intended to simplify Gateway and Remote Access deployment and operation and extend functionality.

> 📘 New Helm Chart
>
> With this new version comes a new Helm chart for K8s deployments. We have created a doc to explain what changed and how. You can see it at [this link](https://github.com/akeylesslabs/helm-charts/blob/main/charts/akeyless-gateway/values.yaml).

## Why Upgrade to the Unified Gateway & Remote Access Version?

This unified version of the Gateway has built-in Remote Access, which offers many benefits to customers in terms of ease of deployment, dynamic configuration, and feature availability, among others:

### Ease of Deployment and Configuration

As a single, unified deployment, Remote Access now comes with the Gateway in a single, coherent configuration file which is much easier to set up and configure. Much of the advanced configuration can be done after the initial basic deployment from within the UI.

### Fewer Overlapping of Parameters in the Helm Chart

In the previous Helm chart, there were overlapping parameters which made the setup and management process complicated. In the unified version, we cleaned up the Helm chart to avoid those redundancies and give users a much more seamless experience with less headache.

### Dynamic Updates from Console UI

The latest version of the Gateway allows administrators to directly apply most of the configuration updates through the Console UI instead of redeploying the chart. This capability reduces downtime, enabling faster rollout so users can simply continue working with the latest updates.

### Access to Enhanced Features and Capabilities

The unified edition introduces powerful new Remote Access functionalities that will only be available in this unified environment, such as [Session Management](doc:remote-access-session-management) capabilities, which enable managers and auditors to better control and monitor activities involving remote access, adding another layer of security and compliance.

## What Does the Unification Include?

The unified deployment of Gateway and Remote Access offers multiple configurations to meet organizational needs for different purposes:

1. **Flexible Deployment Options of Gateway**\
   Organizations have the ability to deploy a Gateway with or without the Remote Access component.

2. **Supports Kubernetes and Docker Compose Deployments**\
   The unified version supports both the Kubernetes and Docker Compose deployments. For Kubernetes, the deployment consists of different services and pods for each component (gateway, web remote access, ssh remote access).\
   For users only leveraging the Gateway in a standalone deployment, they can simply configure the Helm Chart with `SRA=false`, or deploy standalone via Docker Compose.

3. **Planning the Migration**\
   There is no direct upgrade path from the legacy separate Gateway and Remote Access deployments to the unified version. A planned migration is essential, and we strongly recommend scheduling the upgrade to minimize operational disruptions and ensure a seamless transition for your users. For detailed information on changes introduced during the unification process, refer to the document outlining all [Helm chart modifications](https://docs.akeyless.io/docs/helm-chart-changes-and-enhancements).

4. **Unification of endpoints (ports)**\
   The unified Gateway with Remote Access has simplified access to the various components by creating internal mapping of the endpoints. All endpoints can be accessed through the Gateway as follows:

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th>Service</th>
      <th>Old Port</th>
      <th>New Port/Endpoint</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Gateway Configuration Manager](https://docs.akeyless.io/docs/gateway-configuration-manager)</td>
      <td>8000</td>
      <td>8000</td>
    </tr>
    <tr>
      <td>Akeyless Gateway Console</td>
      <td>1888</td>
      <td>&lt;gateway-url&gt;:8000/console</td>
    </tr>
    <tr>
      <td>Remote Access Portal</td>
      <td>-</td>
      <td>&lt;gateway-url&gt;:8000/sra/portal</td>
    </tr>
    <tr>
      <td>Remote Access Web Client</td>
      <td>8888</td>
      <td>&lt;gateway-url&gt;:8000/sra/web-client</td>
    </tr>
    <tr>
      <td>Remote Access SSH Config</td>
      <td>9900</td>
      <td>&lt;gateway-url&gt;:8000/sra/ssh-config</td>
    </tr>
    <tr>
      <td>HVP</td>
      <td>8200</td>
      <td>&lt;gateway-url&gt;:8000/hvp</td>
    </tr>
    <tr>
      <td>Akeyless V1 REST API</td>
      <td>8080</td>
      <td>&lt;gateway-url&gt;:8000/api/v1</td>
    </tr>
    <tr>
      <td>Akeyless V2 REST API</td>
      <td>8081</td>
      <td>&lt;gateway-url&gt;:8000/api/v2</td>
    </tr>
    <tr>
      <td>KMIP Server</td>
      <td>5696</td>
      <td>5696</td>
    </tr>
    <tr>
      <td>GRPC</td>
      <td>8085</td>
      <td>8085</td>
    </tr>
  </tbody>
</Table>

<br />

## Additional Notes

### Zero Trust Web Access Solution

The unification of the Zero Trust Web Access (ZTWA) component with the Gateway is part of our roadmap. You will be able to continue working with the unified Gateway and ZTWA solution without any impact on operations.

With this timeline, an organization can adopt a unified version of SRA now with a clear understanding that enhanced web access functionality will be available in the near term.