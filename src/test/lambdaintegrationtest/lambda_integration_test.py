import os
import unittest
import io
import boto3

from src.birthday_wisher.helpers.secret_manager import SecretManager


class TestLambdaIntegration(unittest.TestCase):
    """Tests that run in Lambda environment to verify AWS service integration"""

    def setUp(self):
        """Set up test environment"""
        self.ssm = boto3.client('ssm')
        self.s3 = boto3.client('s3')
        self.bucket_name = os.environ['BUCKET_NAME']
        self.file_key = os.environ['FILE_KEY']

    def test_ssm_parameters_exist(self):
        """Test that required SSM parameters exist and are accessible"""
        required_params = [
            'ANTHROPIC_API_KEY',
            'OPENAI_API_KEY',
            'SENDER_EMAIL',
            'EMAIL_PASSWORD'
        ]

        for param_name in required_params:
            try:
                response = self.ssm.get_parameter(
                    Name=param_name,
                    WithDecryption=True
                )
                self.assertIsNotNone(response['Parameter']['Value'])
            except Exception as e:
                self.fail(f"Failed to get SSM parameter {param_name}: {str(e)}")

    def test_secret_manager_retrieval(self):
        """Test that SecretManager can retrieve all required secrets"""
        secret_manager = SecretManager()
        required_params = [
            'ANTHROPIC_API_KEY',
            'OPENAI_API_KEY',
            'SENDER_EMAIL',
            'EMAIL_PASSWORD'
        ]

        for param_name in required_params:
            try:
                value = secret_manager.get_secret(param_name)
                self.assertIsNotNone(value)
                self.assertTrue(len(value) > 0,
                                f"Secret {param_name} exists but is empty")
            except Exception as e:
                self.fail(f"SecretManager failed to get parameter {param_name}: {str(e)}")

    def test_s3_bucket_accessible(self):
        """Test that S3 bucket exists and is accessible"""
        try:
            response = self.s3.head_bucket(Bucket=self.bucket_name)
            self.assertTrue(True)  # If we get here, bucket exists and is accessible
        except Exception as e:
            self.fail(f"Failed to access S3 bucket {self.bucket_name}: {str(e)}")

    def test_birthdays_file_exists(self):
        """Test that birthdays.csv exists in S3"""
        try:
            response = self.s3.head_object(
                Bucket=self.bucket_name,
                Key=self.file_key
            )
            self.assertTrue(True)  # If we get here, file exists
        except Exception as e:
            self.fail(f"Failed to access file {self.file_key}: {str(e)}")

    def test_birthdays_file_format(self):
        """Test that birthdays.csv has correct format"""
        try:
            response = self.s3.get_object(
                Bucket=self.bucket_name,
                Key=self.file_key
            )
            content = response['Body'].read().decode('utf-8-sig')
            lines = content.splitlines()

            # Check header - matching actual column order
            expected_headers = ['name', 'email', 'day', 'month', 'sarcastic']
            actual_headers = lines[0].lower().split(',')
            self.assertEqual(expected_headers, actual_headers)

            # Check at least one data row
            if len(lines) > 1:
                data_row = lines[1].split(',')
                self.assertEqual(len(expected_headers), len(data_row))
        except Exception as e:
            self.fail(f"Failed to validate file format: {str(e)}")

def run_lambda_tests():
    """Run Lambda integration tests"""
    buffer = io.StringIO()
    runner = unittest.TextTestRunner(stream=buffer, verbosity=2)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestLambdaIntegration)
    result = runner.run(suite)

    output = buffer.getvalue()

    response = {
        'statusCode': 200 if result.wasSuccessful() else 500,
        'body': {
            'test_output': output,
            'tests_run': result.testsRun,
            'errors': len(result.errors),
            'failures': len(result.failures),
            'skipped': len(result.skipped)
        }
    }

    return response