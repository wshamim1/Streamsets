

import os
from auth import StreamSetsAuth
from pipelinebuilder_dev_to_trash import PipelineBuilder
from streamsets.sdk import ControlHub


class TransformerManager:
    """
    Handles Transformer instance retrieval.
    """
    def __init__(self, control_hub: ControlHub):
        self.control_hub = control_hub
    
    def get_transformer(self, engine_id: str):
        return self.control_hub.transformers.get(id=engine_id)
