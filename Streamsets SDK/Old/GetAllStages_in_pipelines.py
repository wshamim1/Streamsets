from streamsets.sdk import ControlHub, Transformer
Transformer.VERIFY_SSL_CERTIFICATES = False

control_hub_url = "https://***.streamsetscloud.com"
control_hub_user="serviceuser@org"
control_hub_pw="*****"
engine_id='704fd887-0bc0-11ec-b7c3-8d2659d10743'
engine_type='transformer'


#Create Control hub Objects
control_hub = ControlHub(
            control_hub_url,username=control_hub_user, password=control_hub_pw,
        )

#create data_collector object
transformer = control_hub.transformers.get(id=engine_id)
print(transformer)

#create pipeline builder
builder = control_hub.get_pipeline_builder(transformer)

pipelinename = control_hub.pipelines.get(name='pipeline1')
for stage in pipelinename.stages:
    print(stage)
    print(f"----------------------------------------------------------")
    print(f"----> {stage.stage_name}")
    print(f"----------------------------------------------------------")
    for p in dir(stage):

        if p.startswith("_"):
            continue
        try:
            v = eval(f"stage.{p}")
            print("property:{0}  value={1}".format(p, v))
        except:
            pass

