import json
import boto3
from ulid import ULID

def handler(event, context):
    v = boto3.__version__

    id = str(ULID())
    body = {
        "message": "Go Serverless v4.0! Your function executed successfully! Boto3 version: " + v + "; requestId=" + id,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

if __name__ == '__main__':
    print(handler(None, None))
