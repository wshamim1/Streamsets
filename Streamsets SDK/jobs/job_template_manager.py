import argparse
import json
from streamsets.sdk import ControlHub
from ..auth import StreamSetsAuth

class JobTemplateManager:
    """
    Manages job templates in StreamSets Control Hub.
    """
    def __init__(self, control_hub: ControlHub):
        self.control_hub = control_hub
    
    def get_template_by_id(self, template_id: str):
        """Retrieves a job template by its ID."""
        return self.control_hub.job_templates.get(id=template_id)
    
    def get_template_by_name(self, name: str):
        """Retrieves a job template by its name."""
        return self.control_hub.job_templates.get(name=name)
    
    def get_all_templates(self):
        """Retrieves all available job templates."""
        return self.control_hub.job_templates.get_all()
    
    def create_job_from_template(self, template_id: str, job_name: str, parameters: dict = None):
        """Creates a job from a template using optional parameters."""
        template = self.get_template_by_id(template_id)
        if template:
            job = template.create_job(job_name=job_name, parameters=parameters or {})
            print(f"Job '{job.job_name}' created successfully from template '{template.name}'.")
            return job
        else:
            print(f"Template with ID '{template_id}' not found.")
            return None
    
    def print_template_details(self, templates):
        """Prints details of all retrieved job templates."""
        if templates:
            for template in templates:
                print("Template Name: " + template.name)
                print("Template ID: " + template.id)
                print("----------------------------------------------------------")
        else:
            print("No templates found.")

if __name__ == "__main__":
    # Authenticate with StreamSets
    auth = StreamSetsAuth()
    control_hub = auth.authenticate()
    job_template_manager = JobTemplateManager(control_hub)
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="StreamSets Job Template Manager")
    parser.add_argument("action", choices=["list", "create", "get_by_id", "get_by_name", "start", "stop", "restart", "delete"], help="Action to perform")
    parser.add_argument("--template_id", type=str, help="Template ID (required for create and get_by_id)")
    parser.add_argument("--name", type=str, help="Template Name (required for get_by_name)")
    parser.add_argument("--job_name", type=str, help="Job Name (required for create)")
    parser.add_argument("--parameters", type=str, help="Optional job parameters in JSON format")
    
    args = parser.parse_args()
    
    if args.action == "list":
        all_templates = job_template_manager.get_all_templates()
        job_template_manager.print_template_details(all_templates)
    elif args.action == "create" and args.template_id and args.job_name:
        parameters = json.loads(args.parameters) if args.parameters else {}
        job_template_manager.create_job_from_template(args.template_id, args.job_name, parameters)
    elif args.action == "get_by_id" and args.template_id:
        template = job_template_manager.get_template_by_id(args.template_id)
        job_template_manager.print_template_details([template] if template else [])
    elif args.action == "get_by_name" and args.name:
        template = job_template_manager.get_template_by_name(args.name)
        job_template_manager.print_template_details([template] if template else [])
    elif args.action in ["start", "stop", "restart", "delete"]:
        print(f"Action '{args.action}' is not implemented yet.")
    else:
        print("Invalid arguments. Use --help for usage details.")
