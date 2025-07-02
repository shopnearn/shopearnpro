import boto3
import json
import ulid
import web
import log

log = log.AppLogger(service="CALC")
api = web.ApiHttpResolver()
ddb = boto3.resource('dynamodb')
table = ddb.Table('Market_dev')


@api.get("/view")
@api.post("/view")
def view():
    try:
        response = table.scan()
        items = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])
        log.info("successful read")
        return web.success(str(ulid.ULID()), json.dumps(items))
    except Exception as e:
        return web.fail(e)


@api.get("/write")
def write():
    event = api.current_event
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
        log.info("successful write")
        return web.success('Data successfully written to DynamoDB', item)
    except Exception as e:
        return web.fail(e)


@api.get("/calc")
def calc(event, trace):
    pass


@log.inject_lambda_context(correlation_id_path=web.API_GATEWAY_REST, log_event=True, clear_state=True)
def handler(event, context):
    return api.resolve(event, context)
