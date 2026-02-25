---
title: KMIP for vSphere
excerpt: Add a KMS to vCenter Server in vSphere Web Client
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
## Create a KMIP Client on Akeyless Gateway

1. From the Akeyless CLI, enable the KMIP server:

    ```shell
    akeyless kmip-server-setup --hostname <akeyless.gateway.hostname> --gateway-url <Your_Akeyless_GW_URL> --root /kmip/default
    ```

2. Create KMIP client:

    ```shell
    akeyless kmip-create-client --name myVCenter --gateway-url <Your_Akeyless_GW_URL>
    ```

    This returns the `client ID`, `private key` and `certificate`:

    ```shell
    $ New client successfully created.
    Client ID: Zvzw0...VM2u
    Client Key:
    -----BEGIN RSA PRIVATE KEY-----
    MIIEpA...yRCF8UQ==
    -----END RSA PRIVATE KEY-----

    Client Certificate:
    -----BEGIN CERTIFICATE-----
    MIIDSz...0otOEQQ==
    -----END CERTIFICATE-----
    ```

3. Save the received certificate and key in a safe place. They will be used to set up the connection.

4. By default, KMIP clients have no permissions. To grant your KMIP client minimal access permissions, execute the following command:

    ```shell
    akeyless kmip-client-set-rule --gateway-url <Your_Akeyless_GW_URL> --client-id <From step 2, kc-TmA3...VM2u> \
        --path "/*" \
        --capability CREATE \
        --capability GET \
        --capability GET_ATTRIBUTES \
        --capability ACTIVATE
    ```

## vCenter Server Setup

1. Log in to the vCenter Server system with the vSphere Web Client.

2. Browse the inventory list and select the vCenter Server instance.

3. Click **Configure**, then click **Key Management Servers**.

    ![Illustration for: 3. Click Configure, then click Key Management Servers.](https://files.readme.io/376043b-image-20210914-151429.png)

4. Click **Add KMS**. For **Server address**, supply your Akeyless Gateway address, for **Server port**, use 5696. Click **Add**.

    ![Illustration for: 4. Click Add KMS. For Server address, supply your Akeyless Gateway address. For Server port, use 5696. Click Add.](https://files.readme.io/557d218-image-20210914-1519061.png)

5. Extend the new line and click **Make KMS Trusted vCenter**:

    ![Illustration for: 5. Extend the new line and click Make KMS Trusted vCenter.](https://files.readme.io/2b8e7a9-image-20210914-152306.png)

6. For a method, choose **KMS certificate and private key**:

    ![Illustration for: 6. For a method, choose KMS certificate and private key.](https://files.readme.io/4d64c95-image-20210914-152556.png)

7. For **KMS Certificate** and **KMS Private key**, set the certificate and private key, and click **Establish Trust**:

    ![Illustration for: 7. For the KMS Certificate and KMS Private key set the certificate and the Private Key and click Establish Trust.](https://files.readme.io/e797dc2-image-20210914-154420.png)

8. Extend the new line again and click **Make vCenter Trust KMS**:

    ![Illustration for: 8. Extend the new line again and click Make vCenter Trust KMS.](https://files.readme.io/828fb11-image-20210914-154614.png)

9. In the dialog, click **TRUST**:

    ![Illustration for: 9. In the dialog, click TRUST.](https://files.readme.io/26a46cb-image-20210914-154645.png)

10. Verify all statuses are valid:  

    ![Illustration for: 10. Verify all statuses are valid.](https://files.readme.io/35653e2-image-20210914-154951.png)

[Read more about **Enabling Host Encryption Mode in vSphere**](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere-sdks-tools/7-0/web-services-sdk-programming-guide/virtual-machine-security/prerequisites-and-required-privileges-for-encryption-tasks/host-encryption-mode.html).
