---
title: Splunk Target
deprecated: false
hidden: false
metadata:
  robots: index
---
You can define a [Splunk](https://www.splunk.com/en_us/download/splunk-enterprise.html?utm_campaign=google_emea_tier2_en_search_brand\&utm_source=google\&utm_medium=cpc\&utm_content=Splunk_Enterprise_Demo_v3\&utm_term=splunk\&device=c&_bt=749641715948&_bm=e&_bn=g\&gad_source=1\&gad_campaignid=765667359\&gbraid=0AAAAAD8kDz01Bo05Utq98bmNZ9PT40XU1\&gclid=Cj0KCQiAhaHMBhD2ARIsAPAU_D5vrBDoul26TzPrN7Ou4DGjLqCR4evXv99YFM0zdSqK7tdGP-1TNxoaAh8GEALw_wcB) target to be used with Splunk Rotated Secret.

## Create a Splunk Target with the CLI

To create a Splunk target with the CLI, run the following command:

```shell
akeyless target create splunk \
--name <Target Name> \
--url <Server URL> \
--username <Splunk Username>
--password <Splunk Password>
--token <Splunk Token>
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `url`: The Splunk server URL.

* `api-key`: The Admin API Key that will be used in order to create the API Key.

* `username`:  The Splunk Username.

* `password`: The Splunk Password.

* `token`: The Splunk Token.

You can find the complete list of parameters for this command in the CLI Reference - Targets section.

## Create a Splunk Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Infra (Splunk)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
   For more information, [read here](https://docs.akeyless.io/docs/implement-zero-knowledge).

4. Define the remaining parameters as follows:

   * **Splunk URL:** The **Splunk** server URL.

   * **Auth Mode**: In this section, you can select the preferred type of authentication with the Splunk server either `Username` or `Token`:
     * Select the **Username** option to authenticate with **Username** and **Password**
     * Select the **Token** option to authenticate with a **token**.

   * **TLS**: Enable this option to use a **secure (TLS) connection**.

   * **Certificate**: Upload a certificate to secure the connection if one doesn’t already exist.