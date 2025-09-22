---
title: Venafi Target
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
**Venafi** Target can be used with the Venafi Dynamic Secret as described under the [Venafi Integration](doc:venafi-integration) docs.

# Create a Venafi Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Certificate Automation (Venafi)**.

2. Define the Name of the target, and specify the Location as a path to the virtual folder where you want to create the new target, using the slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.  
   For more information, [read here](doc:implement-zero-knowledge).

4. Choose your preferred Venafi target type by selecting one of the options:

   - **Venafi Cloud** Or **Trust Protection Platform**.

   - For **Venafi Cloud**  set the following:

     - **API Key:** The API key to use when connecting to a Venafi Cloud environment.

     - **Zone:** The Venafi zone to use when issuing new certificates (policies will be pulled from here) - for example: `<Application_Name>/<Issuing_template_name>`

     - **Base URL:** Base URL of the Venafi Cloud environment (Default is <https://venafi.cloud/>).

   - For  **Trust Protection Platform** set the following:

     - **Access Token:** Venafi Access Token to use to access the TPP environment

     - **Refresh Token:** Venafi Refresh Token to use when the Access Token is expired

     - **Client ID:**  Default is `akeyless`.

     - **Zone:** The zone to use when issuing new certificates (policies will be pulled from here).

     - **Base URL:** Base URL of the Trusted Protection Platform environment.

5. Click **Finish**.