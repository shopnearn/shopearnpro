import json
import boto3
import numpy

def handler(event, context):

    print(numpy.max([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
    v = boto3.__version__

    body = {
        "message": "Go Serverless v4.0! Your function executed successfully! Boto3 version: " + v,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
