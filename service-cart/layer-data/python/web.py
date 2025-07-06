import json
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver

API_GATEWAY_REST = correlation_paths.API_GATEWAY_REST

class HttpApiResolver(APIGatewayHttpResolver):
    pass

def init_request(event, context):
    path = event['requestContext']['http']['path']
    method = event['requestContext']['http']['method']
    trace = f"[{context.function_name}][{event['routeKey']}]"
    return method, path, trace


def not_found(event, trace):
    print(f"NOT_FOUND{trace}")
    return {
        'statusCode': 404,
        'body': {'error': f"Route not found: {event['routeKey']}"}
    }


def success(msg, data=None, trace=None):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': msg,
            'item': data
        })
    }


def fail(e):
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
