import os
from dotenv import load_dotenv
from streamsets.sdk import ControlHub


class StreamSetsAuth:
    """
    Handles authentication with either StreamSets SDK 3.x or Platform SDK based on .env input.
    """
    def __init__(self):
        load_dotenv()
        self.control_hub_url = os.getenv("CONTROL_HUB_URL")
        self.control_hub_user = os.getenv("CONTROL_HUB_USER")
        self.control_hub_pw = os.getenv("CONTROL_HUB_PW")
        self.control_hub_token = os.getenv("CONTROL_HUB_TOKEN")
        self.auth_type = os.getenv("AUTH_TYPE", "3x")  # Default to 3.x SDK
    
    def authenticate(self):
        """Authenticates using the appropriate SDK based on AUTH_TYPE."""
        if self.auth_type.lower() == "platform":
            if not self.control_hub_token:
                raise ValueError("API Token is required for Platform SDK authentication.")
            print("Authenticating with StreamSets Platform SDK...")
            return ControlHubSession(token=self.control_hub_token, url=self.control_hub_url)
        else:
            print("Authenticating with StreamSets 3.x SDK...")
            return ControlHub(self.control_hub_url, username=self.control_hub_user, password=self.control_hub_pw)

if __name__ == "__main__":
    auth = StreamSetsAuth()
    control_hub = auth.authenticate()
    print("Authentication successful.")
