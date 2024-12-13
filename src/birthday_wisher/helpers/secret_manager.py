import boto3
from venv import logger

class SecretManager:
    """
    Provides functionality to manage and retrieve secrets from AWS Systems Manager (SSM).

    This class is designed to interact with AWS SSM to fetch secure parameters. It uses the
    boto3 library to interact with the AWS API. Secrets are encrypted and require decryption
    during retrieval. Typical use cases include fetching sensitive information such as API
    keys, passwords, and other confidential data stored securely in SSM.
    """
    @staticmethod
    def get_secret(secret_name) -> str:
        """
        Retrieves the decrypted value of a secret parameter from AWS Systems Manager Parameter Store
        specified by its name.

        This function interfaces with the AWS boto3 library to fetch a parameter from the Parameter
        Store within a specified region. It handles all errors by logging them and re-raising the
        exceptions to ensure the calling function is made aware of the issue.

        :param secret_name: The name of the parameter to be retrieved from AWS Systems Manager Parameter
            Store. This parameter must exist in the store and be accessible with appropriate IAM
            permissions.
        :type secret_name: str

        :return: The decrypted value of the parameter retrieved from the AWS Systems Manager Parameter
            Store.
        :rtype: str

        :raises Exception: If there is any problem during retrieval or decryption of the parameter, an
            exception related to the error is raised.
        """
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