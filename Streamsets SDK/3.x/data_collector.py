from streamsets.sdk import ControlHub

class DataCollectorManager:
    """
    Handles Data Collector instance retrieval.
    """
    def __init__(self, control_hub: ControlHub):
        self.control_hub = control_hub
    
    def get_data_collector(self, engine_id: str):
        return self.control_hub.data_collectors.get(id=engine_id)
