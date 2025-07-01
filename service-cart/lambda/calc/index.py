import json
import boto3
import ulid
import web
from aws_lambda_powertools import Logger, Metrics, Tracer

tracer, logger, metrics = Tracer(), Logger(), Metrics(namespace="shopnearn")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Market_dev')


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
# @metrics.log_metrics(capture_cold_start_metric=True)
def handler(event, context):
    method, path, trace = web.init_request(event, context)
    logger.info("logging message")
    match (method, path):
        case ("GET", "/view"):
            return view(trace)
        case ("GET", "/write"):
            return write(event, trace)
        case ("GET", p) if p.startswith("/calc/"):
            # user_id = p.split("/")[-1]
            return web.success("calc called")
        case _:
            return web.not_found(event, trace)


def view(trace):
    try:
        # Attempt to scan the table
        response = table.scan()
        items = response['Items']
        # Handle pagination if there are more items
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])
        # Return successful response with items
        return web.success(str(ulid.ULID()), json.dumps(items), trace)
    except Exception as e:
        return web.fail(e)


def write(event, trace):
    try:
        if 'queryStringParameters' not in event or not event['queryStringParameters']:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'No query parameters provided'
                })
            }
        params = event['queryStringParameters']
        item = {
            'pk': params.get('pk', 'none'),
            'sk': params.get('sk', 'none'),
            'type': params.get('type', 'user'),
            'balance': params.get('balance', "0.0"),
            'refCode': params.get('refCode', "none"),
            'price': params.get('price', "none"),
            'name': params.get('name', "none"),
            'rewardRate': params.get('rewardRate', "0%"),
        }
        table.put_item(Item=item)
        return web.success('Data successfully written to DynamoDB', item, trace)
    except Exception as e:
        return web.fail(e)
