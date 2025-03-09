# StreamSets Scheduler Manager

## Overview
The **StreamSets Scheduler Manager** is a Python script that allows users to manage scheduled tasks in StreamSets Control Hub. It provides functionality to create, retrieve, list, and delete scheduled tasks using command-line arguments.

## Prerequisites
- Python 3.x
- StreamSets SDK (`streamsets.sdk`)
- Authentication module (`auth.StreamSetsAuth`)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/streamsets-scheduler-manager.git
   cd streamsets-scheduler-manager
   ```
2. Install dependencies:
   ```sh
   pip install streamsets
   ```

## Usage
The script supports various scheduled task management operations using command-line arguments.

### List All Scheduled Tasks
```sh
python scheduler_manager.py list
```

### Create a Scheduled Task
```sh
python scheduler_manager.py create --name "MyScheduledTask" --job_id "example-job-id" --schedule '{"cron": "0 0 * * *"}'
```

### Get Scheduled Task by ID
```sh
python scheduler_manager.py get_by_id --task_id <TASK_ID>
```

### Get Scheduled Task by Name
```sh
python scheduler_manager.py get_by_name --name "MyScheduledTask"
```

### Delete a Scheduled Task
```sh
python scheduler_manager.py delete --task_id <TASK_ID>
```

## Error Handling
- If an invalid scheduled task ID or name is provided, an error message will be displayed.
- If no scheduled tasks are found when listing, an appropriate message will be printed.



## Author
Your Name

