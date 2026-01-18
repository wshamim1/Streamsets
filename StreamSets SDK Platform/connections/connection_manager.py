

"""
Connection Manager for StreamSets Platform SDK
Manages connections in StreamSets Control Hub
"""
from streamsets.sdk import ControlHub
from ..utils.auth import get_control_hub


class ConnectionManager:
    """
    Manages connections in StreamSets Control Hub.
    """
    def __init__(self, control_hub: ControlHub):
        self.control_hub = control_hub
    
    def get_connection_by_id(self, connection_id: str):
        """Retrieves a connection by its ID."""
        return self.control_hub.connections.get(id=connection_id)
    
    def get_connection_by_name(self, name: str):
        """Retrieves a connection by its name."""
        return self.control_hub.connections.get(name=name)
    
    def get_all_connections(self):
        """Retrieves all available connections."""
        return self.control_hub.connections.get_all()
    
    def create_connection(self, name: str, connection_type: str, description: str, attributes: dict):
        """Creates a new connection."""
        new_connection = self.control_hub.connections.create(
            name=name, connection_type=connection_type, description=description, attributes=attributes
        )
        print(f"Connection '{name}' created successfully.")
        return new_connection
    
    def delete_connection(self, connection_id: str):
        """Deletes a connection by its ID."""
        connection = self.get_connection_by_id(connection_id)
        self.control_hub.delete_connection(connection)
        print(f"Connection '{connection.name}' deleted successfully.")
    
    def print_connection_details(self, connections):
        """Prints details of all retrieved connections."""
        for connection in connections:
            print("Connection Name: " + connection.name)
            print("Connection ID: " + connection.id)
            print("Connection Type: " + connection.connection_type)
            print("----------------------------------------------------------")


if __name__ == "__main__":
    # Authenticate with StreamSets
    control_hub = get_control_hub()
    connection_manager = ConnectionManager(control_hub)
    
    # Retrieve and print all connections
    all_connections = connection_manager.get_all_connections()
    connection_manager.print_connection_details(all_connections)
    
    # Example connection operations
    example_connection_id = "example-connection-id"
    connection_manager.delete_connection(example_connection_id)
