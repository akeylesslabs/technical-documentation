---
title: Security Health
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
## Overview

The Security Health Dashboard provides users with an overview of the strength and security of their stored passwords, offering real-time insights, improvement suggestions, and critical metrics that help maintain strong password hygiene. This document outlines the layout, functionality, scoring metrics, and API integrations to ensure a comprehensive understanding of the security health features.

![](https://files.readme.io/c51dd3e02752d51b5d79e21377a2cc21270b2bb98962f694dacc5674b4347a87-Screenshot_2024-09-21_at_7.32.19.png)

<br />

<br />

## Dashboard Layout

1. **Upper Section: Gauges**  
   This section contains visual gauges that display the overall health of passwords:

- Security Score Gauge: Represents an overall security score for all stored passwords. This score is a composite of various factors such as length, complexity, and rotation policy. The gauge's colors range from red (low score) to green (high score).
- Weak Passwords Gauge: Displays the number of weak passwords as a fraction of the total passwords. Weak passwords are identified based on their lack of complexity and length.
- Breached Passwords Gauge: Shows the number of passwords that have been compromised in known breaches. This gauge helps users identify vulnerable passwords that should be updated or replaced immediately.

2. **Lower Section: Password List**  
   Below the gauges is a detailed table listing all passwords, providing users with key information and actionable suggestions:

- Password Location: The service or app where the password is used.
- Name of the Password: The name or identifier for the password.
- Score: A graphical representation of the password's strength (e.g., weak, medium, strong).
- Suggestion: Provides recommendations for improving password strength.
- Last Updated: The date when the password was last changed.

<br />

## Enhanced Filtering Options

Users can apply filters to view specific types of passwords:

- Filter by Weak Passwords: Filters the list to show only weak passwords.
- Filter by Breached Passwords: Filters the list to show passwords that have appeared in known breaches.
- Filter by Update Required Passwords: Filters passwords that need to be updated based on their age or vulnerability.

<br />

## Toggle for Password Score Feature

A toggle button has been added to allow users to enable or disable the password score feature in their account settings:

- **Toggle Button:** Located under "Password Management," the button controls whether the password score is displayed.
- **Default Setting:** The feature is disabled by default.  
  Functionality: When enabled, password scores are calculated and displayed; when disabled, scores are hidden.

<br />

## Compromised Password Check

As part of our Password Manager’s Security Health evaluation, we incorporate checks against external databases of known compromised credentials. Specifically, we leverage the “Have I Been Pwned” (HIBP) database, which aggregates publicly disclosed password breaches.

This integration allows us to:

- Verify password exposure: Determine whether a given password has appeared in any known data breach, including those circulating on the dark web.
- Measure reuse risk: Identify how many times the same password has been exposed across different breaches, highlighting patterns of weak or reused credentials.
- Enhance scoring accuracy: Incorporate the exposure and reuse metrics into the overall Password Manager Security Health score, providing a more accurate and risk-aware assessment of each user’s password hygiene.