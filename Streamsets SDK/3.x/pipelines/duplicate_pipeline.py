import os
from auth import StreamSetsAuth
from data_collector import DataCollectorManager
from pipelinebuilder_dev_to_trash import PipelineBuilder
from streamsets.sdk import ControlHub



class DataCollectorManager:
    """
    Handles Data Collector instance retrieval.
    """
    def __init__(self, control_hub: ControlHub):
        self.control_hub = control_hub
    
    def get_data_collector(self, engine_id: str):
        return self.control_hub.data_collectors.get(id=engine_id)



class PipelineManager:
    """
    Manages pipeline retrieval, duplication, and publishing in StreamSets.
    """
    def __init__(self, control_hub: ControlHub):
        self.control_hub = control_hub
        
    def get_pipeline(self, pipeline_id: str):
        """Retrieves a pipeline by ID."""
        return self.control_hub.pipelines.get(pipeline_id=pipeline_id)
    
    def duplicate_pipeline(self, pipeline, name: str, number_of_copies: int, description: str):
        """Duplicates a pipeline with a new name and description."""
        return self.control_hub.duplicate_pipeline(pipeline, name=name, number_of_copies=number_of_copies, description=description)
    
    def publish_pipeline(self, pipeline):
        """Publishes the given pipeline to Control Hub."""
        self.control_hub.publish_pipeline(pipeline)
        print(f"Pipeline '{pipeline.title}' published successfully.")


if __name__ == "__main__":
    # Load environment variables and authenticate
    auth = StreamSetsAuth()
    control_hub = auth.authenticate()
    
    # Retrieve Data Collector instance
    engine_id = os.getenv("ENGINE_ID")
    data_collector_manager = DataCollectorManager(control_hub)
    data_collector = data_collector_manager.get_data_collector(engine_id)
    
    # Retrieve, duplicate, and publish pipeline
    pipeline_manager = PipelineManager(control_hub)
    pipeline = pipeline_manager.get_pipeline(pipeline_id="08eb05b7-689f-4c57-af8c-ea96107c738c:schwilson")
    print(pipeline)
    
    duplicated_pipeline = pipeline_manager.duplicate_pipeline(pipeline, name="xyz", number_of_copies=1, description="test")
    pipeline_manager.publish_pipeline(duplicated_pipeline)
