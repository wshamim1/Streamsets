"""
Configuration utilities for StreamSets Platform SDK
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv


def load_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables.
    
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    load_dotenv()
    
    return {
        'cred_id': os.getenv('CRED_ID'),
        'cred_token': os.getenv('CRED_TOKEN'),
        'sch_url': os.getenv('SCH_URL', 'https://na01.hub.streamsets.com/'),
    }


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate that required configuration values are present.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_keys = ['cred_id', 'cred_token', 'sch_url']
    return all(config.get(key) for key in required_keys)

# Made with Bob
