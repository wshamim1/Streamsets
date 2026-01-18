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
# Stage: MySQL Bulk Load
pipelines = sch.pipelines.get_all(offset=0, len=-1, only_published=True,filter_text='pipeline1')

#pipelines = control_hub.pipelines.get(pipeline_id="49a750b4-a67e-489d-9970-e428915b61c3:schwilson")


#pipelines = control_hub.pipelines.get_all(offset=offset, len=length, only_published=True)
length = 50
offset = 0


origins_dico = {}
destinations_dico = {}
print("*-------------------------------*")
for pipeline in pipelines:
    print(f"pipeline_name: {pipeline.name}")
    for i,stage in enumerate(pipeline.stages):
        
        for x in stage.configuration.items():
            print(x)
        print('-----')
        if stage.stage_name.find("Source") > -1 or stage.stage_name.find("destination") > -1:
            if i == 0:
                if hasattr(stage, 'batch_size_in_recs'):
                    print(f"---ORIGIN  BATCHSIZE:{stage.batch_size_in_recs} {stage.instance_name}")
                elif hasattr(stage, 'batch_size'):
                    print(f"---ORIGIN  BATCHSIZE:{stage.batch_size} {stage.instance_name}")
                elif hasattr(stage, 'buffer_size_in_bytes'):
                    print(f"---ORIGIN  BUFFERSIZE:{stage.buffer_size_in_bytes} {stage.instance_name}")
                else:
                    print(f"---ORIGIN  {stage.instance_name}")
                if stage.instance_name[:6] in origins_dico:
                    origins_dico[stage.instance_name[:6]] = origins_dico[stage.instance_name[:6]] + 1
                else:
                    origins_dico.update({stage.instance_name[:6] : 1})
            else:
                print(f"---DESTINATION  {stage.instance_name}")
                if stage.instance_name[:6] in destinations_dico:
                    destinations_dico[stage.instance_name[:6]] = destinations_dico[stage.instance_name[:6]] + 1
                else:
                    destinations_dico.update({stage.instance_name[:6] : 1})
    print("*-------------------------------*")
    if len(pipelines) < length:
        break
    offset += length
print(f"Origins summary count")
for k,v in origins_dico.items():
    print(f"{k} - {v}")
print("-"*100)
print(f"Destinations summary count")
for k,v in destinations_dico.items():
    print(f"{k} - {v}")
print("-"*100)
