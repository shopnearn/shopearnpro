import json
import db
import log
import ulid
import web

log = log.AppLogger(service="calc")
http = web.HttpApiResolver()

@http.get("/view")
@http.post("/view")
def view():
    try:
        response = db.market.scan()
        items = response['Items']
        while 'LastEvaluatedKey' in response:
            response = db.market.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])
        log.info("successful read")
        return web.success(str(ulid.ULID()), json.dumps(items))
    except Exception as e:
        return web.fail(e)


@http.get("/write")
def write():
    event = http.current_event
    try:
        if 'queryStringParameters' not in event or not event['queryStringParameters']:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'No query parameters provided'
                }
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
        db.market.put_item(Item=item)
        log.info("successful write")
        return web.success('Data successfully written to DynamoDB', item)
    except Exception as e:
        return web.fail(e)


@http.get("/calc")
def calc(event, trace):
    pass


@log.inject_lambda_context(correlation_id_path=web.API_GATEWAY_REST, log_event=True)
def handler(event, context):
    return http.resolve(event, context)
