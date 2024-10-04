from autogen import AssistantAgent

from agents.custom_llama32_vision_client import CustomLLama32VisionClient


class VisionAssistant(AssistantAgent):
    """
    Vision Assistant Agent powered by Llama 3.2 Vision model.
    """

    def __init__(self):
        config_list = [
            {
                "model": "custom_llama32_vision",
                "model_client_cls": "CustomLLama32VisionClient",
            }
        ]
        super().__init__(
            name="vision_assistant",
            system_message="You are a multi-modal assistant that can generate structured outputs from images. Always provide a confidence score with your identification.",
            llm_config={"config_list": config_list, "cache": None, "cache_seed": None},
        )
        self.register_model_client(model_client_cls=CustomLLama32VisionClient)
