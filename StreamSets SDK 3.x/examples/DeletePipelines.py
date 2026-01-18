
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