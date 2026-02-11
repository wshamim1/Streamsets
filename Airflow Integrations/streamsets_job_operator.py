"""
Apache Airflow DAG for StreamSets Job Orchestration

This module provides examples of integrating StreamSets jobs with Apache Airflow,
demonstrating multiple methods to start and monitor StreamSets jobs.
"""

import os
from datetime import datetime, timedelta
from typing import Dict, Any

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv
import requests
from streamsets.sdk import ControlHub

# Load environment variables
load_dotenv()


class StreamSetsJobOperator:
    """Helper class for StreamSets job operations in Airflow."""
    
    def __init__(self):
        """Initialize StreamSets Control Hub connection."""
        self.sch_url = os.getenv('SCH_URL', 'https://na01.hub.streamsets.com')
        self.cred_id = os.getenv('CRED_ID')
        self.cred_token = os.getenv('CRED_TOKEN')
        
        if not self.cred_id or not self.cred_token:
            raise ValueError("CRED_ID and CRED_TOKEN must be set in environment variables")
        
        self.sch = ControlHub(
            sch_url=self.sch_url,
            credential_id=self.cred_id,
            token=self.cred_token
        )
    
    def start_job_by_name(self, job_name: str) -> str:
        """
        Start a StreamSets job by name and wait for completion.
        
        Args:
            job_name: Name of the job to start
            
        Returns:
            str: Status message
        """
        print(f"Starting job: {job_name}")
        job = self.sch.jobs.get(job_name=job_name)
        
        # Start the job
        self.sch.start_job(job)
        print(f"Job {job_name} started successfully")
        
        # Wait for job to complete
        result = self.sch.wait_for_job_status(job=job, status='INACTIVE')
        print(f"Job {job_name} completed with status: {result}")
        
        return f"Job {job_name} completed successfully"
    
    def start_job_from_template(self, template_name: str, 
                                runtime_parameters: list = None) -> str:
        """
        Start a job from a job template with runtime parameters.
        
        Args:
            template_name: Name of the job template
            runtime_parameters: List of parameter dictionaries
            
        Returns:
            str: Status message
        """
        print(f"Starting job from template: {template_name}")
        job_template = self.sch.jobs.get(job_name=template_name)
        
        if runtime_parameters is None:
            runtime_parameters = [{}]
        
        # Start job from template
        jobs = self.sch.start_job_template(
            job_template,
            instance_name_suffix='PARAM_VALUE',
            parameter_name='x',
            runtime_parameters=runtime_parameters
        )
        
        # Wait for completion
        result = self.sch.wait_for_job_status(job=jobs, status='INACTIVE')
        print(f"Job from template {template_name} completed with status: {result}")
        
        return f"Job from template {template_name} completed successfully"
    
    def start_job_via_api(self, job_id: str) -> str:
        """
        Start a StreamSets job using REST API directly.
        
        Args:
            job_id: Full job ID (including organization ID)
            
        Returns:
            str: API response text
        """
        url = f"{self.sch_url}/jobrunner/rest/v1/job/{job_id}/start"
        
        headers = {
            'Content-Type': 'application/json',
            'X-Requested-By': 'airflow',
            'X-SS-REST-CALL': 'true',
            'X-SS-App-Component-Id': self.cred_id,
            'X-SS-App-Auth-Token': self.cred_token
        }
        
        response = requests.post(url, headers=headers)
        
        print(f"API Response Status: {response.status_code}")
        print(f"API Response: {response.text}")
        
        if response.status_code == 200:
            return f"Job {job_id} started successfully via API"
        else:
            raise Exception(f"Failed to start job: {response.text}")


# Initialize operator
streamsets_operator = StreamSetsJobOperator()


# Define Airflow DAG
default_args = {
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='streamsets_job_orchestration',
    default_args=default_args,
    description='StreamSets job orchestration with multiple start methods',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['streamsets', 'data-pipeline'],
) as dag:
    
    # Task 1: Start job by name using SDK
    start_job_task = PythonOperator(
        task_id='start_streamsets_job_by_name',
        python_callable=streamsets_operator.start_job_by_name,
        op_kwargs={'job_name': os.getenv('STREAMSETS_JOB_NAME', 'S3_Trash - 1')},
    )
    
    # Task 2: Print timestamp
    print_date_task = BashOperator(
        task_id='print_timestamp',
        bash_command='date',
    )
    
    # Task 3: Start job from template
    start_template_task = PythonOperator(
        task_id='start_job_from_template',
        python_callable=streamsets_operator.start_job_from_template,
        op_kwargs={
            'template_name': os.getenv('STREAMSETS_TEMPLATE_NAME', 'S3_Trash'),
            'runtime_parameters': [{}]
        },
    )
    
    # Task 4: Start job via API (if job ID is provided)
    job_id = os.getenv('STREAMSETS_JOB_ID')
    if job_id:
        start_api_task = PythonOperator(
            task_id='start_job_via_api',
            python_callable=streamsets_operator.start_job_via_api,
            op_kwargs={'job_id': job_id},
        )
        
        # Define task dependencies
        start_job_task >> print_date_task >> start_template_task >> start_api_task
    else:
        # Define task dependencies without API task
        start_job_task >> print_date_task >> start_template_task


if __name__ == "__main__":
    print("This is an Airflow DAG file. Run it with Airflow scheduler.")


