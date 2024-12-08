import os
import time
import unittest
from unittest.mock import patch, MagicMock
from moto import mock_aws
import boto3
from dotenv import load_dotenv

from src.birthday_wisher.constants.constants import YOUR_EMAIL
from src.birthday_wisher.helpers.email_handler import EmailHandler

class TestEmailHandler(unittest.TestCase):

    def setUp(self):
        load_dotenv()

        self.birthday_data = {
            "name": "John Doe",
            "email": YOUR_EMAIL,
            "sarcastic": "true"
        }

        self.test_message = "Test birthday message"

    @mock_aws
    def test_send_birthday_emails_mock(self):
        """Test email sending with mocked SMTP_SSL"""
        # Set up mock SSM
        ssm = boto3.client('ssm', region_name='ap-southeast-1')

        # Get email credentials from .env
        sender_email = os.getenv("SENDER_EMAIL")
        email_password = os.getenv("EMAIL_PASSWORD")

        if not sender_email or not email_password:
            raise ValueError("Email credentials not found in .env file")

        # Create mock parameters in SSM
        ssm.put_parameter(
            Name='SENDER_EMAIL',
            Value=sender_email,
            Type='SecureString'
        )
        ssm.put_parameter(
            Name='EMAIL_PASSWORD',
            Value=email_password,
            Type='SecureString'
        )

        # Mock SMTP_SSL connection
        with patch('smtplib.SMTP_SSL') as mock_smtp:
            mock_connection = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_connection

            result = EmailHandler.send_birthday_emails(
                self.birthday_data,
                self.test_message
            )

            self.assertTrue(result)
            # Now checking for send_message instead of sendmail
            self.assertEqual(mock_connection.send_message.call_count, 2)

    @mock_aws
    def test_send_birthday_emails_smtp_failure(self):
        ssm = boto3.client('ssm', region_name='ap-southeast-1')

        sender_email = os.getenv("SENDER_EMAIL")
        email_password = os.getenv("EMAIL_PASSWORD")

        ssm.put_parameter(
            Name='SENDER_EMAIL',
            Value=sender_email,
            Type='SecureString'
        )
        ssm.put_parameter(
            Name='EMAIL_PASSWORD',
            Value=email_password,
            Type='SecureString'
        )

        with patch('smtplib.SMTP_SSL') as mock_smtp:
            mock_smtp.return_value.__enter__.side_effect = Exception("SMTP Error")

            result = EmailHandler.send_birthday_emails(
                self.birthday_data,
                self.test_message
            )

            self.assertFalse(result)

    @mock_aws
    def test_send_birthday_emails_missing_credentials(self):
        ssm = boto3.client('ssm', region_name='ap-southeast-1')

        result = EmailHandler.send_birthday_emails(
            self.birthday_data,
            self.test_message
        )

        # Assert the method returned False due to missing credentials
        self.assertFalse(result)
