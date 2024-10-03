from autogen import AssistantAgent

from config import Config


class BlogAssistant(AssistantAgent):
    """
    Blog Assistant Agent powered by Llama 3.2 11B Instruct model.
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
            name="blog_assistant",
            system_message="You are an assistant that can generate blog posts based on the given information. Terminate your response with TERMINATE.",
            llm_config={
                "config_list": config_list_text,
                "cache": None,
                "cache_seed": None,
            },
        )

