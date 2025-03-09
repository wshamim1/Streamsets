from streamsets.sdk import ControlHub, DataCollector,Transformer
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
pipelines = control_hub.pipelines.get(
    pipeline_id='08eb05b7-689f-4c57-af8c-ea96107c738c:schwilson')
print(pipelines)

# use duplicate pipeline method

p = control_hub.duplicate_pipeline(pipelines,name='xyz',number_of_copies=1,
                                   description='test')
control_hub.publish_pipeline(p)