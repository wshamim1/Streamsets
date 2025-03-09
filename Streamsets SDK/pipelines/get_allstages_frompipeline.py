
import os
from auth import StreamSetsAuth
from transformer import TransformerManager
from pipelinebuilder_dev_to_trash import PipelineBuilder
from streamsets.sdk import ControlHub


class PipelineInspector:
    """
    Retrieves and inspects pipeline stages.
    """
    def __init__(self, control_hub: ControlHub):
        self.control_hub = control_hub
    
    def get_pipeline(self, name: str):
        """Retrieves a pipeline by name."""
        return self.control_hub.pipelines.get(name=name)
    
    def inspect_pipeline(self, pipeline):
        """Prints details of each stage in the pipeline."""
        for stage in pipeline.stages:
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


if __name__ == "__main__":
    # Load environment variables and authenticate
    auth = StreamSetsAuth()
    control_hub = auth.authenticate()
    
    # Retrieve Transformer instance
    engine_id = os.getenv("ENGINE_ID")
    transformer_manager = TransformerManager(control_hub)
    transformer = transformer_manager.get_transformer(engine_id)
    print(transformer)
    
    # Inspect pipeline stages
    pipeline_inspector = PipelineInspector(control_hub)
    pipeline = pipeline_inspector.get_pipeline(name="pipeline1")
    pipeline_inspector.inspect_pipeline(pipeline)
