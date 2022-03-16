from streamsets.sdk import ControlHub, DataCollector
DataCollector.VERIFY_SSL_CERTIFICATES = False

control_hub_url = "https://***.streamsetscloud.com"
control_hub_user="serviceuser@org"
control_hub_pw="*****"
engine_id='704fd887-0bc0-11ec-b7c3-8d2659d10743'
engine_type='data_collector'


#Create Control hub Objects
control_hub = ControlHub(
            control_hub_url,username=control_hub_user,
            password=control_hub_pw,
        )

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
    "jdbc_connection_string": "JDBC_STRING",
    "use_credentials": True,
    "username": "USER",
    "password": "PW",
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
