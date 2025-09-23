---
title: Slack Plugin
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
A **One-time Password** (OTP), also known as a one-time PIN, is a password valid for only one login session or transaction, on a computer system or other digital device. Akeyless can be used as a **Slack** app to share **OTP** easily inside your Organization **Slack** account.

# Configuration

Slack [Slash Commands](https://api.slack.com/interactivity/slash-commands) allows users to invoke the Akelyess app by typing a `/akeyless` into the message composer box. By enabling Slash Commands, the Akelyess app can be summoned by users from any conversation in Slack. 

To Set the Slash command a workspace admin shall perform the following configuration: 

**Command** - the name of the command, set to `/akeyless`

**Request URL** - the URL we'll send a payload to, when the command is invoked by a user. Set to `https://sfs.akeyless-security.com`

Short Description - exactly what it sounds like, a short description of what your command does. e.g. `AKEYLESS Secrets Management`

<Image align="center" src="https://files.readme.io/3b3858f-IMG_1834.JPG" />

![](https://files.readme.io/4664042-Screen_Shot_2020-04-30_at_11.27.35.png "Screen Shot 2020-04-30 at 11.27.35.png")

# Using AKEYLESS OTP via Slack

Type `/akeyless` in Slack and select the **OTP** option: 

![](https://files.readme.io/e318cfb-image.png)

Type in the content of the message you'd like to send for example:

`/akeyless Secret Management Reimangined`

Once sending the message, click `Yes` to share the secret **OTP**  in the Slack channel, A URL will be shared with the recipient.

Clicking on the **OTP** URL will allow the view of the secret only for a one-time.

![](https://files.readme.io/2e597b7-image.png)
