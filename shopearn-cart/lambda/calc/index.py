from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.parser import parse
from aws_lambda_powertools.utilities.parser.envelopes import ApiGatewayV2Envelope
from pydantic import ValidationError

import model

import ddb
import log
import ulid
import web

http = web.ApiHttpResolver()
metrics = log.AppMetrics()
tracer = log.AppTracer(service="calc")
logger = log.AppLogger(service="calc", logger_formatter=log.LambdaLogFormatter(), datefmt="%Y%m%dT%H%M%S.%f")


@http.get("/calc/view",
          summary="Get all items from DynamoDB",
          description="Get all items from DynamoDB")
@tracer.capture_method(capture_response=True)
def view():
    response = ddb.market.scan()
    items = response['Items']
    while 'LastEvaluatedKey' in response:
        response = ddb.market.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])
    logger.info("successful read")
    metrics.add_metric(name="view_metric", unit=MetricUnit.Count, value=1)
    # metrics.add_metadata(key="uid", value=f"{uid}")
    return items


@http.get("/calc/compute",
          summary="Calculate bonus",
          description="Calculate bonus for a transaction")
def calc():
    pass


@http.put("/calc/product",
          summary="Save product to DynamoDB",
          description="Save product to DynamoDB")
def save_product():
    pid = str(ulid.ULID())
    try:
        product: model.Product = parse(http.current_event.raw_event, model=model.Product, envelope=ApiGatewayV2Envelope)
        product.id = pid
        logger.info(f"Saving product: {product}")
    except ValidationError as e:
        logger.error(f"Validation error: {e}")


@http.get("/calc/product/<pid>",
          summary="Get product by id",
          description="Get product by id from DynamoDB")
def get_product(pid: str):
    try:
        logger.info(f"Get product: {pid}")
    except ValidationError as e:
        logger.error(f"Validation error: {e}")


@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
@logger.inject_lambda_context(correlation_id_path=web.API_GATEWAY_REST, log_event=logger.log_level in ["info", "debug"])
def handler(event, context):
    return http.resolve(event, context)
