from typing import Union

from src.birthday_wisher.helpers.llm_api_handlers.anthropic_handler import AnthropicHandler
from src.birthday_wisher.helpers.llm_api_handlers.openai_handler import OpenAIHandler


class LLMAPIFactory:
    """
    Factory class for managing and providing handlers for different AI service providers.

    This class is designed to provide a mechanism for retrieving handler instances
    corresponding to various AI providers. It uses a static mapping of providers to
    handler classes and ensures that only supported providers can be utilized. The
    class is not meant to be instantiated and will raise an exception if instantiation
    is attempted.

    :ivar handlers: A dictionary mapping provider names (in lowercase) to their
        corresponding handler classes. This is used to dynamically retrieve the
        appropriate handler based on the provider input.
    :type handlers: dict[str, type]

    """
    def __new__(cls, *args, **kwargs):
        raise RuntimeError('LLMAPIFactory should not be instantiated')

    handlers = {
        "openai": OpenAIHandler,
        "anthropic": AnthropicHandler
    }

    @staticmethod
    def get_handler(provider: str) -> Union[AnthropicHandler, OpenAIHandler]:
        """
        Retrieves the corresponding handler based on the given provider name.

        Allows dynamic selection of a handler class for a supported AI provider
        by referencing a predefined mapping. If the specified provider is not
        supported, an exception is raised.

        :param provider: Name of the AI provider for which the handler is to be
            retrieved.
        :type provider: str
        :return: A handler instance corresponding to the given AI provider.
        :rtype: Union[AnthropicHandler, OpenAIHandler]
        :raises ValueError: If the provided AI provider is not supported or is
            not available in the mapping.
        """
        handler_class = LLMAPIFactory.handlers.get(provider.lower())
        if not handler_class:
            raise ValueError(f"Unsupported AI provider: {provider}")
        return handler_class()