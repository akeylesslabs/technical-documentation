---
title: Usage Reports
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---

Akeyless Usage Reports help administrators monitor secrets, keys, and password manager activity across their organization.

### CLI

```shell
akeyless get-analytics-data --json | jq '.usage_reports.sm.ai_clients'
```
