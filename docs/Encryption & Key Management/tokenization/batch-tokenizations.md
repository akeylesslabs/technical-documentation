---
title: Batch Tokenizations
excerpt: Tokenization Service Enhancement
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
The tokenization service is being enhanced to support batch processing for large datasets, significantly improving its efficiency, especially for handling high volumes of data. This documentation outlines the objectives, background, enhancements, expected outcomes, and additional features being introduced, including the caching mechanism and API support for batch operations.

The primary goal is to enhance the existing tokenization service by integrating a sophisticated batch processing system. This will include the introduction of a new "bulk" flag within the tokenize function, allowing users to transmit entire datasets for encryption in one go. The focus is on improving efficiency, reducing latency, and optimizing resource usage, especially for scenarios involving large datasets.

### Enhancements to the Tokenize Function

**Bulk Input Capability**

- Modification: The existing tokenize function will be updated to accept an array of data entries (or a similar bulk format) instead of processing single data entries individually.
- Format: Data will be in a batch format such as

```shell JSON
{
  "token": "your_token",
  "batch-data": "[{\"item_id\": 758, \"data\": \"4818199332\", \"tweak\": \"YXNkZmdobg==\"}, {\"item_id\": 758, \"data\": \"901347774\", \"tweak\": \"YXNkZmdobg==\"}]"
}
```

### Caching for Tokenization

A caching mechanism is being implemented to further improve the performance of the tokenization service, especially for handling the expected 1.5+ trillion operations per month.

**Key Points**

- Purpose: The cache is intended to handle frequently accessed tokens, reducing the need for repeated processing and further optimizing resource usage.
- API Support: A single API call will be introduced for `tokenize-batch` and `detokenize-batch`. This will streamline batch operations, excluding normal `tokenize/detokenize` operations from caching.
- Key Support: The tokenizer can support both classic and Distributed Fragments Cryptography™ (DFC) keys.