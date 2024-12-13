import csv
from datetime import datetime, timezone
from venv import logger
from typing import List
import boto3


class BirthdayChecker:
    """
    Provides functionality to fetch and filter birthday data for the current date
    from a CSV file stored in an S3 bucket.

    This class includes a method to connect to an AWS S3 bucket, retrieve a specified
    CSV file, and extract a list of birthdays that match today's date (both day and
    month).

    :cvar logger: Logger used to log errors during file reading and processing.
    :type logger: logging.Logger
    """
    @staticmethod
    def get_todays_birthdays(bucket_name, file_key) -> List:
        """
        Retrieve the list of people whose birthdays are today based on a CSV file stored in an S3 bucket. The method reads
        the content of the file, processes the data to identify individuals matching the current day and month, and returns
        a list of those entries as dictionaries.

        :param bucket_name: Name of the Amazon S3 bucket containing the birthday CSV file.
        :type bucket_name: str
        :param file_key: Name of the key (file path) within the S3 bucket where the CSV file is stored.
        :type file_key: str
        :return: A list of dictionaries, where each dictionary represents an individual whose birthday is today.
        :rtype: List
        """
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
