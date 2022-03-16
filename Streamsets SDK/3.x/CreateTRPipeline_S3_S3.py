from streamsets.sdk import ControlHub, Transformer
Transformer.VERIFY_SSL_CERTIFICATES = False

control_hub_url = "https://***.streamsetscloud.com"
control_hub_user="serviceuser@org"
control_hub_pw="*****"
engine_id='704fd887-0bc0-11ec-b7c3-8d2659d10743'
engine_type='data_collector'


#Create Control hub Objects
control_hub = ControlHub(
            control_hub_url,username=control_hub_user, password=control_hub_pw,
        )

#create data_collector object
transformer = control_hub.transformers.get(id=engine_id)
print(transformer)

#create pipeline builder
builder = control_hub.get_pipeline_builder(transformer)

#add stages

src_s3 = builder.add_stage('Amazon S3',type='origin')
src_s3.set_attributes(

    stage_name='test',
    authentication_method="WITH_IAM_ROLES",
    bucket="S3_BUCKET",
    object_name_pattern="*",
    data_format="JSON"

)

src_s3.library='streamsets-spark-aws-no-dependency-lib'
dest_s3 = builder.add_stage('Amazon S3',type='destination')
dest_s3.set_attributes(
    authentication_method="WITH_IAM_ROLES",
    bucket="S3_BUCKET",
    data_format="JSON",
    write_mode='APPEND'
)
dest_s3.library='streamsets-spark-aws-no-dependency-lib'

#link stages in a pipeline
src_s3 >> dest_s3


#add labels in the pipelines while creatint it.
labels = ["label1","label2/dev"]

pipeline = builder.build(title="pipeline1",labels=labels,
                         description="this is a sample pipeline")
#add parameters in a pipeline
pipeline.parameters.update({"name1": "value1","name2":'value2'})


emr_dict = {
 "clusterConfig.clusterType":"EMR",
 "transformerEmrConnection.awsConfig.credentialMode":"WITH_IAM_ROLES",
 "transformerEmrConnection.s3StagingUri":"s3:///wilsonshamim",
 "transformerEmrConnection.clusterId":"j-test",
 "clusterConfig.callbackUrl":"https://transformer.cluster:19630/",
 "sparkConfigs":[{'key': 'spark.driver.memory', 'value': '5G'}, {'key': 'spark.driver.cores', 'value': '1'},
 {'key': 'spark.executor.memory', 'value': '2G'}, {'key': 'spark.executor.cores', 'value': '1'},
 {'key': 'spark.dynamicAllocation.enabled', 'value': 'true'},
 {'key': 'spark.shuffle.service.enabled', 'value': 'true'},
 {'key': 'spark.dynamicAllocation.minExecutors', 'value': '1'}]
      }

for key in emr_dict:
    pipeline.configuration[key]=emr_dict[key]


#publish the pipeline in control hub
control_hub.publish_pipeline(pipeline)


