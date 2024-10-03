import base64
import io

import numpy as np
from autogen import GroupChat, GroupChatManager
from PIL import Image

from constants import MAX_CHAT_ROUNDS
from utils.image_utils import numpy_to_base64


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
        # Import necessary libraries for image processing
        import base64
        import io

        import numpy as np
        from PIL import Image

        # Check if the input is a numpy array (likely an image)
        if isinstance(image_data, np.ndarray):
            # Convert numpy array to base64 encoded image
            img_str = numpy_to_base64(image_data)
            # Prepare the message with the encoded image
            message = f"""
            This is a picture of a famous destination.
            Please figure out the destination name, attractions, transportation, accommodation, food, and description.
            And then generate a blog post based on the given information.
            <image>{img_str}</image>
            """
        else:
            # If not a numpy array, assume it's a URL
            message = f"""
            This is a picture of a famous destination.
            Please figure out the destination name, attractions, transportation, accommodation, food, and description.
            And then generate a blog post based on the given information.
            <url>{image_data}</url>
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
