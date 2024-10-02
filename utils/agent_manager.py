import json

from autogen import GroupChat, GroupChatManager

from constants import MAX_CHAT_ROUNDS


class AgentManager:
    """
    Manages the interaction between agents.
    """

    def __init__(
        self, user_proxy, vision_assistant, blog_assistant, translation_assistant
    ):
        self.user_proxy = user_proxy
        self.vision_assistant = vision_assistant
        self.blog_assistant = blog_assistant
        self.translation_assistant = translation_assistant

    def run(self, image_url: str, language_code: str) -> str:
        """
        Runs the agent interaction to generate a blog post in the specified language.
        """
        message = f"""
        This is a picture of a famous destination.
        Please figure out the destination name, attractions, transportation, accommodation, food, and description.
        Generate a blog post based on the given information.
        Generate the content in {language_code}.
        <url>{image_url}</url>
        """
        groupchat = GroupChat(
            agents=[self.user_proxy, self.vision_assistant, self.blog_assistant],
            messages=[],
            max_round=MAX_CHAT_ROUNDS,
        )
        manager = GroupChatManager(groupchat=groupchat)

        try:
            vision_result = self.user_proxy.initiate_chat(manager, message=message)
        except Exception as e:
            print(f"Warning: An error occurred during chat initiation: {str(e)}")
            vision_result = self._get_last_message(groupchat)

        # Generate the blog post using the BlogAssistant
        blog_post = self.blog_assistant.generate_blog_post(vision_result, language_code)

        return blog_post

    def _get_last_message(self, groupchat):
        """
        Retrieves the last message from the group chat.
        """
        if not groupchat.messages:
            return "No chat messages available."

        last_message = groupchat.messages[-1]
        return last_message.get("content", "No content in the last message.")
