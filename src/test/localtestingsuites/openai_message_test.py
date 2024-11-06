import os
import unittest
import boto3
from dotenv import load_dotenv
from moto import mock_aws

from src.birthday_wisher.constants.constants import YOUR_NAME
from src.birthday_wisher.helpers.openai_handler import OpenAIHandler

load_dotenv()

class TestOpenAIMessage(unittest.TestCase):

    @mock_aws
    def test_get_openai_message(self):

        ssm = boto3.client('ssm', region_name='us-east-1')

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key not found in environment variables")

        ssm.put_parameter(
            Name='OPENAI_API_KEY',
            Value=api_key,
            Type='SecureString'
        )

        try:
            response = ssm.get_parameter(
                Name='OPENAI_API_KEY',
                WithDecryption=True
            )
            print(f"Parameter verification - Retrieved value: {response['Parameter']['Value']}\n")
        except Exception as e:
            print(f"Error verifying parameter: {str(e)}")
            raise

        birthday_data = {
            "name": "John Doe",
            "sarcastic": "true"
        }

        result = OpenAIHandler.get_openai_message(birthday_data)

        print(f"Result From OpenAI: {result}")

        # Assert that we got a non-empty response - THIS WILL ALWAYS PASS - CHECK THE OUTPUT
        self.assertTrue(result)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    @mock_aws
    def test_openai_message_failure(self):
        birthday_data = {
            "name": "John Doe",
            "sarcastic": True
        }

        # Don't set up any SSM parameters - this will cause the OpenAI call to fail
        ssm = boto3.client('ssm', region_name='us-east-1')
        result = OpenAIHandler.get_openai_message(birthday_data)

        expected_message = (f"Happy Birthday, {birthday_data['name']}. "
                            f"\n\nUnfortunately, it seems that {YOUR_NAME} has bungled up the AI-powered backend on this service. "
                            f"Therefore, you are receiving this canned greeting that has no AI in it. If you wish to unleash "
                            f"a torrent of abuse for the lack of care in ensuring sufficient balance on the OpenAI account, "
                            f"please reply to this e-mail with your credit card details which {YOUR_NAME} will definitely not use "
                            f"to buy himself a massive rack of GPUs to run an LLM in his wardrobe.")

        print(f"OpenAI Failed Fallback: {result}")

        self.assertEqual(result, expected_message)
        self.assertIn(birthday_data['name'], result)
        self.assertIn(f"{YOUR_NAME} has bungled", result)




