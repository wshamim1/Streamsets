"""
Deployment Manager for StreamSets Platform SDK
Manages self-managed deployments in StreamSets Control Hub
"""
import argparse
from streamsets.sdk import ControlHub
from ..utils.auth import get_control_hub


class DeploymentManager:
    """
    Manages self-managed deployments in StreamSets Control Hub.
    """
    def __init__(self, control_hub: ControlHub):
        self.control_hub = control_hub
    
    def get_deployment_by_id(self, deployment_id: str):
        """Retrieves a deployment by its ID."""
        return self.control_hub.deployments.get(id=deployment_id)
    
    def get_deployment_by_name(self, name: str):
        """Retrieves a deployment by its name."""
        return self.control_hub.deployments.get(name=name)
    
    def get_all_deployments(self):
        """Retrieves all available deployments."""
        return self.control_hub.deployments.get_all()
    
    def create_deployment(self, name: str, engine_type: str, configuration: dict):
        """Creates a new self-managed deployment."""
        deployment = self.control_hub.deployments.create(name=name, engine_type=engine_type, configuration=configuration)
        print(f"Deployment '{deployment.name}' created successfully.")
        return deployment
    
    def delete_deployment(self, deployment_id: str):
        """Deletes a deployment by its ID."""
        deployment = self.get_deployment_by_id(deployment_id)
        if deployment:
            self.control_hub.deployments.delete(deployment)
            print(f"Deployment '{deployment.name}' deleted successfully.")
        else:
            print(f"Deployment with ID '{deployment_id}' not found.")
    
    def print_deployment_details(self, deployments):
        """Prints details of all retrieved deployments."""
        if deployments:
            for deployment in deployments:
                print("Deployment Name: " + deployment.name)
                print("Deployment ID: " + deployment.id)
                print("Engine Type: " + deployment.engine_type)
                print("----------------------------------------------------------")
        else:
            print("No deployments found.")

if __name__ == "__main__":
    # Authenticate with StreamSets
    control_hub = get_control_hub()
    deployment_manager = DeploymentManager(control_hub)
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="StreamSets Deployment Manager")
    parser.add_argument("action", choices=["list", "create", "get_by_id", "get_by_name", "delete"], help="Action to perform")
    parser.add_argument("--deployment_id", type=str, help="Deployment ID (required for get_by_id and delete)")
    parser.add_argument("--name", type=str, help="Deployment Name (required for create and get_by_name)")
    parser.add_argument("--engine_type", type=str, help="Engine Type (required for create)")
    parser.add_argument("--configuration", type=str, help="Deployment configuration in JSON format (required for create)")
    
    args = parser.parse_args()
    
    if args.action == "list":
        all_deployments = deployment_manager.get_all_deployments()
        deployment_manager.print_deployment_details(all_deployments)
    elif args.action == "create" and args.name and args.engine_type and args.configuration:
        import json
        configuration = json.loads(args.configuration)
        deployment_manager.create_deployment(args.name, args.engine_type, configuration)
    elif args.action == "get_by_id" and args.deployment_id:
        deployment = deployment_manager.get_deployment_by_id(args.deployment_id)
        deployment_manager.print_deployment_details([deployment] if deployment else [])
    elif args.action == "get_by_name" and args.name:
        deployment = deployment_manager.get_deployment_by_name(args.name)
        deployment_manager.print_deployment_details([deployment] if deployment else [])
    elif args.action == "delete" and args.deployment_id:
        deployment_manager.delete_deployment(args.deployment_id)
    else:
        print("Invalid arguments. Use --help for usage details.")
