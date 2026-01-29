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

## Configuration

Slack [Slash Commands](https://api.slack.com/interactivity/slash-commands) allows users to invoke the Akeyless app by typing a `/akeyless` in the message field. By enabling Slash Commands, the Akeyless app can be summoned by users from any conversation in Slack.

To Set the Slash command a workspace admin shall perform the following configuration:

**Command** - the name of the command, set to `/akeyless`

**Request URL** - the URL we'll send a payload to, when the command is invoked by a user. Set to `https://sfs.akeyless-security.com`

Short Description - exactly what it sounds like, a short description of what your command does, for example, `Akeyless Secrets Management`

![Screenshot of the Slack Console for Editing a Slash Command](https://files.readme.io/3b3858f-IMG_1834.JPG "3b3858f-IMG_1834.JPG")

![Screenshot of the Slack Console for Interactivity and Shortcuts](https://files.readme.io/4664042-Screen_Shot_2020-04-30_at_11.27.35.png "Screen Shot 2020-04-30 at 11.27.35.png")

## Using Akeyless OTP by way of Slack

Type `/akeyless` in Slack and select the **OTP** option:

![Screenshot of the Slack Console when Previewing a Slash Command](https://files.readme.io/e318cfb-image.png)

Type in the content of the message you'd like to send for example:

`/akeyless Secret Management Reimangined`

Once sending the message, click `Yes` to share the secret **OTP** in the Slack channel, A URL will be shared with the recipient.

Clicking on the **OTP** URL will allow the view of the secret only for a one-time.

![Illustration for: Once sending the message, click Yes to share the secret OTP in the Slack channel, A URL will be shared with the recipient. Clicking on the OTP URL will allow the view…](https://files.readme.io/2e597b7-image.png)
