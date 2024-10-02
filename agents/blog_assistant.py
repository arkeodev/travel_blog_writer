import json

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
            system_message="You are an assistant that can generate blog posts based on the given information in various languages. Generate the content in the specified language and format the output as a JSON object with a 'blog_post' field containing the generated blog post.",
            llm_config={
                "config_list": config_list_text,
                "cache": None,
                "cache_seed": None,
            },
        )

    def generate_blog_post(self, travel_info: str, language_code: str) -> str:
        try:
            # Try to parse the travel_info as JSON
            travel_data = json.loads(travel_info)
        except json.JSONDecodeError:
            # If parsing fails, use the string as is
            travel_data = {"description": travel_info}
        except Exception as e:
            # If any other error occurs, use a default message
            print(f"Warning: Error processing travel info: {str(e)}")
            travel_data = {
                "description": "Information about the destination is unavailable."
            }

        # Generate the blog post based on the travel data
        blog_post = f"Welcome to our exciting destination!\n\n"

        if isinstance(travel_data, dict):
            if travel_data.get("destination_name"):
                blog_post = f"Welcome to {travel_data['destination_name']}!\n\n"
            if travel_data.get("description"):
                blog_post += f"{travel_data['description']}\n\n"
            if travel_data.get("attractions"):
                blog_post += "Top attractions:\n"
                for attraction in travel_data["attractions"]:
                    blog_post += f"- {attraction}\n"
            # Add more sections based on available data...
        else:
            # If travel_data is not a dict, use it as the blog post content
            blog_post += str(travel_data)

        # Wrap the blog post in a JSON object
        return json.dumps({"blog_post": blog_post})
