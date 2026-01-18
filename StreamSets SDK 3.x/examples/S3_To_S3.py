
engine_id='704fd887-0bc0-11ec-b7c3-8d2659d10743'
engine_type='data_collector'


from streamsets.sdk import ControlHub, DataCollector
DataCollector.VERIFY_SSL_CERTIFICATES = False
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import json
import time
load_dotenv()


# Assisted by watsonx Code Assistant 
import os


def initialize_control_hub(type):
    """
    Initializes and returns a ControlHub object based on environment variables.
    Supports both platform-based and legacy Control Hub 3.x setups.
    """
    # PLATFORM-based credentials (token-based auth)
    if type == 'PLATFORM' :
        CRED_ID = os.getenv('CRED_ID')
        CRED_TOKEN = os.getenv('CRED_TOKEN')
        SCH_URL = os.getenv('SCH_URL')
        if not all([CRED_ID, CRED_TOKEN, SCH_URL]):
            raise EnvironmentError("Missing one or more required PLATFORM environment variables (CRED_ID, CRED_TOKEN, SCH_URL).")
        return ControlHub(sch_url=SCH_URL, credential_id=CRED_ID, token=CRED_TOKEN)

    # Control Hub 3.x username/password auth
    else:
        control_hub_url = os.getenv('control_hub_url')
        control_hub_user = os.getenv('control_hub_user')
        control_hub_pw = os.getenv('control_hub_pw')
        return ControlHub(sch_url=control_hub_url, username=control_hub_user, password=control_hub_pw)


# === USAGE EXAMPLE ===
control_hub = initialize_control_hub('PLATFORM')

#create data_collector object
data_collector = control_hub.data_collectors.get(id=engine_id)
print(data_collector)

#create pipeline builder
builder = control_hub.get_pipeline_builder(data_collector)

#add stages
src_s3 = builder.add_stage('Amazon S3',type='origin')
src_s3.set_attributes(
    authentication_method="WITH_IAM_ROLES",
    bucket="S3_BUCKET",
    common_prefix="PREFIX",
    data_format="JSON",
    prefix_pattern="*"

)

dest_s3 = builder.add_stage('Amazon S3',type='destination')
dest_s3.set_attributes(
    authentication_method="WITH_IAM_ROLES",
    bucket="${bucketname}",
    common_prefix="PREFIX",
    partition_prefix="",
    data_format="JSON",
    object_name_suffix="jsonl",
    compress_with_gzip=True
)

#link stages in a pipeline
src_s3 >> dest_s3



#add labels in the pipelines while creatint it.
labels = ["label1","label2/dev"]

pipeline = builder.build(title="pipeline1",labels=labels,
                         description="this is a sample pipeline")
#add parameters in a pipeline
pipeline.parameters.update({"bucketname": "value1","name2":'value2'})

#publish the pipeline in control hub
control_hub.publish_pipeline(pipeline)
