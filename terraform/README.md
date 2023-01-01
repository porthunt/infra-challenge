# Infrastructure

Terraform Cloud API-driven workflow is being used for the lock/state management.

## Main Resources

### Lambdas

#### populate
Function used to populate the DynamoDB database with some random transaction data.

#### transaction
Function used to retrieve all transactions or an specific transaction (if the id is provided).

#### add transaction
Function used to add new transactions to the table.

### DynamoDB
DynamoDB table that stores all the transaction information.

### API Gateway

Creates a REST API based on `api/openapi.json`. There are three endpoints:

* `/populate`: Which executes the provided function. Maps to `populate` lambda function.
* `/transactions`: Which executes the `transactions` lambda function to retrieve all the transactions.
* `/transactions/<id>`: Which executes the `transactions lambda function to retrieve an specific transaction.

### SQS
Two queues are created. The queue is used to add new transactions to the table, therefore there is a source event for the `add transaction` function.

The other queue is a dead letter queue. This queue is used to host transactions that failed to be inserted (check `api/` for more information).

### S3
An S3 bucket to host the lambda functions code.

### System Manager
A parameter stored on Parameter Store, hosting the API key used by the Serverless Framework API (see `api/` for more information).

## Variables
* `username`: A prefix for multiple resources (e.g. `porthunt`).
* `api_key`: A random string that will be used as the api key for the API.

## Improvements
* Better separation between the application resources from the infrastructure resources, i.e. first the infrastructure resources like S3 must be created, and then the application resources (lambdas, API Gateway). Currently we must run them at the same time, which will generate a new lambda function everytime an `apply` is ran.