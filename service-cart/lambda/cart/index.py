import json
import boto3
import logging
import os
import db
import ulid

def handler(event, context):
    v = boto3.__version__

    db.db_write(None, None)

    body = {
        "message": "Go Serverless v4.0! Your function executed successfully! Boto3 version: " + v + "; id=" + str(ulid.ULID())
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


if __name__ == '__main__':
    print(handler(None, None))
