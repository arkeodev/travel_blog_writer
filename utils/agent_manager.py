import base64
import io

import numpy as np
from autogen import GroupChat, GroupChatManager
from PIL import Image

from constants import MAX_CHAT_ROUNDS


class AgentManager:
    """
    Manages the interaction between agents.
    """

    def __init__(self, user_proxy, vision_assistant, blog_assistant):
        # Initialize the AgentManager with three agents
        self.user_proxy = user_proxy
        self.vision_assistant = vision_assistant
        self.blog_assistant = blog_assistant

    def run(self, image_data):
        """
        Runs the agent interaction to generate a blog post.
        """
        from utils.image_utils import encode_image

        # Encode the image data
        base64_image = encode_image(image_data)

        # Prepare the message with the encoded image
        message = f"""
        This is a picture of a specific travel destination.
        Please analyze the image carefully and identify the exact location shown.
        Do not default to any particular city or landmark.
        Provide detailed observations about what you see in the image that led to your conclusion.
        Then, based on the identified location, provide information about:
        1. The destination name
        2. Key attractions visible in the image or known to be in that location
        3. Common transportation options for tourists
        4. Types of accommodation available
        5. Popular local food or restaurants
        6. A brief description of the destination's significance or appeal

        <image>{base64_image}</image>
        """

        # Create a GroupChat instance with the three agents
        groupchat = GroupChat(
            agents=[self.user_proxy, self.vision_assistant, self.blog_assistant],
            messages=[],
            max_round=MAX_CHAT_ROUNDS,
        )

        # Create a GroupChatManager to manage the conversation
        manager = GroupChatManager(groupchat=groupchat)

        # Initiate the chat with the prepared message and return the result
        result = self.user_proxy.initiate_chat(manager, message=message)
        return result
