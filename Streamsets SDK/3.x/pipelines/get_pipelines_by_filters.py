import os
from auth import StreamSetsAuth
from data_collector import DataCollectorManager
from pipelinebuilder_dev_to_trash import PipelineBuilder
from streamsets.sdk import ControlHub



class PipelineManager:
    """
    Retrieves pipelines using various parameters.
    """
    def __init__(self, control_hub: ControlHub):
        self.control_hub = control_hub
    
    def get_pipeline_by_id(self, pipeline_id: str):
        """Retrieves a pipeline by ID."""
        return self.control_hub.pipelines.get(pipeline_id=pipeline_id)
    
    def get_pipeline_by_name(self, name: str):
        """Retrieves a pipeline by name."""
        return self.control_hub.pipelines.get(name=name)
    
    def get_pipeline_by_commit_id(self, commit_id: str):
        """Retrieves a pipeline by commit ID."""
        return self.control_hub.pipelines.get(commit_id=commit_id)
    
    def get_all_pipelines(self):
        """Retrieves all pipelines."""
        return self.control_hub.pipelines.get_all()
    
    def print_pipeline_details(self, pipelines):
        """Prints details of each retrieved pipeline."""
        for pipeline in pipelines:
            print("Pipeline Name: " + pipeline.name)
            print("Pipeline Commit ID: " + pipeline.commit_id)
            print("Pipeline Version: " + str(pipeline.version))
            print("Pipeline ID: " + pipeline.pipeline_id)
            print("----------------------------------------------------------")


if __name__ == "__main__":
    # Load environment variables and authenticate
    auth = StreamSetsAuth()
    control_hub = auth.authenticate()
    
    # Retrieve Data Collector instance
    engine_id = os.getenv("ENGINE_ID")
    data_collector_manager = DataCollectorManager(control_hub)
    data_collector = data_collector_manager.get_data_collector(engine_id)
    print(data_collector)
    
    # Retrieve pipelines
    pipeline_manager = PipelineManager(control_hub)
    
    pipeline_by_id = pipeline_manager.get_pipeline_by_id("338b384e-732b-4597-b378-cdd5a9b672ba:schwilson")
    print(pipeline_by_id)
    
    pipeline_by_name = pipeline_manager.get_pipeline_by_name("test")
    print(pipeline_by_name)
    
    pipeline_by_commit_id = pipeline_manager.get_pipeline_by_commit_id("e372a299-174d-4755-89b2-6ba19b0d9380:schwilson")
    print(pipeline_by_commit_id)
    
    all_pipelines = pipeline_manager.get_all_pipelines()
    print(all_pipelines)
    pipeline_manager.print_pipeline_details(all_pipelines)
