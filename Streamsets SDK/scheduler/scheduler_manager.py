import argparse
import json
from streamsets.sdk import ControlHub
from ..auth import StreamSetsAuth

class SchedulerManager:
    """
    Manages scheduled tasks in StreamSets Control Hub.
    """
    def __init__(self, control_hub: ControlHub):
        self.control_hub = control_hub
    
    def get_scheduled_task_by_id(self, task_id: str):
        """Retrieves a scheduled task by its ID."""
        return self.control_hub.scheduled_tasks.get(id=task_id)
    
    def get_scheduled_task_by_name(self, name: str):
        """Retrieves a scheduled task by its name."""
        return self.control_hub.scheduled_tasks.get(name=name)
    
    def get_all_scheduled_tasks(self):
        """Retrieves all scheduled tasks."""
        return self.control_hub.scheduled_tasks.get_all()
    
    def create_scheduled_task(self, name: str, job_id: str, schedule: dict):
        """Creates a new scheduled task for a job."""
        job = self.control_hub.jobs.get(id=job_id)
        if job:
            task = self.control_hub.scheduled_tasks.create(name=name, job=job, schedule=schedule)
            print(f"Scheduled task '{task.name}' created successfully.")
            return task
        else:
            print(f"Job with ID '{job_id}' not found.")
            return None
    
    def delete_scheduled_task(self, task_id: str):
        """Deletes a scheduled task by its ID."""
        task = self.get_scheduled_task_by_id(task_id)
        if task:
            self.control_hub.scheduled_tasks.delete(task)
            print(f"Scheduled task '{task.name}' deleted successfully.")
        else:
            print(f"Scheduled task with ID '{task_id}' not found.")
    
    def print_scheduled_task_details(self, tasks):
        """Prints details of all retrieved scheduled tasks."""
        if tasks:
            for task in tasks:
                print("Scheduled Task Name: " + task.name)
                print("Task ID: " + task.id)
                print("----------------------------------------------------------")
        else:
            print("No scheduled tasks found.")

if __name__ == "__main__":
    # Authenticate with StreamSets
    auth = StreamSetsAuth()
    control_hub = auth.authenticate()
    scheduler_manager = SchedulerManager(control_hub)
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="StreamSets Scheduler Manager")
    parser.add_argument("action", choices=["list", "create", "get_by_id", "get_by_name", "delete"], help="Action to perform")
    parser.add_argument("--task_id", type=str, help="Scheduled Task ID (required for get_by_id and delete)")
    parser.add_argument("--name", type=str, help="Scheduled Task Name (required for get_by_name and create)")
    parser.add_argument("--job_id", type=str, help="Job ID (required for create)")
    parser.add_argument("--schedule", type=str, help="Schedule details in JSON format (required for create)")
    
    args = parser.parse_args()
    
    if args.action == "list":
        all_tasks = scheduler_manager.get_all_scheduled_tasks()
        scheduler_manager.print_scheduled_task_details(all_tasks)
    elif args.action == "create" and args.name and args.job_id and args.schedule:
        schedule = json.loads(args.schedule)
        scheduler_manager.create_scheduled_task(args.name, args.job_id, schedule)
    elif args.action == "get_by_id" and args.task_id:
        task = scheduler_manager.get_scheduled_task_by_id(args.task_id)
        scheduler_manager.print_scheduled_task_details([task] if task else [])
    elif args.action == "get_by_name" and args.name:
        task = scheduler_manager.get_scheduled_task_by_name(args.name)
        scheduler_manager.print_scheduled_task_details([task] if task else [])
    elif args.action == "delete" and args.task_id:
        scheduler_manager.delete_scheduled_task(args.task_id)
    else:
        print("Invalid arguments. Use --help for usage details.")