from autogen import GroupChat, GroupChatManager

from constants import MAX_CHAT_ROUNDS


class AgentManager:
    """
    Manages the interaction between agents.
    """

    def __init__(self, user_proxy, vision_assistant, blog_assistant):
        self.user_proxy = user_proxy
        self.vision_assistant = vision_assistant
        self.blog_assistant = blog_assistant

    def run(self, image_url: str) -> str:
        """
        Runs the agent interaction to generate a blog post.
        """
        message = f"""
        This is a picture of a famous destination.
        Please figure out the destination name, attractions, transportation, accommodation, food, and description.
        And then generate a blog post based on the given information.
        <url>{image_url}</url>
        """
        groupchat = GroupChat(
            agents=[self.user_proxy, self.vision_assistant, self.blog_assistant],
            messages=[],
            max_round=MAX_CHAT_ROUNDS,
        )
        manager = GroupChatManager(groupchat=groupchat)
        result = self.user_proxy.initiate_chat(manager, message=message)
        return result
