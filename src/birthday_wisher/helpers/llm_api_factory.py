from typing import Union

from src.birthday_wisher.helpers.llm_api_handlers.anthropic_handler import AnthropicHandler
from src.birthday_wisher.helpers.llm_api_handlers.openai_handler import OpenAIHandler


class LLMAPIFactory:
    """Static factory class for getting AI handlers"""
    def __new__(cls, *args, **kwargs):
        raise RuntimeError('LLMAPIFactory should not be instantiated')

    handlers = {
        "openai": OpenAIHandler,
        "anthropic": AnthropicHandler
    }

    @staticmethod
    def get_handler(provider: str) -> Union[AnthropicHandler, OpenAIHandler]:
        handler_class = LLMAPIFactory.handlers.get(provider.lower())
        if not handler_class:
            raise ValueError(f"Unsupported AI provider: {provider}")
        return handler_class()