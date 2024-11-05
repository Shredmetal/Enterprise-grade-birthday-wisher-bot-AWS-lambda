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
            "sarcastic": True
        }

        self.test_message = "Test birthday message"

    @mock_aws
    def test_send_birthday_emails_mock(self):
        """Test email sending with mocked SMTP"""
        # Set up mock SSM
        ssm = boto3.client('ssm', region_name='us-east-1')

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

        # Mock SMTP connection
        with patch('smtplib.SMTP') as mock_smtp:
            mock_connection = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_connection

            result = EmailHandler.send_birthday_emails(
                self.birthday_data,
                self.test_message
            )

            self.assertTrue(result)
            self.assertEqual(mock_connection.sendmail.call_count, 2)

    @mock_aws
    def test_send_birthday_emails_real(self):
        """
        Test email sending with real SMTP connection

        IMPORTANT: Check your email inbox after running this test!
        Test recipient email: {test_email}
        Expected messages:
        1. Birthday wish
        2. Notification to Yourself
        """
        # Set up SSM
        ssm = boto3.client('ssm', region_name='us-east-1')

        # Get email credentials from .env
        sender_email = os.getenv("SENDER_EMAIL")
        email_password = os.getenv("EMAIL_PASSWORD")
        test_email = YOUR_EMAIL

        if not all([sender_email, email_password, test_email]):
            raise ValueError("Email credentials or test email not found in .env file")

        # Create parameters in SSM
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

        # Send real email
        print(f"\nSending real test email to: {test_email}")
        print("Please check your inbox for the test message!")

        result = EmailHandler.send_birthday_emails(
            self.birthday_data,
            self.test_message
        )

        self.assertTrue(result)
        print("\nEmails sent successfully. Please verify receipt in your inbox.")
        print(f"Test recipient email: {test_email}")
        print("Expected messages:")
        print("1. Birthday wish")
        print("2. Notification to yourself")

        # Add a small delay to allow emails to be sent
        time.sleep(2)

    @mock_aws
    def test_send_birthday_emails_smtp_failure(self):

        ssm = boto3.client('ssm', region_name='us-east-1')

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

        with patch('smtplib.SMTP') as mock_smtp:
            mock_smtp.return_value.__enter__.side_effect = Exception("SMTP Error")

            result = EmailHandler.send_birthday_emails(
                self.birthday_data,
                self.test_message
            )

            self.assertFalse(result)

    @mock_aws
    def test_send_birthday_emails_missing_credentials(self):

        ssm = boto3.client('ssm', region_name='us-east-1')

        result = EmailHandler.send_birthday_emails(
            self.birthday_data,
            self.test_message
        )

        # Assert the method returned False due to missing credentials
        self.assertFalse(result)
