from autogen import UserProxyAgent


class UserProxyAgent(UserProxyAgent):
    """
    User Proxy Agent.
    """

    def __init__(self):
        super().__init__(
            name="user_proxy", code_execution_config=False, human_input_mode="TERMINATE"
        )
