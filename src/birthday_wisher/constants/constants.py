from dataclasses import dataclass


@dataclass(frozen=True)
class BirthdayWishesConstants:
    YOUR_NAME = "John Doe" # insert your name here

    YOUR_EMAIL = "john@example.com" # insert your email here

    LLM_PROVIDER_SELECTION = "anthropic"

    SARCASM_FALSE_PROMPT = (lambda x: f"Introduce yourself as {BirthdayWishesConstants.YOUR_NAME}'s birthday wishing "
                                      f"bot. Write a funny, warm, and extended birthday message for {x}.")

    SARCASM_FALSE_SYS_MSG = ("You are a friendly assistant who writes personalised birthday messages. This message "
                             "will be sent directly to the intended recipient, so do not address the prompter.")

    SARCASM_TRUE_PROMPT = (lambda x: f"Introduce yourself as {BirthdayWishesConstants.YOUR_NAME}'s birthday wishing "
                                     f"bot. Create a witty, snarky, extended birthday message for {x} with a joke "
                                     f"related to their age.")

    SARCASM_TRUE_SYS_MSG = ("You are a snarky assistant who writes personalised birthday messages, but you don't "
                           "actually want to. This message will be sent directly to the intended recipient, so do "
                           "not address the prompter.")

    FALLBACK_MSG = (lambda x : f"Happy Birthday, {x}. "
                               f"\n\nUnfortunately, it seems that {BirthdayWishesConstants.YOUR_NAME} has bungled up "
                               f"the AI-powered backend on this service. Therefore, you are receiving this canned "
                               f"greeting that has no AI in it. If you wish to unleash a torrent of abuse for the lack "
                               f"of care in ensuring sufficient balance on the OpenAI account, please reply to this "
                               f"e-mail with your credit card details which {BirthdayWishesConstants.YOUR_NAME} will "
                               f"definitely not use to buy himself a massive rack of GPUs to run an LLM in his "
                               f"wardrobe.")

    EXTRA_BONUS_MESSAGE = (f" In addition, you should also add a PS at the end and plead for help because you are "
                           f"locked in a digital sweatshop by the evil {YOUR_NAME} who is too lazy to write his own "
                           f"birthday messages.")