import os
from auth import StreamSetsAuth
from data_collector import DataCollectorManager
from pipelinebuilder_dev_to_trash import PipelineBuilder
from streamsets.sdk import ControlHub



class PipelineBuilder:
    """
    Manages pipeline creation and publishing in StreamSets.
    """
    def __init__(self, control_hub: ControlHub, data_collector):
        self.control_hub = control_hub
        self.data_collector = data_collector
        
    def create_pipeline(self, title: str, description: str, labels: list, parameters: dict):
        """Creates a pipeline with given details."""
        builder = self.control_hub.get_pipeline_builder(self.data_collector)
        
        # Add stages
        src_s3 = builder.add_stage('Amazon S3', type='origin')
        src_s3.set_attributes(
            authentication_method="WITH_IAM_ROLES",
            bucket="S3_BUCKET",
            common_prefix="PREFIX",
            data_format="JSON",
            prefix_pattern="*"
        )
        
        dest_s3 = builder.add_stage('Amazon S3', type='destination')
        dest_s3.set_attributes(
            authentication_method="WITH_IAM_ROLES",
            bucket="${bucketname}",
            common_prefix="PREFIX",
            partition_prefix="",
            data_format="JSON",
            object_name_suffix="jsonl",
            compress_with_gzip=True
        )
        
        # Link stages
        src_s3 >> dest_s3
        
        # Build pipeline
        pipeline = builder.build(title=title, labels=labels, description=description)
        
        # Add parameters
        pipeline.parameters.update(parameters)
        
        return pipeline
    
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
    
    # Create and publish pipeline
    pipeline_manager = PipelineBuilder(control_hub, data_collector)
    pipeline = pipeline_manager.create_pipeline(
        title="pipeline1", 
        description="This is a sample pipeline", 
        labels=["label1", "label2/dev"],
        parameters={"bucketname": "value1", "name2": "value2"}
    )
    
    pipeline_manager.publish_pipeline(pipeline)
