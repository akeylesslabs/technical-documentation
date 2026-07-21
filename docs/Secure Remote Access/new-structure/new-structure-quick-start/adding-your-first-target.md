---
title: adding your first target
deprecated: false
hidden: false
metadata:
  robots: index
---
add a guide with reference to [Resource Types](doc:new-structure-resource-types)

<br /><br />

Then run `kubectl get services` and look for the `EXTERNAL-IP` of the service starting with `quick-start-gw`. Copy the `EXTERNAL-IP` and paste that into your browser with port 8000/console (for example, `http://<Your-Akeyless-GW-URL>:8000/console`). If you get the login page, you have successfully deployed the Gateway!

#### Gateway URLs

For the Gateway, you can access the following:

- The Gateway's Internal Console is located at `http://<Your-Akeyless-GW-URL>:8000/console`. The internal console means you are working from inside the Gateway and talking directly with the SaaS. If you are using `https://console.akeyless.io`, you will not be able to interact with this Gateway as it is not secured with TLS.

#### Remote Access URLs

For Remote Access, you can access the following:

- The Remote Access Internal Web Portal is located at `http://<Your-Akeyless-GW-URL>:8000/sra/portal`

- Remote Access can also be accessed using our public URL: `https://zerotrust.akeyless.io`. If you are using the public URL for RDP, Web, or similar sessions, you will be required to add your Web URL endpoint: `http://<Your-Akeyless-GW-URL>:8000/sra/web-client`

## Testing Out Remote Access

Here we will lay out the steps to get a SAML user to access the Remote Access Portal.

1. Firstly, you need to make sure you have your SAML application set up, for example, an Okta account set up with the Akeyless application configured. You will also need to retrieve your Metadata URL for this.

2. Next, run the following command to create your SAML Auth Method and make sure to input your Kubernetes Service External-IP address:

   ```shell
   akeyless auth-method create saml --name mySamlAuth --unique-identifier email --idp-metadata-url <your-okta-metadata-url> --allowed-redirect-uri https://console.akeyless.io/login-saml,http://127.0.0.1:*,http://<EXTERNAL-IP-of-K8s-Service>:*
   ```

3. Create a role with access to Items with Secure Remote Access with Allow Access permissions.

   ```shell
   akeyless set-role-rule --role-name MySamlRole --path "/\*" --rule-type sra-rule --capability allow_access
   ```

4. Associate your Auth Method as follows:

   ```shell
   akeyless assoc-role-am --role-name MySamlRole --am-name MySamlAuth
   ```

5. Next, open your browser and go to your Remote Access internal endpoint: `http://<Your-Akeyless-GW-URL>:8000/sra/portal`

6. Enter your SAML AccessID and click “Sign In”. You will be redirected to your SAML service login page to log in and then when you finish that will redirect you to a page with various resources you can set at a later time.

## Next Steps

With a Gateway deployed, you can now test out using just-in-time [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) for various applications and services by setting up [Targets](https://docs.akeyless.io/docs/targets). If you are also using Remote Access, you can also set up Remote Access on those Targets and log into those [Resources](https://docs.akeyless.io/docs/supported-resource-types) securely from anywhere by [reading the docs](https://docs.akeyless.io/docs/sra-overview).<br /><br />

- [Admin Guides](https://docs.akeyless.io/docs/sra-admin-guides)

- [Accessing Resources](https://docs.akeyless.io/docs/sra-accessing-resources)

<br />
