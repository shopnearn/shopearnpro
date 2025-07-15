import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ["MARKET_TABLE"]
table = dynamodb.Table(table_name)


def handler(event, context):
    with open('dbinit.json', 'r') as file:
        items = json.load(file)
    with table.batch_writer(overwrite_by_pkeys=['pk', 'sk']) as batch:
        for item in items:
            batch.put_item(Item=item)
    return {"dbinit": f"{table_name} table loaded {len(items)} items."}
