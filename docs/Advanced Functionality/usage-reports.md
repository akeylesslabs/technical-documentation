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

Retrieve analytics and usage data:

```shell
akeyless get-analytics-data
```

Sample output:

```json
{
  "usage_reports": {
    "sm": {
      "total_clients": 17,
      "ai_clients": 4
    }
  }
}
```
