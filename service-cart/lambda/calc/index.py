import json

from aws_lambda_powertools import Tracer, Metrics
from aws_lambda_powertools.event_handler import Response, content_types
from aws_lambda_powertools.metrics import MetricUnit

from aws_lambda_powertools.utilities.parser import parse

import model

import ddb
import log
import ulid
import web

log = log.AppLogger(service="calc", logger_formatter=log.LambdaLogFormatter(), datefmt="%Y%m%dT%H%M%S.%f")
http = web.ApiHttpResolver()
tracer = Tracer(service="calc")
metrics = Metrics()


@http.get("/calc/view",
          summary="Get all items from DynamoDB",
          description="Get all items from DynamoDB")
@tracer.capture_method(capture_response=True)
def view():
    uid = str(ulid.ULID())
    response = ddb.market.scan()
    items = response['Items']
    while 'LastEvaluatedKey' in response:
        response = ddb.market.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])
    log.info("successful read")
    metrics.add_metric(name="view_metric", unit=MetricUnit.Count, value=1)
    # metrics.add_metadata(key="uid", value=f"{uid}")
    return items


@http.get("/calc/compute")
def calc(event, trace):
    pass


@http.not_found()
def http_not_found() -> Response:
    log.debug("Route not found", route=http.current_event.path)
    return Response(status_code=404, content_type=content_types.TEXT_PLAIN, body="Not found")


@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
@log.inject_lambda_context(correlation_id_path=web.API_GATEWAY_REST, log_event=log.log_level in ["info", "debug"])
def handler(event, context):
    return http.resolve(event, context)
