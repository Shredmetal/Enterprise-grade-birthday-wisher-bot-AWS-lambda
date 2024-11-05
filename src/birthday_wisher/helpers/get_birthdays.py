import csv
from datetime import datetime, timezone
from venv import logger
import boto3


class BirthdayChecker:
    @staticmethod
    def get_todays_birthdays(bucket_name, file_key):
        """Get today's birthdays using simple CSV reading"""
        try:
            s3 = boto3.client('s3')
            response = s3.get_object(Bucket=bucket_name, Key=file_key)
            lines = response['Body'].read().decode('utf-8-sig').splitlines()

            current_day = datetime.now(timezone.utc).strftime("%d")
            current_month = datetime.now(timezone.utc).strftime("%m")

            todays_birthdays = []
            reader = csv.DictReader(lines)

            for row in reader:
                if (row['day'].zfill(2) == current_day and
                        row['month'].zfill(2) == current_month):
                    todays_birthdays.append(row)

            return todays_birthdays

        except Exception as e:
            logger.error(f"Error reading birthday data: {str(e)}")
            return []
