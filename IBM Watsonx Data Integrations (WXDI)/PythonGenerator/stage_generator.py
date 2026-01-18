from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration import Platform
from ibm_watsonx_data_integration.services.streamsets.api import *
from ibm_watsonx_data_integration.services.datastage import *
from ibm_watsonx_data_integration.services.streamsets import *
from ibm_watsonx_data_integration.codegen import PythonGenerator

import random
import string
import os

from dotenv import load_dotenv

load_dotenv()



# Read API key from .env file
api_key = os.getenv('IBM_WATSONX_API_KEY')

if not api_key:
    raise ValueError("IBM_WATSONX_API_KEY environment variable not found.")

auth = IAMAuthenticator(api_key)


auth = IAMAuthenticator(api_key=api_key)
platform = Platform(auth, base_api_url=os.getenv('WATSONX_BASE_URL', 'https://api.ca-tor.dai.cloud.ibm.com'))

# Get project
project = platform.projects.get(name='Customer Demo Project')



# Get the flow that we were working with
streaming_flow = project.flows.get(name="New streaming flow for fraud detection")


# Python generator generating streaming flow template or learning SDK
generator = PythonGenerator(
    source=streaming_flow,
    destination='/Users/wilsonshamim/Desktop/Code/pythonProjectsOld/IBM/watsonx data integrations/streaming_flow_template.py',
    auth=auth,
    base_api_url=os.getenv('WATSONX_BASE_URL', 'https://api.ca-tor.dai.cloud.ibm.com')
)
generator.save()

