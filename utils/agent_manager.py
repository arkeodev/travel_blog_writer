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
        self.user_proxy = user_proxy
        self.vision_assistant = vision_assistant
        self.blog_assistant = blog_assistant

    def run(self, image_data):
        """
        Runs the agent interaction to generate a blog post.
        """
        import base64
        import io

        import numpy as np
        from PIL import Image

        if isinstance(image_data, np.ndarray):
            # Convert numpy array to base64 encoded image
            img = Image.fromarray((image_data * 255).astype(np.uint8))
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            message = f"""
            This is a picture of a famous destination.
            Please figure out the destination name, attractions, transportation, accommodation, food, and description.
            And then generate a blog post based on the given information.
            <image>{img_str}</image>
            """
        else:
            # Assume it's a URL if it's not a numpy array
            message = f"""
            This is a picture of a famous destination.
            Please figure out the destination name, attractions, transportation, accommodation, food, and description.
            And then generate a blog post based on the given information.
            <url>{image_data}</url>
            """

        groupchat = GroupChat(
            agents=[self.user_proxy, self.vision_assistant, self.blog_assistant],
            messages=[],
            max_round=MAX_CHAT_ROUNDS,
        )
        manager = GroupChatManager(groupchat=groupchat)
        result = self.user_proxy.initiate_chat(manager, message=message)
        return result
