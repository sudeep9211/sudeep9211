import os
import json
import unittest
from unittest.mock import patch, MagicMock
from function.quote_lambda import fetch_random_quote, lambda_handler

class TestLambdaFunctions(unittest.TestCase):

    @patch('function.quote_lambda.urllib.request.urlopen')
    @patch('function.quote_lambda.os.getenv')
    def test_fetch_random_quote(self, mock_getenv, mock_urlopen):
        # Mock the environment variable
        mock_getenv.return_value = "http://mockapi.com/quote"
        
        # Mock the API response
        mock_urlopen.return_value.__enter__.return_value.read.return_value = json.dumps([
            {"q": "Life is what happens when you're busy making other plans.", "a": "John Lennon"}
        ]).encode('utf-8')

        # Call the function
        result = fetch_random_quote()
        
        # Assert the expected output
        self.assertEqual(result, '"Life is what happens when you\'re busy making other plans." - John Lennon')

    @patch('function.quote_lambda.boto3.client')
    @patch('function.quote_lambda.fetch_random_quote')
    @patch('function.quote_lambda.os.getenv')
    def test_lambda_handler(self, mock_getenv, mock_fetch_random_quote, mock_boto_client):
        # Mock the environment variable
        mock_getenv.return_value = "arn:aws:sns:us-east-1:123456789012:MyTopic"
        
        # Mock the fetch_random_quote function
        mock_fetch_random_quote.return_value = '"Life is what happens when you\'re busy making other plans." - John Lennon'
        
        # Mock the SNS client
        mock_sns_client = MagicMock()
        mock_boto_client.return_value = mock_sns_client
        
        # Call the lambda_handler function
        event = {}
        context = {}
        response = lambda_handler(event, context)
        
        # Assert the expected response
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], 'Quote sent to SNS')
        mock_sns_client.publish.assert_called_once()

if __name__ == '__main__':
    unittest.main()
