---
title: Break-Glass Access Best Practices
deprecated: false
hidden: false
metadata:
  robots: index
---
In scenarios requiring emergency or "break-glass" access to critical systems or secrets, it is essential to implement robust security measures to minimize risks while ensuring availability. Akeyless recommends configuring a dedicated Authentication Method (Auth Method) specifically for break-glass purposes. Below are key best practices to enhance the security of this Auth Method:

## Additional Protections for Break-Glass Auth Methods

To safeguard against unauthorized use, apply layered controls to the dedicated Auth Method:

* IP Range Restrictions: Limit access to the Auth Method by configuring it to accept authentication attempts only from a predefined IP address range. This ensures that break-glass access can only be initiated from trusted locations, such as a secure operations center or specific on-premises networks.
* High-Level Alerting: Enable monitoring and alerting mechanisms to trigger notifications (e.g., via email, Slack, or integrated SIEM tools) whenever the break-glass Auth Method is accessed. This provides immediate visibility into emergency usage, allowing for rapid response and audit.

## Dual-Control Authentication with MFA

For heightened security, consider using a **User and Password** Auth Method combined with Multi-Factor Authentication (MFA). To enforce the separation of duties and prevent single-point compromise:

* Split the credentials across multiple individuals or groups. For example:
* Assign the password to one trusted user or team.
* Assign control of the MFA factor (e.g., email-based OTP or authenticator app) to a different user or team.

This setup requires collaboration between at least two parties to authenticate successfully, reducing the risk of insider threats or unauthorized access.

Implementing these practices ensures that break-glass access remains a secure, last-resort option while aligning with compliance requirements such as least privilege and auditability. For configuration details, refer to the [Authentication Methods](https://docs.akeyless.io/docs/understanding-authentication) section. If you encounter specific use cases, contact Akeyless support for tailored guidance.

<br />
