from dataclasses import dataclass


@dataclass(frozen=True)
class BirthdayWishesConstants:
    """
    Constants class for generating birthday messages with and without sarcasm.

    This class contains attributes and constants used to configure the behavior of a
    birthday wishing bot. It is designed for generating customized birthday messages,
    either in a warm and funny tone or in a snarky and witty tone, depending on the
    chosen settings. The class is immutable as indicated by the use of ``@dataclass(frozen=True)``.
    The constants also include default provider selection for language models and
    fallback mechanism in case of system errors.

    :ivar YOUR_NAME: Your personal name, used in the birthday message. Insert your name here.
    :type YOUR_NAME: str
    :ivar YOUR_EMAIL: Your personal email address, used by the bot to send you an email telling you it has sent something.
    :type YOUR_EMAIL: str
    :ivar LLM_PROVIDER_SELECTION: The default language model provider used for generating messages.
    :type LLM_PROVIDER_SELECTION: str
    :ivar SARCASM_FALSE_PROMPT: Lambda function generating a warm and funny formatting prompt for the specified recipient.
    :type SARCASM_FALSE_PROMPT: Callable[[str], str]
    :ivar SARCASM_FALSE_SYS_MSG: Instruction for the assistant to act as a friendly and warm birthday bot.
    :type SARCASM_FALSE_SYS_MSG: str
    :ivar SARCASM_TRUE_PROMPT: Lambda function generating a witty, snarky, and humorous formatting prompt for the recipient.
    :type SARCASM_TRUE_PROMPT: Callable[[str], str]
    :ivar SARCASM_TRUE_SYS_MSG: Instruction for the assistant to act as a sarcastic birthday bot containing humor and age-related jokes.
    :type SARCASM_TRUE_SYS_MSG: str
    :ivar FALLBACK_MSG: Lambda function defining the fallback message to be sent if the system fails.
    :type FALLBACK_MSG: Callable[[str], str]
    :ivar EXTRA_BONUS_MESSAGE: Additional default text appended to prompt for humorous effect regarding bot's condition.
    :type EXTRA_BONUS_MESSAGE: str
    """
    YOUR_NAME = "John" # insert your name here

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