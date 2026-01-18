"""
ACL Manager for StreamSets Platform SDK
Manages Access Control Lists (ACLs) in StreamSets Control Hub
"""
import argparse
from streamsets.sdk import ControlHub
from ..utils.auth import get_control_hub


class ACLManager:
    """
    Manages Access Control Lists (ACLs) in StreamSets Control Hub.
    """
    def __init__(self, control_hub: ControlHub):
        self.control_hub = control_hub
    
    def get_acl(self, resource_id: str):
        """Retrieves the ACL for a given resource ID."""
        return self.control_hub.acls.get(id=resource_id)
    
    def update_acl(self, resource_id: str, acl_updates: dict):
        """Updates the ACL for a given resource ID."""
        acl = self.get_acl(resource_id)
        if acl:
            for key, value in acl_updates.items():
                setattr(acl, key, value)
            acl.save()
            print(f"ACL for resource '{resource_id}' updated successfully.")
        else:
            print(f"ACL for resource ID '{resource_id}' not found.")
    
    def delete_acl(self, resource_id: str):
        """Deletes the ACL for a given resource ID."""
        acl = self.get_acl(resource_id)
        if acl:
            self.control_hub.acls.delete(acl)
            print(f"ACL for resource '{resource_id}' deleted successfully.")
        else:
            print(f"ACL for resource ID '{resource_id}' not found.")
    
    def print_acl_details(self, acl):
        """Prints details of an ACL."""
        if acl:
            print(f"Resource ID: {acl.id}")
            print(f"Permissions: {acl.permissions}")
            print("----------------------------------------------------------")
        else:
            print("No ACL found.")

if __name__ == "__main__":
    # Authenticate with StreamSets
    control_hub = get_control_hub()
    acl_manager = ACLManager(control_hub)
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="StreamSets ACL Manager")
    parser.add_argument("action", choices=["get", "update", "delete"], help="Action to perform")
    parser.add_argument("--resource_id", type=str, required=True, help="Resource ID for the ACL")
    parser.add_argument("--acl_updates", type=str, help="ACL updates in JSON format (required for update)")
    
    args = parser.parse_args()
    
    if args.action == "get":
        acl = acl_manager.get_acl(args.resource_id)
        acl_manager.print_acl_details(acl)
    elif args.action == "update" and args.acl_updates:
        import json
        acl_updates = json.loads(args.acl_updates)
        acl_manager.update_acl(args.resource_id, acl_updates)
    elif args.action == "delete":
        acl_manager.delete_acl(args.resource_id)
    else:
        print("Invalid arguments. Use --help for usage details.")