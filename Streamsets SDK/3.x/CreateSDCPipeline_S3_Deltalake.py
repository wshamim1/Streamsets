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
src_s3 = builder.add_stage('Amazon S3',type='origin')
src_s3.set_attributes(
    authentication_method="WITH_IAM_ROLES",
    bucket="S3_BUCKET",
    common_prefix="PREFIX",
    data_format="JSON",
    prefix_pattern="*"

)
databricks_deltalake = builder.add_stage('Databricks Delta Lake',
                                         type='destination')
databricks_deltalake.set_attributes(
    description= "Load bulk data into Delta table",
    jdbc_url= "JDBC URL",
    token= "TOKEN",
    table_name= "test_table",
    enable_data_drift= True,
    auto_create_table= True,
    staging_location= "AWS_S3",
    purge_stage_file_after_ingesting= True,
    bucket= "S3_BUCKET/S3_PATH",
    use_instance_profile= True,
    connection_pool_size= 10,
    s3_uploading_threads= 10,
    replace_newlines=True,
    new_line_replacement_character= " ",
)

dest_s3 = builder.add_stage('Amazon S3',type='destination')
dest_s3.set_attributes(
    authentication_method="WITH_IAM_ROLES",
    bucket="S3_BUCKET",
    common_prefix="PREFIX",
    partition_prefix="",
    data_format="JSON",
    object_name_suffix="jsonl",
    compress_with_gzip=True
)

#link stages in a pipeline
src_s3 >> [databricks_deltalake,dest_s3]



#add labels in the pipelines while creatint it.
labels = ["label1","label2/dev"]

pipeline = builder.build(title="pipeline1",labels=labels,
                         description="this is a sample pipeline")
#add parameters in a pipeline
pipeline.parameters.update({"name1": "value1","name2":'value2'})

#publish the pipeline in control hub
control_hub.publish_pipeline(pipeline)
