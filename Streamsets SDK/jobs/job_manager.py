from streamsets.sdk import ControlHub
from ..auth import StreamSetsAuth
import argparse

class JobManager:
    """
    Manages jobs in StreamSets Control Hub.
    """
    def __init__(self, control_hub: ControlHub):
        self.control_hub = control_hub
    
    def get_job_by_id(self, job_id: str):
        """Retrieves a job by its ID."""
        return self.control_hub.jobs.get(id=job_id)
    
    def get_all_jobs(self):
        """Retrieves all available jobs."""
        return self.control_hub.jobs.get_all()
    
    def start_job(self, job_id: str):
        """Starts a job by its ID."""
        job = self.get_job_by_id(job_id)
        if job:
            job.start()
            print(f"Job '{job.job_name}' started successfully.")
        else:
            print(f"Job with ID '{job_id}' not found.")
    
    def stop_job(self, job_id: str):
        """Stops a job by its ID."""
        job = self.get_job_by_id(job_id)
        if job:
            job.stop()
            print(f"Job '{job.job_name}' stopped successfully.")
        else:
            print(f"Job with ID '{job_id}' not found.")
    
    def restart_job(self, job_id: str):
        """Restarts a job by its ID."""
        job = self.get_job_by_id(job_id)
        if job:
            job.restart()
            print(f"Job '{job.job_name}' restarted successfully.")
        else:
            print(f"Job with ID '{job_id}' not found.")
    
    def delete_job(self, job_id: str):
        """Deletes a job by its ID."""
        job = self.get_job_by_id(job_id)
        if job:
            self.control_hub.delete_job(job)
            print(f"Job '{job.job_name}' deleted successfully.")
        else:
            print(f"Job with ID '{job_id}' not found.")
    
    def print_job_details(self, jobs):
        """Prints details of all retrieved jobs."""
        if jobs:
            for job in jobs:
                print("Job Name: " + job.job_name)
                print("Job ID: " + job.job_id)
                print("Job Status: " + job.status)
                print("----------------------------------------------------------")
        else:
            print("No jobs found.")

if __name__ == "__main__":
    # Authenticate with StreamSets
    auth = StreamSetsAuth()
    control_hub = auth.authenticate()
    job_manager = JobManager(control_hub)
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="StreamSets Job Manager")
    parser.add_argument("action", choices=["start", "stop", "restart", "delete", "list"], help="Action to perform")
    parser.add_argument("--job_id", type=str, help="Job ID (required for start, stop, restart, delete)")
    
    args = parser.parse_args()
    
    if args.action == "list":
        all_jobs = job_manager.get_all_jobs()
        job_manager.print_job_details(all_jobs)
    elif args.action in ["start", "stop", "restart", "delete"] and args.job_id:
        action_map = {
            "start": job_manager.start_job,
            "stop": job_manager.stop_job,
            "restart": job_manager.restart_job,
            "delete": job_manager.delete_job
        }
        action_map[args.action](args.job_id)
    else:
        print("Invalid arguments. Use --help for usage details.")
