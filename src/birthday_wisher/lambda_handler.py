import os
from venv import logger

from src.birthday_wisher.constants.constants import BirthdayWishesConstants
from src.birthday_wisher.helpers.email_handler import EmailHandler
from src.birthday_wisher.helpers.get_birthdays import BirthdayChecker
from src.birthday_wisher.helpers.llm_api_factory import LLMAPIFactory
from src.test.lambdaintegrationtest.lambda_integration_test import run_lambda_tests


def lambda_handler(event, context):
    """
    Handles the AWS Lambda function execution for sending birthday emails. This function
    checks for any birthdays occurring on the current day, retrieves personalized birthday
    messages through an LLM (Large Language Model) provider, and sends the messages via
    email. Additionally, it processes success and failure results and generates a response
    documenting the execution summary.

    If the execution environment includes `test_mode` set to True, the function performs
    lambda tests instead of normal execution.

    :param event: The event data passed to the Lambda function. Expected to be an AWS event,
                  which can include additional keys like 'test_mode' for specific behavior.
    :type event: dict
    :param context: The runtime context of the Lambda function, provided by AWS Lambda
                    during function execution. Contains runtime and invocation metadata.
    :type context: object
    :return: Returns a response dictionary including HTTP status code and execution
             details. If no birthdays are found, a message indicating no birthdays is
             returned. In case of exceptions, a 500 status code along with the error
             message is returned.
    :rtype: dict
    """
    if event.get('test_mode', False):
        return run_lambda_tests()

    try:
        bucket_name = os.environ['BUCKET_NAME']
        file_key = os.environ['FILE_KEY']

        todays_birthdays = BirthdayChecker.get_todays_birthdays(bucket_name, file_key)

        if not todays_birthdays:
            return {
                'statusCode': 200,
                'body': 'No birthdays today'
            }

        results = []

        for birthday_data in todays_birthdays:
            try:
                llm_provider = LLMAPIFactory.get_handler(BirthdayWishesConstants.LLM_PROVIDER_SELECTION)

                email_text = llm_provider.get_birthday_message(birthday_data)

                success = EmailHandler.send_birthday_emails(birthday_data, email_text)

                results.append({
                    'name': birthday_data['name'],
                    'success': success,
                    'message': 'Email sent successfully' if success else 'Failed to send email'
                })

            except Exception as e:
                logger.error(f"Error processing birthday for {birthday_data['name']}: {str(e)}")
                results.append({
                    'name': birthday_data['name'],
                    'success': False,
                    'message': f'Error: {str(e)}'
                })

        total_processed = len(results)
        successful_sends = sum(1 for r in results if r['success'])
        failed_sends = total_processed - successful_sends

        response = {
            'statusCode': 200 if failed_sends == 0 else 207,  # 207 Multi-Status if some failed
            'body': {
                'summary': f"Processed {total_processed} birthdays: {successful_sends} successful, {failed_sends} failed",
                'details': results
            }
        }

        return response

    except Exception as e:
        error_message = f"Critical error in lambda function: {str(e)}"
        logger.error(error_message)
        return {
            'statusCode': 500,
            'body': error_message
        }
