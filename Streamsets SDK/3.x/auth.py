import os
from dotenv import load_dotenv
from streamsets.sdk import ControlHub

class StreamSetsAuth:
    """
    Handles authentication and loading credentials from environment variables.
    """
    def __init__(self):
        load_dotenv()
        self.control_hub_url = os.getenv("CONTROL_HUB_URL")
        self.control_hub_user = os.getenv("CONTROL_HUB_USER")
        self.control_hub_pw = os.getenv("CONTROL_HUB_PW")

    def authenticate(self):
        """Authenticates with StreamSets Control Hub and returns a ControlHub object."""
        return ControlHub(self.control_hub_url, username=self.control_hub_user, password=self.control_hub_pw)
