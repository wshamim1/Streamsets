"""
Authentication utilities for StreamSets Platform SDK
"""
import os
from dotenv import load_dotenv
from streamsets.sdk import ControlHub


def get_control_hub() -> ControlHub:
    """
    Authenticate and return a ControlHub instance.
    
    Returns:
        ControlHub: Authenticated ControlHub instance
        
    Raises:
        ValueError: If required environment variables are missing
    """
    load_dotenv()
    
    cred_id = os.getenv('CRED_ID')
    cred_token = os.getenv('CRED_TOKEN')
    sch_url = os.getenv('SCH_URL', 'https://na01.hub.streamsets.com/')
    
    if not cred_id or not cred_token:
        raise ValueError("CRED_ID and CRED_TOKEN must be set in environment variables")
    
    return ControlHub(sch_url=sch_url, credential_id=cred_id, token=cred_token)


if __name__ == "__main__":
    # Test authentication
    sch = get_control_hub()
    print(f"Successfully authenticated to {sch.api_client.server_url}")

# Made with Bob
