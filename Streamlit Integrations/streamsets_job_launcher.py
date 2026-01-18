"""
Streamlit Web Application for StreamSets Job Management

This application provides a user-friendly interface to start StreamSets jobs
from templates with customizable runtime parameters.
"""

import os
import ast
import datetime
from typing import List, Dict, Any

import streamlit as st
from streamsets.sdk import ControlHub
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class StreamSetsJobLauncher:
    """Helper class for StreamSets job operations in Streamlit."""
    
    def __init__(self):
        """Initialize StreamSets Control Hub connection."""
        self.sch_url = os.getenv('SCH_URL', 'https://na01.hub.streamsets.com')
        self.cred_id = os.getenv('CRED_ID')
        self.cred_token = os.getenv('CRED_TOKEN')
        
        if not self.cred_id or not self.cred_token:
            st.error("CRED_ID and CRED_TOKEN must be set in environment variables")
            st.stop()
        
        self.sch = ControlHub(
            sch_url=self.sch_url,
            credential_id=self.cred_id,
            token=self.cred_token
        )
    
    def fetch_all_job_templates(self, search_pattern: str = '***') -> List[str]:
        """
        Fetch all job templates matching the search pattern.
        
        Args:
            search_pattern: Search pattern for job names
            
        Returns:
            List of job template names
        """
        query = f'name=="{search_pattern}"'
        jobs = self.sch.jobs.get_all(search=query, job_template=True)
        return [job.job_name for job in jobs]
    
    def fetch_runtime_parameters(self, job_name: str) -> str:
        """
        Fetch runtime parameters for a job template.
        
        Args:
            job_name: Name of the job template
            
        Returns:
            Runtime parameters as string
        """
        query = f'name=="*{job_name}*"'
        job = self.sch.jobs.get(search=query, job_template=True)
        return job.runtime_parameters
    
    def start_job_from_template(self, job_name: str, 
                                runtime_params: List[str],
                                num_instances: int = 1) -> Any:
        """
        Start a job from template with runtime parameters.
        
        Args:
            job_name: Name of the job template
            runtime_params: List of runtime parameter strings
            num_instances: Number of job instances to start
            
        Returns:
            Started job instance(s)
        """
        job_template = self.sch.jobs.get(job_name=job_name)
        
        # Parse runtime parameters
        parsed_params = [ast.literal_eval(param) for param in runtime_params]
        
        # Start job from template
        job = self.sch.start_job_template(
            job_template,
            runtime_parameters=parsed_params,
            number_of_instances=num_instances
        )
        
        return job


def main():
    """Main Streamlit application."""
    
    # Page configuration
    st.set_page_config(
        page_title="StreamSets Job Launcher",
        page_icon="🚀",
        layout="wide"
    )
    
    # Header
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.title("🚀 StreamSets Job Launcher")
        st.markdown("Start StreamSets jobs from templates with custom parameters")
    with col2:
        # Optional: Add logo if available
        logo_path = os.getenv('LOGO_PATH')
        if logo_path and os.path.exists(logo_path):
            st.image(logo_path, width=200)
    
    # Initialize launcher
    try:
        launcher = StreamSetsJobLauncher()
    except Exception as e:
        st.error(f"Failed to initialize StreamSets connection: {str(e)}")
        st.stop()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Search pattern for job templates
        search_pattern = st.text_input(
            "Job Template Search Pattern",
            value="***",
            help="Use wildcards (*) to search for job templates"
        )
        
        # Number of instances
        num_instances = st.number_input(
            "Number of Instances",
            min_value=1,
            max_value=10,
            value=1,
            help="Number of job instances to start"
        )
        
        # Engine labels
        engine_label = st.selectbox(
            "Engine Label",
            options=['DEV', 'SIT', 'UAT', 'PROD'],
            help="Select the deployment environment"
        )
        
        # Cron expression
        cron_expression = st.text_input(
            "Cron Expression",
            value="*/5 * * * *",
            help="Schedule expression for recurring jobs"
        )
        
        # Start date
        start_date = st.date_input(
            "Start Date",
            value=datetime.date.today(),
            help="Job start date"
        )
    
    # Main content area
    st.header("📋 Job Template Selection")
    
    # Fetch job templates
    with st.spinner("Fetching job templates..."):
        try:
            job_templates = launcher.fetch_all_job_templates(search_pattern)
            
            if not job_templates:
                st.warning("No job templates found matching the search pattern.")
                st.stop()
            
        except Exception as e:
            st.error(f"Error fetching job templates: {str(e)}")
            st.stop()
    
    # Job template selection
    selected_job = st.selectbox(
        "Select Job Template",
        options=job_templates,
        help="Choose a job template to start"
    )
    
    # Fetch and display runtime parameters
    if selected_job:
        st.header("🔧 Runtime Parameters")
        
        try:
            runtime_params = launcher.fetch_runtime_parameters(selected_job)
            
            # Display runtime parameters in text area
            params_input = st.text_area(
                "Runtime Parameters (JSON format)",
                value=runtime_params,
                height=200,
                help="Edit runtime parameters as needed"
            )
            
        except Exception as e:
            st.error(f"Error fetching runtime parameters: {str(e)}")
            params_input = "{}"
    
    # Job submission form
    st.header("🚀 Launch Job")
    
    with st.form(key="job_launch_form"):
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            submit_button = st.form_submit_button(
                label="🚀 Start Job",
                use_container_width=True
            )
        
        with col2:
            if st.form_submit_button("🔄 Reset", use_container_width=True):
                st.rerun()
        
        # Handle job submission
        if submit_button:
            with st.spinner("Starting job..."):
                try:
                    # Start the job
                    job = launcher.start_job_from_template(
                        job_name=selected_job,
                        runtime_params=[params_input],
                        num_instances=num_instances
                    )
                    
                    # Display success message
                    st.success(f"✅ Job '{selected_job}' started successfully!")
                    
                    # Display job details
                    with st.expander("📊 Job Details", expanded=True):
                        st.json({
                            "Job Name": selected_job,
                            "Instances": num_instances,
                            "Engine Label": engine_label,
                            "Start Date": str(start_date),
                            "Cron Expression": cron_expression
                        })
                    
                    # Display job object info
                    st.info(f"Job ID: {job.job_id if hasattr(job, 'job_id') else 'N/A'}")
                    
                except Exception as e:
                    st.error(f"❌ Error starting job: {str(e)}")
                    st.exception(e)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>StreamSets Job Launcher | Powered by Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

# Made with Bob
