import json
import boto3
from botocore.exceptions import ClientError
import ulid

def handler(event, context):
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Market_dev')  # Using the table name from your serverless.yml

    try:
        # Attempt to scan the table
        response = table.scan()
        items = response['Items']

        # Handle pagination if there are more items
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])

        # Return successful response with items
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(items) + "; ulid=" + str(ulid.ULID())
        }

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']

        if error_code == 'ResourceNotFoundException':
            # Scenario 4: Table not found
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': 'Table not found'
                })
            }
        elif error_code in ['AccessDeniedException', 'UnauthorizedException']:
            # Scenario 3: Lambda doesn't have permissions
            return {
                'statusCode': 403,
                'body': json.dumps({
                    'error': 'Access denied to DynamoDB table'
                })
            }
        else:
            # Handle other errors
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': error_message
                })
            }
