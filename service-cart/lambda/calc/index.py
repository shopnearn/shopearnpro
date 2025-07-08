import json

from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import Response, content_types

import ddb
import log
import ulid
import web

log = log.AppLogger(service="calc", logger_formatter=log.LambdaLogFormatter(), datefmt="%Y%m%dT%H%M%S.%f")
http = web.ApiHttpResolver()
tracer = Tracer()


@http.get("/view",
          summary="Get all items from DynamoDB",
          description="Get all items from DynamoDB")
def view():
    try:
        response = ddb.market.scan()
        items = response['Items']
        while 'LastEvaluatedKey' in response:
            response = ddb.market.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])
        log.append_keys(app_key="my_value")
        print(log.structure_logs)
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
        ddb.market.put_item(Item=item)
        log.info("successful write")
        return web.success('Data successfully written to DynamoDB', item)
    except Exception as e:
        return web.fail(e)


@http.get("/calc")
def calc(event, trace):
    pass


@http.not_found()
@tracer.capture_method(capture_response=False)
def http_not_found() -> Response:
    log.debug("Route not found", route=http.current_event.path)
    return Response(status_code=404, content_type=content_types.TEXT_PLAIN, body="Not found")


@log.inject_lambda_context(correlation_id_path=web.API_GATEWAY_REST, log_event=log.log_level in ["info", "debug"])
def handler(event, context):
    return http.resolve(event, context)
