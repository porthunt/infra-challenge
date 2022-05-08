# primer-api

## Configuring

### Prerequisites
* Python 3.8
* virtualenv (recommended)

Execute the following commands to configure the environment (Unix based):
```shell
$ cd primer-api/
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ make init
```

### Executing tests

To execute the unit tests, execute:

```shell
$ make unit
```

### Linting
To follow PEP8 coding stardards, it's possible to run flake8 and black. This is good to prevent multiple devs working on a project using different standards.

It's possible to verify linting using:
```shell
$ make lint
```

In case a local version of the API needs to be deployed, it's possible to use:
```shell
$ npm install
$ npx serverless deploy --stage dev
```

## Endpoints
More information can be seen on `openapi.json`, but here are the current endpoints:

### `/populate`
It reuses the code available on the challenge page. Nothing was changed here.

### `/transactions`
Retrieves transactions from the dynamoDB table. It uses pagination, since millions of items might be available. The default limit is 100, but this can be set on the query parameter.

Query parameters:
* `limit`: How many items should be retrieved. Default is 100. Must be a number between 1 and 1000. In case there are more transactions than the limit, a `cursor` attribute is returned with the last transaction id that was retrieved.
* `cursor`: In case this is set, the endpoint will start retrieving from that transaction id.
* `merchant`: Possible to filter transactions for a specific merchant.
* `currency`: Possible to filter transactions for a certain currency.
* `processor`: Possible to filter transactions for a specific processor.
* `amount`: Possible to retrieve transactions with a certain amount or gte/lte than the amount. The query parameter format can be `amount=400`, `amount=gte:400` or `amount=lte:400`.

### `/transactions/<id>`
Retrieves a specific transaction information in case it is available.

### Add transactions
This is **not** and endpoint. Transactions are added through an SQS queue. This is done to avoid multiple lambda functions being spawned for each transaction added. The queue can host multiple messages and a lambda function processes them at once.

The transaction might get discarded (i.e. sent to the DLQ) if:
* There is an issue with the body of the message;
* Invalid attributes (e.g. currency that is not defined, a date 2 years from now, etc);
* The `transaction_id` exists on the table already.

## Know Issues
* DynamoDB uses an unorthodox way of limiting/filtering. It first limits the items and then it applies the filter. Therefore if the query parameter is `limit=1&currency=USD`, unless the first item has `currency=USD`, the endpoint will return an empty list. There are ways to circuvent that, for example using local indexes on dynamoDB, but I didn't want to go deeper.
* Currently an API Key is needed to access `/transactions` and `/transactions/<id>`. There are two API keys set up, basically because there is one for the serverless framework API and another one for the API deployed using terraform.

## Improvements
* I wanted to implement integration with AWS Cognito for the authN/Z, but that would take much longer.
* Filter transactions by date.