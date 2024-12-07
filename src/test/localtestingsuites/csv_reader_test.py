import unittest
from moto import mock_aws
import boto3
from datetime import datetime, timezone
from src.birthday_wisher.helpers.get_birthdays import BirthdayChecker


class TestBirthdayChecker(unittest.TestCase):

    @mock_aws
    def test_get_todays_birthdays(self):

        s3 = boto3.client("s3", region_name="us-east-1")
        bucket_name = "mock_bucket"
        file_key = "birthdays.csv"
        current_day = datetime.now(timezone.utc).strftime("%d")
        current_month = datetime.now(timezone.utc).strftime("%m")

        s3.create_bucket(Bucket = bucket_name)

        s3.create_bucket(Bucket=bucket_name)

        test_data = f"""name,email,month,day
John Doe,john@example.com,{current_month},{current_day}
Jane Smith,jane@example.com,12,25
"""

        s3.put_object(Bucket=bucket_name, Key=file_key, Body=test_data)

        expected_result = [{'name': 'John Doe', 'email': 'john@example.com', 'month': f'{current_month}', 'day': f'{current_day}'}]
        result = BirthdayChecker.get_todays_birthdays(bucket_name, file_key)

        self.assertEqual(result, expected_result)

