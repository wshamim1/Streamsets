# Airflow Integrations

Apache Airflow DAG examples for orchestrating StreamSets jobs.

## Overview

This directory contains Airflow DAG implementations that demonstrate how to integrate StreamSets jobs into Apache Airflow workflows for data pipeline orchestration.

## Files

- **streamsets_job_operator.py** - Main Airflow DAG with StreamSets job operators
- **.env.example** - Environment variable template

## Features

### StreamSetsJobOperator Class
A helper class that provides three methods to start StreamSets jobs:

1. **start_job_by_name()** - Start a job using StreamSets SDK by job name
2. **start_job_from_template()** - Start a job from a template with runtime parameters
3. **start_job_via_api()** - Start a job using REST API directly

### DAG Tasks

The example DAG includes:
- **start_streamsets_job_by_name** - Starts a job using SDK
- **print_timestamp** - Simple bash task for logging
- **start_job_from_template** - Starts a job from template
- **start_job_via_api** - Starts a job via REST API (optional)

## Setup

### Prerequisites

```bash
# Install Apache Airflow
pip install apache-airflow

# Install StreamSets SDK
pip install streamsets

# Install other dependencies
pip install python-dotenv requests
```

### Configuration

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` with your credentials:
```bash
SCH_URL=https://na01.hub.streamsets.com
CRED_ID=your-credential-id
CRED_TOKEN=your-api-token
STREAMSETS_JOB_NAME=Your Job Name
STREAMSETS_TEMPLATE_NAME=Your Template Name
STREAMSETS_JOB_ID=job-id:org-id  # Optional, for API method
```

### Deployment

1. Copy the DAG file to your Airflow DAGs folder:
```bash
cp streamsets_job_operator.py $AIRFLOW_HOME/dags/
```

2. Ensure environment variables are accessible to Airflow:
   - Add to Airflow environment
   - Or use Airflow Variables/Connections

3. Restart Airflow scheduler:
```bash
airflow scheduler
```

## Usage

### View DAG in Airflow UI
1. Navigate to Airflow UI (typically http://localhost:8080)
2. Find DAG: `streamsets_job_orchestration`
3. Enable the DAG
4. Trigger manually or wait for schedule

### Customize the DAG

Modify task dependencies:
```python
# Sequential execution
task1 >> task2 >> task3

# Parallel execution
task1 >> [task2, task3] >> task4
```

Add custom parameters:
```python
start_template_task = PythonOperator(
    task_id='start_job_from_template',
    python_callable=streamsets_operator.start_job_from_template,
    op_kwargs={
        'template_name': 'MyTemplate',
        'runtime_parameters': [{'param1': 'value1'}]
    },
)
```

## Task Dependencies

Default flow:
```
start_job_by_name → print_timestamp → start_job_from_template → start_job_via_api
```

## Error Handling

The operator includes:
- Automatic retries (configurable in default_args)
- Exception handling for API calls
- Job status monitoring with wait_for_job_status()

## Best Practices

1. **Use Airflow Variables** for sensitive data instead of .env files in production
2. **Set appropriate retry policies** based on job characteristics
3. **Monitor job status** using StreamSets Control Hub
4. **Use XCom** to pass data between tasks if needed
5. **Configure email alerts** for job failures

## Troubleshooting

### Common Issues

**Issue**: DAG not appearing in Airflow UI
- Check DAG file syntax: `python streamsets_job_operator.py`
- Verify file is in correct DAGs folder
- Check Airflow logs: `$AIRFLOW_HOME/logs/scheduler/`

**Issue**: Authentication failures
- Verify CRED_ID and CRED_TOKEN are correct
- Check token hasn't expired
- Ensure SCH_URL is correct for your region

**Issue**: Job not starting
- Verify job name/ID is correct
- Check job is not already running
- Ensure sufficient resources in StreamSets deployment

## Additional Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [StreamSets SDK Documentation](https://docs.streamsets.com/sdk/)
- [StreamSets REST API Documentation](https://docs.streamsets.com/platform-controlhub/latest/controlhub/UserGuide/RestAPI/RestAPI-Title.html)