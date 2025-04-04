import json

def handler(event, context):

    body = {
        "message": "Howdy Your function executed successfully!",
    }


    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
