
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
jdbc_multitable_consumer = builder.add_stage("JDBC Multitable Consumer"
                                             ,type='origin')
jdbc_multitable_consumer_params = {
    "description": "Bulk load",
    "jdbc_connection_string": os.getenv('JDBC_CONNECTION_STRING', 'jdbc:mysql://host:port/database'),
    "use_credentials": True,
    "username": os.getenv('DB_USERNAME', 'your-username'),
    "password": os.getenv('DB_PASSWORD', 'your-password'),
    "number_of_threads": 5,
    "per_batch_strategy": "PROCESS_ALL_AVAILABLE_ROWS_FROM_TABLE",
    "maximum_pool_size": 5,
    "max_batch_size_in_records": 10000,
    "fetch_size": 10000,
    "additional_jdbc_configuration_properties": [
        {"key": "useCursorFetch", "value": "true"}
    ],
}
jdbc_multitable_consumer.set_attributes(**jdbc_multitable_consumer_params)

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

trash = builder.add_stage('Trash',type='destination')

stream_selector = builder.add_stage("Stream Selector")

#first link the staged then add stream selector condition

jdbc_multitable_consumer >> stream_selector >> dest_s3
stream_selector >> trash

stream_selector.condition = [dict(outputLane=stream_selector.output_lanes[0],
                            predicate='${record:value("/test") == "True"}'),
                             dict(outputLane=stream_selector.output_lanes[1],
                            predicate='default')]


#add labels in the pipelines while creatint it.
labels = ["label1","label2/dev"]

pipeline = builder.build(title="pipeline1",labels=labels,
                         description="this is a sample pipeline")
#add parameters in a pipeline
pipeline.parameters.update({"bucketname": "value1","name2":'value2'})

#publish the pipeline in control hub
control_hub.publish_pipeline(pipeline)
