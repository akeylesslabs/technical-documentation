---
title: Update a Classic Key
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
You can update a classic key to change its name, add metadata, or add or remove tags.

The CLI command to update a classic key is:

```shell
akeyless gateway-update-item --gateway-url <Akeyless PAI GW URL> --name <classic key name> /
--new-name <new classic key name> /
--new-metadata <metadata>
```

where:

* **gateway-url:** The URL of the Akeyless Gateway. If you are working with your own Akeyless Gateway, set the value of this option as your Akeyless Gateway URL on port 8080. For example, `https://akeyless-gw:8080`.
* **name:** The name of the classic key to be updated. 
* **new-name:** The new name for the classic key (optional).
* **new-metadata:** The new metadata about the classic key (optional).
* **add tag:** The new tags to be attached to the classic key (optional).
* **rm-tag:** The tags to be removed from the classic key (optional).
* **auto-rotate:** Indicates if the classic key should be automatically rotated (`true`). If you do not enable automatic rotation, you can rotate the key manually.

The full list of options for this command is:

```shell
-u, --gateway-url[=http://localhost:8000]   Akeyless Gateway URL (Configuration Management port)
-n, --name                                 *Item name
-t, --type                                 *Item type; options: [classic-key, rotated-secret]
    --new-name                              New item name
    --new-metadata[=default_metadata]       New item metadata
    --add-tag                               List of the new tags that will be attached to this item. To specify multiple tags use argument multiple times: --add-tag Tag1 --add-tag Tag2
    --rm-tag                                List of the existent tags that will be removed from this item. To specify multiple tags use argument multiple times: --rm-tag Tag1 --rm-tag Tag2
    --auto-rotate                           [true/false] Sets automatic rotation to be enabled or disabled, if enabled rotation will be triggered periodically based on --rotation-interval
    --rotation-interval                     The number of days to wait between every automatic key rotation (1-365)
    --rotation_hour[=0]                     The Hour of the rotaion in UTC (relevant only for --type=rotated-secret)
    --rotator_creds_type[=use-self-creds]   The credentials to connect with use-self-creds/use-target-creds (relevant only for --type=rotated-secret)
    --new-version[=false]                   Whether to create a new version of not (relevant only for --type=rotated-secret)
-k, --key                                   The name of the key that protects the item value (if empty, the account default key will be used)
    --profile                               Use a specific profile from your akeyless/profiles/ folder
    --username                              Optional username for various authentication flows
    --password                              Optional password for various authentication flows
    --uid-token                             The universal identity token, Required only for universal_identity authentication
-h, --help                                  display help information
    --json[=false]                          Set output format to JSON
    --no-creds-cleanup[=false]              Do not clean local temporary expired creds
```
