import re
from types import SimpleNamespace

from instructor import Mode, from_openai
from openai import OpenAI

from config import Config
from models.travel_destination import TravelDestination


class CustomLLama32VisionClient:
    """
    Custom client to interact with Llama 3.2 Vision model.
    """

    def __init__(self, config, **kwargs):
        # Initialize the client with configuration and API details
        self.config = config
        self.api_key = Config.FIREWORKS_API_KEY
        self.base_url = "https://api.fireworks.ai/inference/v1"
        # Create an OpenAI client with custom base URL and API key
        # Use 'instructor' to wrap the client for structured output handling
        self.client = from_openai(
            OpenAI(base_url=self.base_url, api_key=self.api_key), mode=Mode.JSON
        )

    def create(self, params):
        try:
            new_messages = self._transform_messages(params["messages"])
            response = self.client.chat.completions.create(
                model="accounts/fireworks/models/llama-v3p2-90b-vision-instruct",
                messages=new_messages,
                response_model=TravelDestination,
            )
            autogen_response = self._build_autogen_response(response)
            return autogen_response
        except Exception as e:
            print(f"Error in vision model processing: {str(e)}")
            raise

    def _transform_messages(self, messages):
        new_messages = []
        for message in messages:
            if message["role"] == "user":
                new_content = []
                text_content = message["content"]
                # Extract image data from the message content
                image_data = re.search(r"<image>(.*?)</image>", text_content, re.DOTALL)
                if image_data:
                    base64_image = image_data.group(1)
                    new_content.append(
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        }
                    )
                    # Remove the image tags from the text content
                    text_content = re.sub(
                        r"<image>.*?</image>", "", text_content, flags=re.DOTALL
                    ).strip()
                if text_content:
                    new_content.insert(0, {"type": "text", "text": text_content})
                new_messages.append({"role": "user", "content": new_content})
        return new_messages

    def _build_autogen_response(self, response):
        # Create a SimpleNamespace object to mimic the structure of an autogen response
        autogen_response = SimpleNamespace()
        autogen_response.choices = []
        autogen_response.model = "custom_llama32_vision"

        choice = SimpleNamespace()
        choice.message = SimpleNamespace()
        # Convert the structured response to JSON string
        choice.message.content = response.model_dump_json()
        choice.message.function_call = None
        autogen_response.choices.append(choice)
        return autogen_response

    def message_retrieval(self, response):
        # Extract the content from each choice in the response
        choices = response.choices
        return [choice.message.content for choice in choices]

    def cost(self, response) -> float:
        # Set a placeholder cost (0) for the response
        response.cost = 0
        return 0

    @staticmethod
    def get_usage(response):
        # Return an empty dictionary for usage information
        return {}
