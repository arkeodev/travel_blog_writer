from autogen import AssistantAgent

from config import Config


class TranslationAssistant(AssistantAgent):
    """
    Translation Assistant Agent powered by Llama 3.2 11B Instruct model.
    """

    def __init__(self):
        config_list_text = [
            {
                "model": "accounts/fireworks/models/llama-v3p2-11b-vision-instruct",
                "api_key": Config.FIREWORKS_API_KEY,
                "base_url": "https://api.fireworks.ai/inference/v1",
            }
        ]
        super().__init__(
            name="translation_assistant",
            system_message="You are an assistant that can translate text to various languages. Translate the given text to the specified language accurately and fluently.",
            llm_config={
                "config_list": config_list_text,
                "cache": None,
                "cache_seed": None,
            },
        )
