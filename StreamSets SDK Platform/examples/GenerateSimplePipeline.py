

"""
Example: Generate simple pipeline code dynamically
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Pipeline configuration
origin = 'S3'
destination = 'Trash'


def generate_pipeline_code(origin=origin, destination=destination):
    """
    Generate Python code for a simple pipeline.
    
    Args:
        origin: Source stage name
        destination: Destination stage name
    """
    print(f'Generating pipeline code: {origin} -> {destination}')
    
    # Get credentials from environment
    credential_id = os.getenv('CRED_ID', 'your-credential-id')
    token = os.getenv('CRED_TOKEN', 'your-token')
    engine_id = os.getenv('ENGINE_ID', 'your-engine-id')
    
    # Generate code
    code = f"""from streamsets.sdk import ControlHub
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Authenticate
control_hub = ControlHub(
    credential_id=os.getenv('CRED_ID'),
    token=os.getenv('CRED_TOKEN')
)

# Get pipeline builder
builder = control_hub.get_pipeline_builder(
    engine_type='data_collector',
    engine_id=os.getenv('ENGINE_ID')
)

# Add stages
{origin} = builder.add_stage('{origin}')
{destination} = builder.add_stage('{destination}')

# Connect stages
{origin} >> {destination}

# Build and publish pipeline
pipeline = builder.build('Pipeline 1')
control_hub.publish_pipeline(pipeline, commit_message='First Commit')
"""
    
    # Write to file
    filename = f"{origin}_{destination}.py"
    with open(filename, "w") as f:
        f.write(code)
    
    print(f"Generated: {filename}")


if __name__ == "__main__":
    generate_pipeline_code(origin=origin, destination=destination)
