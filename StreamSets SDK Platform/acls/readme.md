# StreamSets ACL Manager

## Overview
The **StreamSets ACL Manager** is a Python script that allows users to manage Access Control Lists (ACLs) in StreamSets Control Hub. It provides functionality to retrieve, update, and delete ACLs using command-line arguments.

## Prerequisites
- Python 3.x
- StreamSets SDK (`streamsets.sdk`)
- Authentication module (`auth.StreamSetsAuth`)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/streamsets-acl-manager.git
   cd streamsets-acl-manager
   ```
2. Install dependencies:
   ```sh
   pip install streamsets
   ```

## Usage
The script supports various ACL management operations using command-line arguments.

### Get ACL by Resource ID
```sh
python acl_manager.py get --resource_id <RESOURCE_ID>
```

### Update ACL for a Resource
```sh
python acl_manager.py update --resource_id <RESOURCE_ID> --acl_updates '{"permissions": {"user@example.com": "READ"}}'
```

### Delete ACL for a Resource
```sh
python acl_manager.py delete --resource_id <RESOURCE_ID>
```

## Error Handling
- If an invalid resource ID is provided, an error message will be displayed.
- If no ACL is found when retrieving, an appropriate message will be printed.



## Author
Your Name