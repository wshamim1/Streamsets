# StreamSets User and Group Manager

## Overview
The **StreamSets User and Group Manager** is a Python script that allows users to manage users and groups in StreamSets Control Hub. It provides functionality to create, retrieve, list, and delete users and groups using command-line arguments.

## Prerequisites
- Python 3.x
- StreamSets SDK (`streamsets.sdk`)
- Authentication module (`auth.StreamSetsAuth`)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/streamsets-user-group-manager.git
   cd streamsets-user-group-manager
   ```
2. Install dependencies:
   ```sh
   pip install streamsets
   ```

## Usage
The script supports various user and group management operations using command-line arguments.

### List All Users
```sh
python user_group_manager.py list_users
```

### Create a User
```sh
python user_group_manager.py create_user --email "user@example.com" --roles "admin,operator"
```

### Get User by ID
```sh
python user_group_manager.py get_user_by_id --user_id <USER_ID>
```

### Get User by Name
```sh
python user_group_manager.py get_user_by_name --name "username"
```

### Delete a User
```sh
python user_group_manager.py delete_user --user_id <USER_ID>
```

### List All Groups
```sh
python user_group_manager.py list_groups
```

### Create a Group
```sh
python user_group_manager.py create_group --name "MyGroup" --description "Example Group"
```

### Get Group by ID
```sh
python user_group_manager.py get_group_by_id --group_id <GROUP_ID>
```

### Get Group by Name
```sh
python user_group_manager.py get_group_by_name --name "MyGroup"
```

### Delete a Group
```sh
python user_group_manager.py delete_group --group_id <GROUP_ID>
```

## Error Handling
- If an invalid user or group ID/name is provided, an error message will be displayed.
- If no users or groups are found when listing, an appropriate message will be printed.



## Author
WS

