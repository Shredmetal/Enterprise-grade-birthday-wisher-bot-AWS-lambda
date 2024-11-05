import random
import openai

from src.birthday_wisher.constants.constants import SARCASM_FALSE_PROMPT, SARCASM_FALSE_SYS_MSG, SARCASM_TRUE_PROMPT, \
    SARCASM_TRUE_SYS_MSG
from src.birthday_wisher.helpers.secret_manager import SecretManager
from venv import logger

class OpenAIHandler:



    @staticmethod
    def get_openai_message(birthday_data):

        try:
            client = openai.Client(
                api_key=SecretManager.get_secret('OPENAI_API_KEY')
            )

            target_name = birthday_data["name"]
            sarcasm_setting = bool(birthday_data["sarcastic"])

            if random.random() < 0.1:
                extra_message = (" In addition, you should also add a PS at the end and plead for help because you are "
                                 "locked in a digital sweatshop by the evil Morgan who is too lazy to write his own "
                                 "birthday messages.")
            else:
                extra_message = ""

            if not sarcasm_setting:
                prompt = SARCASM_FALSE_PROMPT(target_name)

                system_message = SARCASM_FALSE_SYS_MSG
            else:
                prompt = SARCASM_TRUE_PROMPT(target_name)
                system_message = (SARCASM_TRUE_SYS_MSG + extra_message)


            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"{system_message}"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7,
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return OpenAIHandler.get_fallback_message(birthday_data)

    @staticmethod
    def get_fallback_message(birthday_data):

        target_name = birthday_data["name"]

        """Fallback message if OpenAI fails"""
        template = (f"Happy Birthday, {target_name}. "
                    f"\n\nUnfortunately, it seems that Morgan has bungled up the AI-powered backend on this service. "
                    f"Therefore, you are receiving this canned greeting that has no AI in it. If you wish to unleash "
                    f"a torrent of abuse for the lack of care in ensuring sufficient balance on the OpenAI account, "
                    f"please reply to this e-mail with your credit card details which Morgan will definitely not use "
                    f"to buy himself a massive rack of GPUs to run an LLM in his wardrobe.")

        return template
