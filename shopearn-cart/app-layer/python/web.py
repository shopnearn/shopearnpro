from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.logging import correlation_paths

API_GATEWAY_REST = correlation_paths.API_GATEWAY_REST


class AppHttpResolver(APIGatewayHttpResolver):
    pass
