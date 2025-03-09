import os
from auth import StreamSetsAuth
from data_collector import DataCollectorManager
from pipelinebuilder_dev_to_trash import PipelineBuilder
from streamsets.sdk import ControlHub




class PipelineManager:
    """
    Retrieves all pipelines with a specific label.
    """
    def __init__(self, control_hub: ControlHub):
        self.control_hub = control_hub
    
    def get_all_pipelines(self, label: str):
        """Retrieves all pipelines with the specified label."""
        return self.control_hub.pipelines.get_all(label=label)
    
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
    
    # Retrieve and print all pipelines with a specific label
    pipeline_manager = PipelineManager(control_hub)
    all_pipelines = pipeline_manager.get_all_pipelines(label="label2/dev")
    print(all_pipelines)
    pipeline_manager.print_pipeline_details(all_pipelines)
