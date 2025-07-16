import json

import boto3
from aws_lambda_powertools import Logger, Metrics, Tracer

import ulid
from cart import (
    get_cart_id,
    get_headers
)

logger, tracer, metrics = Logger(), Tracer(), Metrics()

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Market_dev")


# product_service_url = os.environ["PRODUCT_SERVICE_URL"]

def handler(event, context):
    v = boto3.__version__
    try:
        print(event)
        payload = json.loads(event["body"])
    except KeyError:
        return {
            "statusCode": 400,
            "headers": get_headers("00000000-0000-0000-0000-000000000000"),
            "body": json.dumps({"message": "No Request payload"}),
        }
    product_id = payload.get("id",0)
    quantity = payload.get("quantity", 1)
    cart_id, _ = get_cart_id(event["headers"])

    body = {
        "message": "Go Serverless v4.0! Your function executed successfully! Boto3 version: " + v + "; id=" + str(
            ulid.ULID())
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
