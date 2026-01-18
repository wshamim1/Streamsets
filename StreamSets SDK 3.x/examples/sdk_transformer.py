"""
Example: Creating Transformer pipelines with StreamSets SDK
"""
import os
from streamsets.sdk import ControlHub, Transformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Disable SSL verification if needed (not recommended for production)
Transformer.VERIFY_SSL_CERTIFICATES = False

# Authenticate using environment variables
control_hub = ControlHub(
    sch_url=os.getenv('SCH_URL'),
    credential_id=os.getenv('CRED_ID'),
    token=os.getenv('CRED_TOKEN')
)

print(f"Connected to Control Hub: {control_hub}")

tr = Transformer('https://127.0.0.1:19633', control_hub=control_hub)
id = tr.id
print(id)

print(control_hub.transformers.get(id=id))

pipeline_builder = control_hub.get_pipeline_builder(control_hub.transformers.get(url='https://transformer.cluster:19633'))
print(pipeline_builder)



dev_random = pipeline_builder.add_stage('Dev Random')

trash_1 = pipeline_builder.add_stage('Trash')
#change the name of the stage
trash_1.label="Top Trash"

# or use
dev_random >> trash_1

print("--=--==========")

print("--=--==========")
labels = ['test/dev', 'test']
#
pipeline = pipeline_builder.build(title='pipeline1',description='my description',labels=['label2','label2/dev'])
pipeline.parameters={'NAME':'VALUE'}


emr_dict = {
        "clusterConfig.clusterType":"EMR",
        "transformerEmrConnection.awsConfig.credentialMode":"WITH_IAM_ROLES",
        "transformerEmrConnection.s3StagingUri":"s3://streamsets-customer-success-internal/wilsonshamim",
        "transformerEmrConnection.clusterId":"j-XRH3Z7MCL2JY",
        "clusterConfig.callbackUrl":"https://transformer.cluster:19630/",
        "sparkConfigs":[{'key': 'spark.driver.memory', 'value': '5G'}, {'key': 'spark.driver.cores', 'value': '1'},
                                                   {'key': 'spark.executor.memory', 'value': '2G'}, {'key': 'spark.executor.cores', 'value': '1'},
                                                   {'key': 'spark.dynamicAllocation.enabled', 'value': 'true'},
                                                   {'key': 'spark.shuffle.service.enabled', 'value': 'true'},
                                                   {'key': 'spark.dynamicAllocation.minExecutors', 'value': '1'}]
      }

dbx_dict =  {
        "clusterConfig.clusterType":"DATABRICKS",
        "databricksConfig.baseUrl": os.getenv('DATABRICKS_URL', 'https://your-databricks-url.cloud.databricks.com/'),
        "databricksConfig.credentialType":"TOKEN",
        "databricksConfig.token": os.getenv('DATABRICKS_TOKEN', 'your-databricks-token'),
        "databricksConfig.provisionNewCluster":False,
        "databricksConfig.clusterId": os.getenv('DATABRICKS_CLUSTER_ID', 'your-cluster-id'),
        "clusterConfig.callbackUrl":"https://transformer.cluster:19630/",
        "sparkConfigs":[{'key': 'spark.driver.memory', 'value': '5G'}, {'key': 'spark.driver.cores', 'value': '1'},
                                                   {'key': 'spark.executor.memory', 'value': '2G'}, {'key': 'spark.executor.cores', 'value': '1'},
                                                   {'key': 'spark.dynamicAllocation.enabled', 'value': 'true'},
                                                   {'key': 'spark.shuffle.service.enabled', 'value': 'true'},
                                                   {'key': 'spark.dynamicAllocation.minExecutors', 'value': '1'}]
      }

for key in emr_dict:
    pipeline.configuration[key]=emr_dict[key]

for key in dbx_dict:
    pipeline.configuration[key]=dbx_dict[key]




print(pipeline.configuration.get("sparkConfigs"))

print(pipeline.configuration.get("clusterConfig.sparkMasterUrl"))
print(pipeline.configuration.get("clusterConfig.clusterType"))


control_hub.publish_pipeline(pipeline)

job_builder = control_hub.get_job_builder()


# create job . also can pass runtime parameter.
job1 = job_builder.build(job_name='My Job1',pipeline=pipeline,tags=['tag1'],job_template=True,
                         runtime_parameters={"schema_name": ""})
control_hub.add_job(job1)





