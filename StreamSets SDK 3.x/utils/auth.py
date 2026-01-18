"""
Authentication utilities for StreamSets Data Collector SDK 3.x
"""
import os
from dotenv import load_dotenv
from streamsets.sdk import DataCollector


def get_data_collector() -> DataCollector:
    """
    Authenticate and return a DataCollector instance.
    
    Returns:
        DataCollector: Authenticated DataCollector instance
        
    Raises:
        ValueError: If required environment variables are missing
    """
    load_dotenv()
    
    sdc_url = os.getenv('SDC_URL')
    sdc_username = os.getenv('SDC_USERNAME', 'admin')
    sdc_password = os.getenv('SDC_PASSWORD', 'admin')
    
    if not sdc_url:
        raise ValueError("SDC_URL must be set in environment variables")
    
    return DataCollector(sdc_url, username=sdc_username, password=sdc_password)


if __name__ == "__main__":
    # Test authentication
    sdc = get_data_collector()
    print(f"Successfully authenticated to {sdc.server_url}")

# Made with Bob
