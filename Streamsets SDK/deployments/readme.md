# StreamSets Deployment Manager

## Overview
The **StreamSets Deployment Manager** is a Python script that allows users to manage self-managed deployments in StreamSets Control Hub. It provides functionality to create, retrieve, list, and delete deployments using command-line arguments.

## Prerequisites
- Python 3.x
- StreamSets SDK (`streamsets.sdk`)
- Authentication module (`auth.StreamSetsAuth`)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/streamsets-deployment-manager.git
   cd streamsets-deployment-manager
   ```
2. Install dependencies:
   ```sh
   pip install streamsets
   ```

## Usage
The script supports various deployment management operations using command-line arguments.

### List All Deployments
```sh
python deployment_manager.py list
```

### Create a Deployment
```sh
python deployment_manager.py create --name "MyDeployment" --engine_type "DATA_COLLECTOR" --configuration '{"property": "value"}'
```

### Get Deployment by ID
```sh
python deployment_manager.py get_by_id --deployment_id <DEPLOYMENT_ID>
```

### Get Deployment by Name
```sh
python deployment_manager.py get_by_name --name "MyDeployment"
```

### Delete a Deployment
```sh
python deployment_manager.py delete --deployment_id <DEPLOYMENT_ID>
```

## Error Handling
- If an invalid deployment ID or name is provided, an error message will be displayed.
- If no deployments are found when listing, an appropriate message will be printed.

## License
This project is licensed under the MIT License.

## Author
Your Name