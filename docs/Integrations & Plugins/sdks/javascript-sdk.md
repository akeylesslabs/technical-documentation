---
title: JavaScript SDK
excerpt: This documentation suits Node.js and React.
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
The Akeyless [JavaScript](https://github.com/akeylesslabs/akeyless-javascript) makes it easy to integrate your **NodeJS** applications, libraries, or scripts with Akeyless. The following guide shows a typical integration.

# Installation

To install the **JavaScript SDK**  run: 

```shell
npm install akeyless --save
```

# Configuration

Create and configure an instance of Akeyless Client:

```javascript
const akeyless = require('akeyless');

const client = new akeyless.ApiClient();

client.basePath = 'https://api.akeyless.io';

const api = new akeyless.V2Api(client);
```

To work with Your [Gateway](https://docs.akeyless.io/docs/api-gw) set the `client.basePath` with your Gateway API endpoint on port `8081`.

# Authentication

The Akeyless **JavaScript** SDK supports multiple [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods). 

## Using cloud ID

To work with a Cloud-based Auth,  Add the Akeyless [Cloud ID library](https://github.com/akeylesslabs/akeyless-js-cloud-id) for **JavaScript**  and set the relevant `access-type` based on your cloud provide, the following example uses `azure_ad`:

```javascript
const akeyless = require('akeyless')
var akeylessCloud = require('akeyless-cloud-id')


const AkeylessClient = new akeyless.ApiClient();
AkeylessClient.basePath = 'https://api.akeyless.io';
const api = new akeyless.V2Api(AkeylessClient)


async function getSecret(key, opts) {
    try {
        const authResult = await api.auth(akeyless.Auth.constructFromObject(opts))
        const token = authResult.token

        const someObject = akeyless.GetSecretValue.constructFromObject({
            names: [key],
            token: token
        })
        const data = await api.getSecretValue(someObject)
        console.log('API called successfully. Returned data: ' + JSON.stringify(data))
        return JSON.stringify(data)
    } catch (e) {
        console.log(JSON.stringify(e, null, 2))
    }
}

async function getSecretWithCloudId() {
    const accessType = "azure_ad"
    const cloudId = await akeylessCloud.getCloudId(accessType)
    const opts = { 'access-id': "Access ID", 'access-type': accessType, 'cloud-id': cloudId }
    const secret = await getSecret("my-secret", opts)    
    console.log(secret)
}
    
getSecretWithCloudId()

```

Make sure to set your `Access Id` and `accessType` in the relevant places. The received token should be provided for every request that requires authentication.

# API Reference

For a detailed API reference, see [here](https://github.com/akeylesslabs/akeyless-javascript).
