import os
from auth import StreamSetsAuth
from data_collector import DataCollectorManager
from pipelinebuilder_dev_to_trash import PipelineBuilder
from streamsets.sdk import ControlHub



class PipelineManager:
    """
    Manages pipeline retrieval and deletion in StreamSets.
    """
    def __init__(self, control_hub: ControlHub):
        self.control_hub = control_hub
        
    def get_pipeline(self, name: str):
        """Retrieves a pipeline by name."""
        return self.control_hub.pipelines.get(name=name)
    
    def delete_pipeline(self, pipeline):
        """Deletes a pipeline from Control Hub."""
        self.control_hub.delete_pipeline(pipeline)
        print(f"Pipeline '{pipeline}' deleted successfully.")


if __name__ == "__main__":
    # Load environment variables and authenticate
    auth = StreamSetsAuth()
    control_hub = auth.authenticate()
    
    # Retrieve Data Collector instance
    engine_id = os.getenv("ENGINE_ID")
    data_collector_manager = DataCollectorManager(control_hub)
    data_collector = data_collector_manager.get_data_collector(engine_id)
    
    # Retrieve and delete pipeline
    pipeline_manager = PipelineManager(control_hub)
    pipeline = pipeline_manager.get_pipeline(name="test")
    print(pipeline)
    pipeline_manager.delete_pipeline(pipeline)
