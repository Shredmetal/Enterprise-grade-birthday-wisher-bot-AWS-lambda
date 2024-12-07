import boto3
from venv import logger

class SecretManager:

    @staticmethod
    def get_secret(secret_name) -> str:
        ssm = boto3.client('ssm', region_name='ap-southeast-1')
        try:
            response = ssm.get_parameter(
                Name=secret_name,
                WithDecryption=True
            )
            return response['Parameter']['Value']

        except Exception as e:
            logger.error(f"Error retrieving parameter: {str(e)}")
            raise