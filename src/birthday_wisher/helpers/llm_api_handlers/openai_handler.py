import random
import openai
from src.birthday_wisher.constants.constants import BirthdayWishesConstants
from src.birthday_wisher.helpers.secret_manager import SecretManager
from venv import logger


class OpenAIHandler:
    """
    Provides functionality to generate birthday messages using OpenAI's API,
    with options for sarcasm and fallback mechanism in case of API failure.

    This class includes methods to handle the creation of both API-based
    customized birthday messages and static fallback messages. The primary
    use case is to ensure a birthday message is always available, even if
    there are issues with the API.

    :ivar NONE: This class does not have class-level attributes.
    """
    @staticmethod
    def get_birthday_message(birthday_data) -> str:
        """
        Generates a birthday message using the OpenAI API based on given data.

        This static method interacts with the OpenAI API to generate a birthday message. Depending on the
        'sarcastic' flag provided in the `birthday_data`, it chooses an appropriate prompt and system
        message to send to the API. In the event of an API failure, it logs the error and returns a
        fallback message. The method also incorporates a small probability of appending an extra bonus
        prompt to generate the output.

        :param birthday_data: A dictionary containing data required to generate the birthday message.
            Expected keys include:
            - 'name': A string representing the target individual's name.
            - 'sarcastic': A string ("true" or "false") indicating if the message should be sarcastic.
        :return: A string containing the generated birthday message. Defaults to a fallback message if
            an error occurs.
        """
        try:
            client = openai.Client(
                api_key=SecretManager.get_secret('OPENAI_API_KEY')
            )

            target_name = birthday_data["name"]
            sarcasm_setting = birthday_data["sarcastic"].lower() == "true"

            if random.random() < 0.1:
                extra_message = BirthdayWishesConstants.EXTRA_BONUS_MESSAGE
            else:
                extra_message = ""

            if not sarcasm_setting:
                prompt = BirthdayWishesConstants.SARCASM_FALSE_PROMPT(target_name)

                system_message = BirthdayWishesConstants.SARCASM_FALSE_SYS_MSG
            else:
                prompt = BirthdayWishesConstants.SARCASM_TRUE_PROMPT(target_name)
                system_message = (BirthdayWishesConstants.SARCASM_TRUE_SYS_MSG + extra_message)


            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"{system_message}"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7,
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return OpenAIHandler.get_fallback_message(birthday_data)

    @staticmethod
    def get_fallback_message(birthday_data) -> str:
        """
        Generates a fallback birthday message using the provided birthday data.

        The method retrieves the recipient's name from the input data and utilizes
        a predefined fallback message format to generate a personalized birthday
        message. It ensures that a meaningful string is returned even when specific
        customized birthday content is unavailable.

        :param birthday_data: A dictionary containing the birthday recipient's
            information. The dictionary must include the key "name" mapped to the
            recipient’s name (type: str).
        :return: A string representing the fallback birthday message for the given
            recipient’s name.
        :rtype: str
        """
        target_name = birthday_data["name"]
        template = BirthdayWishesConstants.FALLBACK_MSG(target_name)

        return template
