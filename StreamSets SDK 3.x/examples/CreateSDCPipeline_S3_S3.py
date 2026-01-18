from streamsets.sdk import ControlHub, DataCollector
DataCollector.VERIFY_SSL_CERTIFICATES = False

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
