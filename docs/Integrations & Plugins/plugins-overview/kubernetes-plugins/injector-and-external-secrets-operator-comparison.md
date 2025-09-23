---
title: Akeyless Injector Vs External Secrets Operator
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
The following is a comparison between the [External Secrets Operator](https://external-secrets.io/latest/) and the [Akeyless Injector](https://docs.akeyless.io/docs/how-to-provision-secret-to-your-k8s). Both solutions manage secrets in Kubernetes, but they differ in approach, storage, and security model.

# Akeyless K8s Secrets Injector

A solution that injects secrets into pods at runtime without storing them in Kubernetes secrets. Containers within the pod can consume those secrets without interacting with Akeyless. The injector is a Kubernetes 

[MutatingAdmissionWebhook](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#admission-control-extension-points:~:text=the%20cluster%20administrator.-,Admission%20control%20extension%20points,-Within%20the%20full) controller that modifies annotated pods, delivering secrets as environment variables or files via an init container.  Updates can be handled automatically using rollout restart.

<Image align="center" src="https://files.readme.io/ae1f338b176b05b4ffb15eecb0bee9fdfd0d2f9bc3389569f9c6cdeb79a95368-k8s-injection.jpg" />

# External Secrets Operator (ESO)

An open-source Kubernetes operator that integrates external secret managers like Akeyless. It fetches secrets via external APIs, converts them into Kubernetes Secrets, and stores them securely in the cluster storage. Automatic secret refresh is supported without changing the application,  also pushing secrets back to Akeyless is supported.

# Akeyless Injector vs. External Secrets Operator

<Image align="center" src="https://files.readme.io/143d329a383df21e1e4481289a4d1be018652093b525d21d77e2b6d758efa807-External_Secrets_Operator_1.jpg" />

The following table compares key aspects of the Akeyless Kubernetes Injector and the External Secrets Operator (ESO), focusing on how each solution handles secret management within Kubernetes environments.

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th>
        Feature
      </th>

      <th>
        Akeyless Injector
      </th>

      <th>
        External Secrets Operator
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        Secret Types
      </td>

      <td>
        [Static](https://docs.akeyless.io/docs/static-secrets)\
        [Rotated](https://docs.akeyless.io/docs/rotated-secrets)\
        [Dynamic](https://docs.akeyless.io/docs/how-to-create-dynamic-secret)\
        [Certificates](https://docs.akeyless.io/docs/certificate-lifecycle-management)\
        [USC](https://docs.akeyless.io/docs/universal-secrets-connector)
      </td>

      <td>
        [Static](https://docs.akeyless.io/docs/static-secrets)\
        [Rotated](https://docs.akeyless.io/docs/rotated-secrets)\
        [Dynamic](https://docs.akeyless.io/docs/how-to-create-dynamic-secret)\
        [Certificates](https://docs.akeyless.io/docs/certificate-lifecycle-management) 
      </td>
    </tr>

    <tr>
      <td>
        Authentication Methods
      </td>

      <td>
        [K8s](https://docs.akeyless.io/docs/kubernetes-auth)\
        [API Key](https://docs.akeyless.io/docs/api-key)\
        [Azure AD](https://docs.akeyless.io/docs/azure-ad)\
        [AWS\_IAM](https://docs.akeyless.io/docs/aws-iam)\
        [GCP](https://docs.akeyless.io/docs/gcp-auth-method)
      </td>

      <td>
        [K8s](https://docs.akeyless.io/docs/kubernetes-auth)\
        [API Key](https://docs.akeyless.io/docs/api-key)\
        [Azure AD](https://docs.akeyless.io/docs/azure-ad)\
        [AWS\_IAM](https://docs.akeyless.io/docs/aws-iam)\
        [GCP](https://docs.akeyless.io/docs/gcp-auth-method)  
      </td>
    </tr>

    <tr>
      <td>
        How secrets are fetched
      </td>

      <td>
        Secrets are injected into pods at runtime, and each pod requests the relevant secret it needs 
      </td>

      <td>
        Secrets are synced from external systems into [K8s Secret](https://kubernetes.io/docs/concepts/configuration/secret/) resources using a dedicated external secret resource per secret. All requests are done via the controller
      </td>
    </tr>

    <tr>
      <td>
        Access Control
      </td>

      <td>
        Access control is done via Akeyless RBAC, where different claims can be used to control the RBAC itself.
      </td>

      <td>
        Access control is done on Akeyless and on K8s itself, as it creates K8s secrets. In addition, due to the architecture of a single requestor, only the SA reference can be used in addition to limit access via Akeyless RBAC.
      </td>
    </tr>

    <tr>
      <td>
        Secret lifetime
      </td>

      <td>
        The secret exists only while the pod is running
      </td>

      <td>
        Secret stays in the cluster until it’s manually deleted
      </td>
    </tr>

    <tr>
      <td>
        K8s Integration type
      </td>

      <td>
        Seamless as K8s admission controller
      </td>

      <td>
        Uses a controller that interacts with K8s secret
      </td>
    </tr>

    <tr>
      <td>
        Secret storage location
      </td>

      <td>
        The secrets are injected directly into the pod.  Can be saved in a specific [location](https://docs.akeyless.io/docs/how-to-provision-secret-to-your-k8s#annotations-list:~:text=akeyless/inject_file%3A%20%22/mysecret/%7Clocation%3D/path%20to%20save%20secret%20name%22) with custom file permissions
      </td>

      <td>
        Secrets are stored as Kubernetes Secrets
      </td>
    </tr>

    <tr>
      <td>
        Secret Automatic Refresh
      </td>

      <td>
        Support of [rollout restart](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_restart/) upon any change of a secret, without periodic checks 
      </td>

      <td>
        [Periodic checks](https://external-secrets.io/latest/api/externalsecret/#:~:text=%23%20other%20fields...-,Periodic,-With%20refreshPolicy%3A%20Periodic) for secret changes (many requests) without auto detection. 
      </td>
    </tr>

    <tr>
      <td>
        Cache
      </td>

      <td>
        [Bypass cache](https://docs.akeyless.io/docs/how-to-provision-secret-to-your-k8s#annotations-list:~:text=akeyless/ignore_cache%3A%20%22true%22) is supported to fetch the latest secret value. This can be controlled globally for all deployments, to fetch the secret latest value, Can be controlled globally for all deployments, or explicitly.
      </td>

      <td>
        Not supported, in case the Gateway cache is used, first it will provide a cached version when it exists
      </td>
    </tr>

    <tr>
      <td>
        Observability and Monitoring
      </td>

      <td>
        All secret accesses are logged in the Akeyless audit logs, recording who accessed what, when, and from where, as well as telemetry metrics available
      </td>

      <td>
        All secrets access are logged in the Akelyess audit logs. ESO sends out K8s events when it syncs secrets, runs into errors while fetching them, or updates the status of an ExternalSecret.
      </td>
    </tr>

    <tr>
      <td>
        Deployment
      </td>

      <td>
        Deployed via a Helm chart. Supporting global settings in addition to the settings each deployment can be set with via [annotations](https://docs.akeyless.io/docs/how-to-provision-secret-to-your-k8s#annotations-list).
      </td>

      <td>
        Deployed via a Helm chart.\
        Uses K8s resources like [ExternalSecret](https://external-secrets.io/v0.5.1/api-externalsecret/), [SecretStore](https://external-secrets.io/v0.5.1/api-secretstore/), etc, to manage and settings.  
      </td>
    </tr>
  </tbody>
</Table>

<br />

# Conclusion

Kubernetes is not a secrets management solution. It does support native secrets storage, but those are not encrypted. It does come with a built-in RBAC model, but this is not easy to manage at scale and does not provide the same level of fine-grained policy control as Akeyless. Once a Kubernetes secrets are defined, they are stored in the Kubernetes storage server and presented to pods only during pod creation. meaning it is a common issue where secrets are being stale, outdated, or expired, requiring additional workflows to update and rotate the secrets, and then re-deploy the application to use the new version of the secrets.
