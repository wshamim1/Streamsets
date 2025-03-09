from streamsets.sdk import ControlHub, DataCollector
DataCollector.VERIFY_SSL_CERTIFICATES = False

control_hub_url = "https://***.streamsetscloud.com"
control_hub_user="serviceuser@org"
control_hub_pw="*****"
engine_id='704fd887-0bc0-11ec-b7c3-8d2659d10743'
engine_type='data_collector'


#Create Control hub Objects
control_hub = ControlHub(
            control_hub_url,username=control_hub_user, password=control_hub_pw,)

#create data_collector object
data_collector = control_hub.data_collectors.get(id=engine_id)
print(data_collector)

#create pipeline builder
builder = control_hub.get_pipeline_builder(data_collector)

# Get a single pipeline by passing either pipeline_id or name or commit_id
pipelines = control_hub.pipelines.get(name='test')
print(pipelines)

# Invoke delete_pipeline method to delete the pipeline
control_hub.delete_pipeline(pipelines)