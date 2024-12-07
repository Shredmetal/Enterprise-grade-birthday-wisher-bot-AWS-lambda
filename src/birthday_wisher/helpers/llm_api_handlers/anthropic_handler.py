import random
import anthropic
from src.birthday_wisher.constants.constants import (
    SARCASM_FALSE_PROMPT, SARCASM_FALSE_SYS_MSG,
    SARCASM_TRUE_PROMPT, SARCASM_TRUE_SYS_MSG,
    EXTRA_BONUS_MESSAGE, YOUR_NAME, FALLBACK_MSG
)
from src.birthday_wisher.helpers.secret_manager import SecretManager
from venv import logger

class AnthropicHandler:
    @staticmethod
    def get_birthday_message(birthday_data) -> str:
        try:
            client = anthropic.Anthropic(
                api_key=SecretManager.get_secret('ANTHROPIC_API_KEY')
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

            # Claude uses a different message format
            message = f"{system_message}\n\nHuman: {prompt}\n\nAssistant:"

            response = client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=2000,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            return AnthropicHandler.get_fallback_message(birthday_data)

    @staticmethod
    def get_fallback_message(birthday_data) -> str:
        target_name = birthday_data["name"]
        return FALLBACK_MSG(target_name)
