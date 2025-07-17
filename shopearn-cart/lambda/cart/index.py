import os

import log
import web
from cart import get_cart_id

app = web.AppHttpResolver()
metrics = log.AppMetrics()
tracer = log.AppTracer(service="cart")
logger = log.AppLogger(service="cart", logger_formatter=log.LambdaLogFormatter(), datefmt="%Y%m%dT%H%M%S.%f")

@app.get("/cart/view",
          summary="Get all items from cart",
          description="Get all items from cart")
@tracer.capture_method(capture_response=True)
def list_cart():
    # ddb.market.put_item(Item=payload)
    print("USERPOOL_ID: " + os.getenv("USERPOOL_ID"))
    cart_id, generated = get_cart_id(app.current_event.get("headers"))
    return f"cartId: {cart_id} generated: {generated}"

@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
@logger.inject_lambda_context(correlation_id_path=web.API_GATEWAY_REST, log_event=logger.log_level in ["info", "debug"])
def handler(event, context):
    return app.resolve(event, context)
