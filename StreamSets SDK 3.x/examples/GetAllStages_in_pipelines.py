import os
from streamsets.sdk import ControlHub, Transformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Disable SSL verification if needed (not recommended for production)
Transformer.VERIFY_SSL_CERTIFICATES = False

# Configuration from environment variables
control_hub_url = os.getenv('SCH_URL', 'https://your-control-hub.streamsetscloud.com')
control_hub_user = os.getenv('SCH_USER', 'serviceuser@org')
control_hub_pw = os.getenv('SCH_PASSWORD', 'your-password')
engine_id = os.getenv('ENGINE_ID', 'your-engine-id')
engine_type = 'data_collector'


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

