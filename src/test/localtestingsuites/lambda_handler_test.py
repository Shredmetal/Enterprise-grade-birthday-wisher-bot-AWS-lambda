import os
import unittest
from unittest.mock import patch, MagicMock
from moto import mock_aws

from src.birthday_wisher.constants.constants import BirthdayWishesConstants
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
    @patch('src.birthday_wisher.helpers.email_handler.EmailHandler.send_birthday_emails')
    @patch('src.birthday_wisher.helpers.llm_api_factory.LLMAPIFactory.get_handler')  # Changed this line
    @patch('src.birthday_wisher.helpers.get_birthdays.BirthdayChecker.get_todays_birthdays')
    def test_successful_birthday_processing(self, mock_birthdays, mock_llm_factory, mock_email):
        # Configure mocks
        mock_birthdays.return_value = [self.test_birthday_data]

        # Mock the LLM provider
        mock_llm_provider = MagicMock()
        mock_llm_provider.get_birthday_message.return_value = "Test birthday message"
        mock_llm_factory.return_value = mock_llm_provider

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
        mock_llm_factory.assert_called_once_with(BirthdayWishesConstants.LLM_PROVIDER_SELECTION)
        mock_llm_provider.get_birthday_message.assert_called_once_with(self.test_birthday_data)
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
    @patch('src.birthday_wisher.helpers.email_handler.EmailHandler.send_birthday_emails')
    @patch('src.birthday_wisher.helpers.llm_api_factory.LLMAPIFactory.get_handler')
    @patch('src.birthday_wisher.helpers.get_birthdays.BirthdayChecker.get_todays_birthdays')
    def test_failed_email_sending(self, mock_birthdays, mock_llm_factory, mock_email):
        # Configure mocks
        mock_birthdays.return_value = [self.test_birthday_data]

        # Mock the LLM provider
        mock_llm_provider = MagicMock()
        mock_llm_provider.get_birthday_message.return_value = "Test birthday message"
        mock_llm_factory.return_value = mock_llm_provider

        mock_email.return_value = False

        # Call lambda handler
        response = lambda_handler({}, None)

        # Verify response
        self.assertEqual(response['statusCode'], 207)  # Partial success
        self.assertIn('Processed 1 birthdays: 0 successful', response['body']['summary'])

        # Verify mock calls
        mock_birthdays.assert_called_once()
        mock_llm_provider.get_birthday_message.assert_called_once()
        mock_email.assert_called_once()

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
    @patch('src.birthday_wisher.helpers.email_handler.EmailHandler.send_birthday_emails')
    @patch('src.birthday_wisher.helpers.llm_api_factory.LLMAPIFactory.get_handler')
    @patch('src.birthday_wisher.helpers.get_birthdays.BirthdayChecker.get_todays_birthdays')
    def test_multiple_birthdays_mixed_success(self, mock_birthdays, mock_llm_factory, mock_email):
        # Create multiple test birthday entries
        test_birthdays = [
            self.test_birthday_data,
            {**self.test_birthday_data, "name": "Test Person 2", "email": "test2@example.com"}
        ]

        # Configure mocks
        mock_birthdays.return_value = test_birthdays

        # Mock the LLM provider
        mock_llm_provider = MagicMock()
        mock_llm_provider.get_birthday_message.return_value = "Test birthday message"
        mock_llm_factory.return_value = mock_llm_provider

        mock_email.side_effect = [True, False]  # First succeeds, second fails

        # Call lambda handler
        response = lambda_handler({}, None)

        # Verify response
        self.assertEqual(response['statusCode'], 207)
        self.assertIn('Processed 2 birthdays: 1 successful', response['body']['summary'])
        self.assertEqual(len(response['body']['details']), 2)

        # Verify mock calls
        mock_birthdays.assert_called_once()
        self.assertEqual(mock_llm_provider.get_birthday_message.call_count, 2)
        self.assertEqual(mock_email.call_count, 2)

    def test_missing_environment_variables(self):
        # Remove environment variables
        os.environ.pop('BUCKET_NAME', None)
        os.environ.pop('FILE_KEY', None)

        # Call lambda handler
        response = lambda_handler({}, None)

        # Verify response indicates error
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Critical error in lambda function', response['body'])
