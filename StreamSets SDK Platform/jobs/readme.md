# StreamSets Job Manager

## Overview
StreamSets Job Manager is a Python script that allows users to manage jobs in StreamSets Control Hub. It provides functionality to start, stop, restart, delete jobs, and list all available jobs.

## Prerequisites
- Python 3.x
- StreamSets SDK (`streamsets.sdk`)
- Authentication module (`auth.StreamSetsAuth`)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/streamsets-job-manager.git
   cd streamsets-job-manager
   ```
2. Install dependencies:
   ```sh
   pip install streamsets
   ```

## Usage
The script supports various job management operations using command-line arguments.

### List All Jobs
```sh
python job_manager.py list
```

### Start a Job
```sh
python job_manager.py start --job_id <JOB_ID>
```

### Stop a Job
```sh
python job_manager.py stop --job_id <JOB_ID>
```

### Restart a Job
```sh
python job_manager.py restart --job_id <JOB_ID>
```

### Delete a Job
```sh
python job_manager.py delete --job_id <JOB_ID>
```

## Error Handling
- If a job ID is invalid, an error message will be displayed.
- If no jobs are found when listing, an appropriate message will be printed.



## Author
Your Name

