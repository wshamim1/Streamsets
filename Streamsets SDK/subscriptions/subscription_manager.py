import argparse
import json
from streamsets.sdk import ControlHub
from ..auth import StreamSetsAuth

class SubscriptionManager:
    """
    Manages subscriptions in StreamSets Control Hub.
    """
    def __init__(self, control_hub: ControlHub):
        self.control_hub = control_hub
    
    def get_subscription_by_id(self, subscription_id: str):
        """Retrieves a subscription by its ID."""
        return self.control_hub.subscriptions.get(id=subscription_id)
    
    def get_subscription_by_name(self, name: str):
        """Retrieves a subscription by its name."""
        return self.control_hub.subscriptions.get(name=name)
    
    def get_all_subscriptions(self):
        """Retrieves all available subscriptions."""
        return self.control_hub.subscriptions.get_all()
    
    def create_subscription(self, name: str, event_type: str, webhook_url: str):
        """Creates a new subscription for an event type with a webhook URL."""
        subscription = self.control_hub.subscriptions.create(
            name=name, event_type=event_type, webhook_url=webhook_url
        )
        print(f"Subscription '{subscription.name}' created successfully.")
        return subscription
    
    def delete_subscription(self, subscription_id: str):
        """Deletes a subscription by its ID."""
        subscription = self.get_subscription_by_id(subscription_id)
        if subscription:
            self.control_hub.subscriptions.delete(subscription)
            print(f"Subscription '{subscription.name}' deleted successfully.")
        else:
            print(f"Subscription with ID '{subscription_id}' not found.")
    
    def print_subscription_details(self, subscriptions):
        """Prints details of all retrieved subscriptions."""
        if subscriptions:
            for subscription in subscriptions:
                print("Subscription Name: " + subscription.name)
                print("Subscription ID: " + subscription.id)
                print("Event Type: " + subscription.event_type)
                print("Webhook URL: " + subscription.webhook_url)
                print("----------------------------------------------------------")
        else:
            print("No subscriptions found.")

if __name__ == "__main__":
    # Authenticate with StreamSets
    auth = StreamSetsAuth()
    control_hub = auth.authenticate()
    subscription_manager = SubscriptionManager(control_hub)
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="StreamSets Subscription Manager")
    parser.add_argument("action", choices=["list", "create", "get_by_id", "get_by_name", "delete"], help="Action to perform")
    parser.add_argument("--subscription_id", type=str, help="Subscription ID (required for get_by_id and delete)")
    parser.add_argument("--name", type=str, help="Subscription Name (required for get_by_name and create)")
    parser.add_argument("--event_type", type=str, help="Event Type (required for create)")
    parser.add_argument("--webhook_url", type=str, help="Webhook URL (required for create)")
    
    args = parser.parse_args()
    
    if args.action == "list":
        all_subscriptions = subscription_manager.get_all_subscriptions()
        subscription_manager.print_subscription_details(all_subscriptions)
    elif args.action == "create" and args.name and args.event_type and args.webhook_url:
        subscription_manager.create_subscription(args.name, args.event_type, args.webhook_url)
    elif args.action == "get_by_id" and args.subscription_id:
        subscription = subscription_manager.get_subscription_by_id(args.subscription_id)
        subscription_manager.print_subscription_details([subscription] if subscription else [])
    elif args.action == "get_by_name" and args.name:
        subscription = subscription_manager.get_subscription_by_name(args.name)
        subscription_manager.print_subscription_details([subscription] if subscription else [])
    elif args.action == "delete" and args.subscription_id:
        subscription_manager.delete_subscription(args.subscription_id)
    else:
        print("Invalid arguments. Use --help for usage details.")