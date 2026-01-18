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
project = platform.projects.get(name=os.getenv('WATSONX_PROJECT_NAME', 'Customer Demo Project'))




#print(platform.create_project(name="My New Project", description="This is my new project").name)
print(auth.get_token())
print(project.name)

print(platform.projects.get_all())

env = project.environments.get_all()
print(env)

#creating Streamsets Flow with Row Generator and Trash stages
flow_name_prefix = "RowGen"
random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))  # Generate a 5-char alphanumeric suffix
SS_flow_name = f"{flow_name_prefix}_{random_suffix}"
SS_Job_name = f"SS_Job_{random_suffix}"
# For the first flow
flow = project.create_flow(name=SS_flow_name,environment=None, flow_type="streamsets")
# Stages
row_generator = flow.add_stage(label="Dev Raw Data Source")
trash = flow.add_stage(label= "Trash")
# Graph
link_2 = row_generator.connect_output_to(trash)
project.update_flow(flow)

#creating Streamsets Job
ss_job = project.create_job(flow=flow, name=SS_Job_name, description='...')

print(ss_job) 

# For the second flow
random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))  # Generate a new 5-char alphanumeric suffix
DS_flow_name  = f"{flow_name_prefix}_{random_suffix}"
DS_Job_name = f"DS_Job_{random_suffix}"
flow = project.create_flow( name=DS_flow_name,environment=None,flow_type="datastage")

# Stages
row_generator = flow.add_stage("Row Generator", "Row_Generator")
row_generator.configuration.runtime_column_propagation = False

peek = flow.add_stage("Peek", "Peek")
peek.configuration.runtime_column_propagation = False

# Graph
link_1 = row_generator.connect_output_to(peek)
link_1.name = "Link_1"

row_generator_schema = link_1.create_schema()
row_generator_schema.add_field("VARCHAR", "COLUMN_1").length(100)

project.update_flow(flow)

ds_job = project.create_job(flow=flow, name=DS_Job_name,description='...',)

print(ds_job)


#Start Streamsets Job
ss_job_run = ss_job.start(name='SS Job Run', description='...')
print(ss_job_run)

ds_job_run = ds_job.start(name='DS Job Run', description='...')
print(ds_job_run)

exit()

# env1 = project.create_environment(
#     name='Sample',
#     # Optional parameters - see API Reference for more optional parameters
#     description='Basic env.',
#     stage_libs=[
#         'streamsets-datacollector-basic-lib',
#         'streamsets-datacollector-dataformats-lib',
#         'streamsets-datacollector-dev-lib'
#     ],
#     cpus_to_allocate=2,
# )
# env = project.environments.get(environment_id='69dcce3b-ce9e-4d2e-b413-6e50361796f8')
# project.delete_environment(env)
env = project.environments
print(env)


print(platform.available_engine_versions)

print(project.engines)


job = project.jobs
print(job)


flow = project.flows

print(flow)
