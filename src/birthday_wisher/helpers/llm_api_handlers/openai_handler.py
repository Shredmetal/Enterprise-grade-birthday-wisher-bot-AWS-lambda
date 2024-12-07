import random
import openai
from src.birthday_wisher.constants.constants import SARCASM_FALSE_PROMPT, SARCASM_FALSE_SYS_MSG, SARCASM_TRUE_PROMPT, \
    SARCASM_TRUE_SYS_MSG, EXTRA_BONUS_MESSAGE, YOUR_NAME, FALLBACK_MSG
from src.birthday_wisher.helpers.secret_manager import SecretManager
from venv import logger


class OpenAIHandler:

    @staticmethod
    def get_birthday_message(birthday_data) -> str:

        try:
            client = openai.Client(
                api_key=SecretManager.get_secret('OPENAI_API_KEY')
            )

            target_name = birthday_data["name"]
            sarcasm_setting = bool(birthday_data["sarcastic"])

            if random.random() < 0.1:
                extra_message = EXTRA_BONUS_MESSAGE
            else:
                extra_message = ""

            if not sarcasm_setting:
                prompt = SARCASM_FALSE_PROMPT(target_name)

                system_message = SARCASM_FALSE_SYS_MSG
            else:
                prompt = SARCASM_TRUE_PROMPT(target_name)
                system_message = (SARCASM_TRUE_SYS_MSG + extra_message)


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

        target_name = birthday_data["name"]

        """Fallback message if OpenAI fails"""
        template = FALLBACK_MSG(target_name)

        return template
