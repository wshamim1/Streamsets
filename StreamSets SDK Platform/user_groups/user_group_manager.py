"""
User and Group Manager for StreamSets Platform SDK
Manages users and groups in StreamSets Control Hub
"""
import argparse
from streamsets.sdk import ControlHub
from ..utils.auth import get_control_hub


class UserGroupManager:
    """
    Manages users and groups in StreamSets Control Hub.
    """
    def __init__(self, control_hub: ControlHub):
        self.control_hub = control_hub
    
    # User Management
    def get_user_by_id(self, user_id: str):
        """Retrieves a user by their ID."""
        return self.control_hub.users.get(id=user_id)
    
    def get_user_by_name(self, name: str):
        """Retrieves a user by their name."""
        return self.control_hub.users.get(name=name)
    
    def get_all_users(self):
        """Retrieves all users."""
        return self.control_hub.users.get_all()
    
    def create_user(self, email: str, roles: list):
        """Creates a new user with assigned roles."""
        user = self.control_hub.users.create(email=email, roles=roles)
        print(f"User '{user.email}' created successfully.")
        return user
    
    def delete_user(self, user_id: str):
        """Deletes a user by their ID."""
        user = self.get_user_by_id(user_id)
        if user:
            self.control_hub.users.delete(user)
            print(f"User '{user.email}' deleted successfully.")
        else:
            print(f"User with ID '{user_id}' not found.")
    
    # Group Management
    def get_group_by_id(self, group_id: str):
        """Retrieves a group by its ID."""
        return self.control_hub.groups.get(id=group_id)
    
    def get_group_by_name(self, name: str):
        """Retrieves a group by its name."""
        return self.control_hub.groups.get(name=name)
    
    def get_all_groups(self):
        """Retrieves all groups."""
        return self.control_hub.groups.get_all()
    
    def create_group(self, name: str, description: str):
        """Creates a new group."""
        group = self.control_hub.groups.create(name=name, description=description)
        print(f"Group '{group.name}' created successfully.")
        return group
    
    def delete_group(self, group_id: str):
        """Deletes a group by its ID."""
        group = self.get_group_by_id(group_id)
        if group:
            self.control_hub.groups.delete(group)
            print(f"Group '{group.name}' deleted successfully.")
        else:
            print(f"Group with ID '{group_id}' not found.")
    
    def print_user_details(self, users):
        """Prints details of all retrieved users."""
        if users:
            for user in users:
                print("User Email: " + user.email)
                print("User ID: " + user.id)
                print("Roles: " + ", ".join(user.roles))
                print("----------------------------------------------------------")
        else:
            print("No users found.")
    
    def print_group_details(self, groups):
        """Prints details of all retrieved groups."""
        if groups:
            for group in groups:
                print("Group Name: " + group.name)
                print("Group ID: " + group.id)
                print("Description: " + group.description)
                print("----------------------------------------------------------")
        else:
            print("No groups found.")

if __name__ == "__main__":
    # Authenticate with StreamSets
    control_hub = get_control_hub()
    user_group_manager = UserGroupManager(control_hub)
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="StreamSets User and Group Manager")
    parser.add_argument("action", choices=["list_users", "create_user", "get_user_by_id", "get_user_by_name", "delete_user",
                                           "list_groups", "create_group", "get_group_by_id", "get_group_by_name", "delete_group"], help="Action to perform")
    parser.add_argument("--user_id", type=str, help="User ID (required for get_user_by_id and delete_user)")
    parser.add_argument("--email", type=str, help="User Email (required for create_user)")
    parser.add_argument("--roles", type=str, help="Comma-separated roles for the user (required for create_user)")
    parser.add_argument("--group_id", type=str, help="Group ID (required for get_group_by_id and delete_group)")
    parser.add_argument("--name", type=str, help="Group Name (required for create_group and get_group_by_name)")
    parser.add_argument("--description", type=str, help="Group Description (required for create_group)")
    
    args = parser.parse_args()
    
    if args.action == "list_users":
        all_users = user_group_manager.get_all_users()
        user_group_manager.print_user_details(all_users)
    elif args.action == "create_user" and args.email and args.roles:
        roles = args.roles.split(',')
        user_group_manager.create_user(args.email, roles)
    elif args.action == "get_user_by_id" and args.user_id:
        user = user_group_manager.get_user_by_id(args.user_id)
        user_group_manager.print_user_details([user] if user else [])
    elif args.action == "get_user_by_name" and args.name:
        user = user_group_manager.get_user_by_name(args.name)
        user_group_manager.print_user_details([user] if user else [])
    elif args.action == "delete_user" and args.user_id:
        user_group_manager.delete_user(args.user_id)
    elif args.action == "list_groups":
        all_groups = user_group_manager.get_all_groups()
        user_group_manager.print_group_details(all_groups)
    elif args.action == "create_group" and args.name and args.description:
        user_group_manager.create_group(args.name, args.description)
    elif args.action == "get_group_by_id" and args.group_id:
        group = user_group_manager.get_group_by_id(args.group_id)
        user_group_manager.print_group_details([group] if group else [])
    elif args.action == "get_group_by_name" and args.name:
        group = user_group_manager.get_group_by_name(args.name)
        user_group_manager.print_group_details([group] if group else [])
    elif args.action == "delete_group" and args.group_id:
        user_group_manager.delete_group(args.group_id)
    else:
        print("Invalid arguments. Use --help for usage details.")