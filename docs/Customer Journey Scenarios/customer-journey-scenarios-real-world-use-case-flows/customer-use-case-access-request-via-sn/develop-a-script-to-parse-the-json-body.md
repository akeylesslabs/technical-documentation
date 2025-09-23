---
title: Develop a Script to Parse the JSON Body
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
The provided script is designed to be used in a ServiceNow instance, specifically for handling incoming HTTP requests to a Scripted REST API. It parses a JSON payload from the request, creates a new record in a specified table with data extracted from the JSON, and responds appropriately based on the success or failure of these operations. Below is a detailed explanation of how this script works:

# Understanding the Script Flow

**Receive and Parse JSON Payload**

- The script starts by accessing the incoming HTTP request's body through request.body.dataString. This contains the raw JSON payload sent to the endpoint.
- It attempts to parse this JSON string into a JavaScript object using JSON.parse(requestBody). If parsing fails (e.g., due to malformed JSON), it catches the error and responds with a 400 status code (Bad Request) and an error message indicating the JSON is invalid.

**Initialize a New Record**

- It then initializes a new record in the u_akeyless_event_reciver table using GlideRecord, a ServiceNow API for database operations. This table name is specified in the script and should exist in your ServiceNow instance. If it doesn’t, you need to create it or use an existing table name.

**Set Record Fields from JSON Data**

- The script sets various fields of the new record (u_access_id, u_event_id, etc.) with values extracted from the parsed JSON data. It's important that these field names match the column names in your u_akeyless_event_reciver table.
- For fields that are expected to store complex data types like arrays or objects (u_capabilities), the script converts them into JSON strings using JSON.stringify() before storing. This is because relational database fields typically store text or numbers and cannot directly store complex types.

**Insert the Record and Respond**

- After setting all the necessary fields, the script attempts to insert the new record into the database with record.insert().
- If the insertion is successful, it retrieves the new record's Sys ID (newRecordSysId), responds with a 201 status code (Created), and includes the Sys ID in the response body.
- If the insertion fails, perhaps due to missing mandatory fields or other database constraints, it responds with a 500 status code (Internal Server Error) and an appropriate error message.

**Key Points to Note**

- Table and Field Names: Ensure that the table u_akeyless_event_reciver and the field names like u_access_id, u_event_id, etc., exist in your ServiceNow instance. If they don't, you'll need to create them according to your data model.
- Error Handling: The script includes basic error handling for JSON parsing and database insertion. It responds with HTTP status codes and messages that help the caller understand what went wrong.
- Data Conversion: Complex data types are converted to JSON strings to be stored in text fields. Ensure that your application logic accounts for this when reading these fields.

**Script Example **

```Text JavaScript
(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
    // Parse the incoming JSON payload from the request body
    var requestBody = request.body.dataString;
    var jsonData;
    try {
        jsonData = JSON.parse(requestBody);
    } catch (e) {
        // Handle parsing error
        response.setStatus(400);
        response.setBody({error: 'Bad request', message: 'Invalid JSON format'});
        return;
    }

    // Initialize a new record in the specified table
    var record = new GlideRecord('u_akeyless_event_reciver'); // Ensure table name is correct

    // Manually set record fields based on the jsonData
    record.initialize();
    record.setValue('u_access_id', jsonData.access_id);
    record.setValue('u_event_id', jsonData.event_id.toString()); // Assuming this is a string field
    record.setValue('u_rule_type', jsonData.rule_type);
    record.setValue('u_secret', jsonData.secret);
    record.setValue('u_secret_type', jsonData.secret_type);
    record.setValue('u_comment', jsonData.comment);
    // For array or object fields, you might need to store them as JSON strings
    record.setValue('u_capabilities', JSON.stringify(jsonData.capabilities));
    //record.setValue('u_client_sub_claims', JSON.stringify(jsonData.client_sub_claims));
    //record.setValue('u_ttl_in_min', jsonData.ttl_in_min.toString()); // Assuming this is a string field
	record.setValue('u_json_event_with_access_request', requestBody);

    // Insert the new record into the database
    var newRecordSysId = record.insert();
    
    if (newRecordSysId) {
        // Respond with success
        response.setStatus(201); // Created
        response.setBody({result: 'success', sys_id: newRecordSysId});
    } else {
        // Handle insertion failure (e.g., due to mandatory fields missing)
        response.setStatus(500); // Internal Server Error
        response.setBody({error: 'Server error', message: 'Failed to insert the record'});
    }
})(request, response);

```