import unittest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
import json
import index

class TestDynamoDBLambda(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.context = {}
        self.event = {}

    @patch('boto3.resource')
    def test_successful_scan_with_items(self, mock_boto3_resource):
        """Test Scenario 1: Successful read of records"""
        # Mock DynamoDB response
        mock_table = MagicMock()
        mock_table.scan.return_value = {
            'Items': [
                {'id': {'S': '1'}, 'name': {'S': 'item1'}},
                {'id': {'S': '2'}, 'name': {'S': 'item2'}}
            ]
        }
        
        mock_dynamodb = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_boto3_resource.return_value = mock_dynamodb

        # Execute the Lambda function
        response = index.handler(self.event, self.context)

        # Verify the response
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertIn('items', body)
        self.assertEqual(len(body['items']), 2)

    @patch('boto3.resource')
    def test_empty_table(self, mock_boto3_resource):
        """Test Scenario 2: Empty table"""
        # Mock empty DynamoDB response
        mock_table = MagicMock()
        mock_table.scan.return_value = {'Items': []}
        
        mock_dynamodb = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_boto3_resource.return_value = mock_dynamodb

        # Execute the Lambda function
        response = index.handler(self.event, self.context)

        # Verify the response
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertIn('items', body)
        self.assertEqual(len(body['items']), 0)

    @patch('boto3.resource')
    def test_unauthorized_access(self, mock_boto3_resource):
        """Test Scenario 3: Lambda doesn't have permissions"""
        # Mock DynamoDB unauthorized error
        mock_table = MagicMock()
        error_response = {
            'Error': {
                'Code': 'AccessDeniedException',
                'Message': 'Access denied'
            }
        }
        mock_table.scan.side_effect = ClientError(error_response, 'Scan')
        
        mock_dynamodb = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_boto3_resource.return_value = mock_dynamodb

        # Execute the Lambda function
        response = index.handler(self.event, self.context)

        # Verify the response
        self.assertEqual(response['statusCode'], 403)
        body = json.loads(response['body'])
        self.assertIn('error', body)
        self.assertIn('denied', body['error'].lower())

    @patch('boto3.resource')
    def test_table_not_found(self, mock_boto3_resource):
        """Test Scenario 4: Table doesn't exist"""
        # Mock DynamoDB table not found error
        mock_table = MagicMock()
        error_response = {
            'Error': {
                'Code': 'ResourceNotFoundException',
                'Message': 'Table not found'
            }
        }
        mock_table.scan.side_effect = ClientError(error_response, 'Scan')
        
        mock_dynamodb = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_boto3_resource.return_value = mock_dynamodb

        # Execute the Lambda function
        response = index.handler(self.event, self.context)

        # Verify the response
        self.assertEqual(response['statusCode'], 500)
        body = json.loads(response['body'])
        self.assertIn('error', body)
        self.assertEqual(body['error'], 'Table not found')

    @patch('boto3.resource')
    def test_pagination(self, mock_boto3_resource):
        """Test pagination handling"""
        # Mock DynamoDB responses with pagination
        mock_table = MagicMock()
        mock_table.scan.side_effect = [
            {
                'Items': [{'id': {'S': '1'}, 'name': {'S': 'item1'}}],
                'LastEvaluatedKey': {'id': {'S': '1'}}
            },
            {
                'Items': [{'id': {'S': '2'}, 'name': {'S': 'item2'}}]
            }
        ]
        
        mock_dynamodb = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_boto3_resource.return_value = mock_dynamodb

        # Execute the Lambda function
        response = index.handler(self.event, self.context)

        # Verify the response
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertIn('items', body)
        self.assertEqual(len(body['items']), 2)
        # Verify that scan was called twice due to pagination
        self.assertEqual(mock_table.scan.call_count, 2)

if __name__ == '__main__':
    unittest.main()