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
sch = initialize_control_hub('PLATFORM')


# Get currently active SDC (reported in last 5 minutes)
def get_active_sdc():
    data_collectors = sch.data_collectors.get_all()
    current_time_ms = int(time.time() * 1000)
    five_minutes_ms = 5 * 60 * 1000
    for dc in data_collectors:
        if dc.last_reported_time and (current_time_ms - dc.last_reported_time) <= five_minutes_ms:
            return dc
    return None

sdc = get_active_sdc()

builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sdc.id)


#add stages
dev_raw_data_source = builder.add_stage('Dev Raw Data Source',type='origin')
dev_raw_data_source.set_attributes(
    raw_data='{ "f1": "122", "f2": "xyz","f3": "lmn" }',
    data_format='JSON'

)
trash = builder.add_stage('Trash',type='destination')

#link stages in a pipeline
dev_raw_data_source >> trash

#add enents and connect using >=
pipeline_finisher = builder.add_stage('Pipeline Finisher Executor')
dev_raw_data_source >= pipeline_finisher

#add labels in the pipelines while creatint it.
labels = ["label1","label2/dev"]

pipeline = builder.build(title="pipeline1",labels=labels,
                         description="this is a sample pipeline"
                         )


#add parameters in a pipeline
pipeline.parameters.update({"name1": "value1","name2":'value2'})


#publish the pipeline in control hub
sch.publish_pipeline(pipeline)



