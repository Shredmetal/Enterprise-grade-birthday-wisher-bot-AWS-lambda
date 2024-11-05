import os
import unittest
from unittest.mock import patch
from moto import mock_aws

from src.birthday_wisher.lambda_handler import lambda_handler


class TestLambdaHandler(unittest.TestCase):

    def setUp(self):
        # Set up environment variables for testing
        os.environ['BUCKET_NAME'] = 'test-bucket'
        os.environ['FILE_KEY'] = 'test-birthdays.csv'

        self.test_birthday_data = {
            "name": "Test Person",
            "email": "test@example.com",
            "sarcastic": True,
            "day": "01",
            "month": "01"
        }

    def tearDown(self):
        # Clean up environment variables
        os.environ.pop('BUCKET_NAME', None)
        os.environ.pop('FILE_KEY', None)

    @mock_aws
    @patch('src.birthday_wisher.helpers.get_birthdays.BirthdayChecker.get_todays_birthdays')
    @patch('src.birthday_wisher.helpers.openai_handler.OpenAIHandler.get_openai_message')
    @patch('src.birthday_wisher.helpers.email_handler.EmailHandler.send_birthday_emails')
    def test_successful_birthday_processing(self, mock_email, mock_openai, mock_birthdays):
        # Configure mocks
        mock_birthdays.return_value = [self.test_birthday_data]
        mock_openai.return_value = "Test birthday message"
        mock_email.return_value = True

        # Call lambda handler
        response = lambda_handler({}, None)

        # Verify response
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Processed 1 birthdays: 1 successful', response['body']['summary'])

        # Verify mock calls
        mock_birthdays.assert_called_once_with(
            os.environ['BUCKET_NAME'],
            os.environ['FILE_KEY']
        )
        mock_openai.assert_called_once_with(self.test_birthday_data)
        mock_email.assert_called_once()

    @mock_aws
    @patch('src.birthday_wisher.helpers.get_birthdays.BirthdayChecker.get_todays_birthdays')
    def test_no_birthdays(self, mock_birthdays):
        # Configure mock to return empty list
        mock_birthdays.return_value = []

        # Call lambda handler
        response = lambda_handler({}, None)

        # Verify response
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], 'No birthdays today')

    @mock_aws
    @patch('src.birthday_wisher.helpers.get_birthdays.BirthdayChecker.get_todays_birthdays')
    @patch('src.birthday_wisher.helpers.openai_handler.OpenAIHandler.get_openai_message')
    @patch('src.birthday_wisher.helpers.email_handler.EmailHandler.send_birthday_emails')
    def test_failed_email_sending(self, mock_email, mock_openai, mock_birthdays):
        # Configure mocks
        mock_birthdays.return_value = [self.test_birthday_data]
        mock_openai.return_value = "Test birthday message"
        mock_email.return_value = False

        # Call lambda handler
        response = lambda_handler({}, None)

        # Verify response
        self.assertEqual(response['statusCode'], 207)  # Partial success
        self.assertIn('Processed 1 birthdays: 0 successful', response['body']['summary'])

    @mock_aws
    @patch('src.birthday_wisher.helpers.get_birthdays.BirthdayChecker.get_todays_birthdays')
    def test_birthday_checker_exception(self, mock_birthdays):
        # Configure mock to raise exception
        mock_birthdays.side_effect = Exception("Test error")

        # Call lambda handler
        response = lambda_handler({}, None)

        # Verify response
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Critical error in lambda function', response['body'])

    @mock_aws
    @patch('src.birthday_wisher.helpers.get_birthdays.BirthdayChecker.get_todays_birthdays')
    @patch('src.birthday_wisher.helpers.openai_handler.OpenAIHandler.get_openai_message')
    @patch('src.birthday_wisher.helpers.email_handler.EmailHandler.send_birthday_emails')
    def test_multiple_birthdays_mixed_success(self, mock_email, mock_openai, mock_birthdays):
        # Create multiple test birthday entries
        test_birthdays = [
            self.test_birthday_data,
            {**self.test_birthday_data, "name": "Test Person 2", "email": "test2@example.com"}
        ]

        # Configure mocks
        mock_birthdays.return_value = test_birthdays
        mock_openai.return_value = "Test birthday message"
        mock_email.side_effect = [True, False]  # First succeeds, second fails

        # Call lambda handler
        response = lambda_handler({}, None)

        # Verify response
        self.assertEqual(response['statusCode'], 207)
        self.assertIn('Processed 2 birthdays: 1 successful', response['body']['summary'])
        self.assertEqual(len(response['body']['details']), 2)

    def test_missing_environment_variables(self):
        # Remove environment variables
        os.environ.pop('BUCKET_NAME', None)
        os.environ.pop('FILE_KEY', None)

        # Call lambda handler
        response = lambda_handler({}, None)

        # Verify response indicates error
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Critical error in lambda function', response['body'])
