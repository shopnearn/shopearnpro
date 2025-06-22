import json

import boto3
from botocore.exceptions import ClientError


def handler(event, context):
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Market_dev')

    try:
        # Get URL parameters from the event
        if 'queryStringParameters' not in event or not event['queryStringParameters']:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'No query parameters provided'
                })
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

        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'Data successfully written to DynamoDB',
                'item': item
            })
        }

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']

        if error_code == 'ResourceNotFoundException':
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': 'Table not found'
                })
            }
        elif error_code in ['AccessDeniedException', 'UnauthorizedException']:
            return {
                'statusCode': 403,
                'body': json.dumps({
                    'error': 'Access denied to DynamoDB table'
                })
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': error_message
                })
            }
