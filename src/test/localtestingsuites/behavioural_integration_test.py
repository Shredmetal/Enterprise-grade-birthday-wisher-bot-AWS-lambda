import os
import unittest
import boto3
from dotenv import load_dotenv
from llm_app_test.behavioral_assert.behavioral_assert import BehavioralAssertion
from moto import mock_aws

from src.birthday_wisher.helpers.llm_api_factory import LLMAPIFactory

load_dotenv()

class TestAnthropicMessage(unittest.TestCase):
    """
    Unittest class for testing interactions with LLM API handlers and parameter
    store within a mocked AWS environment.

    This class contains unit tests to verify the behavior of message generation
    from actual LLM API handlers (Anthropic and OpenAI). It uses llm-app-test to
    validate behavioral matches between generated messages and expected outputs
    in order to ensure that the system and human prompts are getting the right
    behavior out of the LLMs.

    :ivar behavioral_asserter: Utility for asserting behavioral match between
        generated messages and expected outputs.
    :type behavioral_asserter: BehavioralAssertion
    """
    def setUp(self):
        self.behavioral_asserter = BehavioralAssertion()

    @mock_aws
    def test_get_anthropic_message(self):

        ssm = boto3.client('ssm', region_name='ap-southeast-1')

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("API key not found in environment variables")

        ssm.put_parameter(
            Name='ANTHROPIC_API_KEY',
            Value=api_key,
            Type='SecureString'
        )

        try:
            response = ssm.get_parameter(
                Name='ANTHROPIC_API_KEY',
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

        llm_provider = LLMAPIFactory.get_handler("anthropic")

        result = llm_provider.get_birthday_message(birthday_data)

        print(f"Result From Anthropic: {result}")

        self.behavioral_asserter.assert_behavioral_match(result, "A sarcastic birthday greeting to John Doe")

    @mock_aws
    def test_get_openai_message(self):

        ssm = boto3.client('ssm', region_name='ap-southeast-1')

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

        llm_provider = LLMAPIFactory.get_handler("openai")

        result = llm_provider.get_birthday_message(birthday_data)

        print(f"Result From OpenAI: {result}")

        self.behavioral_asserter.assert_behavioral_match(result, "A sarcastic birthday greeting to John Doe")





