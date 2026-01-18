# StreamSets Subscription Manager

## Overview
The **StreamSets Subscription Manager** is a Python script that allows users to manage event subscriptions in StreamSets Control Hub. It provides functionality to create, retrieve, list, and delete subscriptions using command-line arguments.

## Prerequisites
- Python 3.x
- StreamSets SDK (`streamsets.sdk`)
- Authentication module (`auth.StreamSetsAuth`)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/streamsets-subscription-manager.git
   cd streamsets-subscription-manager
   ```
2. Install dependencies:
   ```sh
   pip install streamsets
   ```

## Usage
The script supports various subscription management operations using command-line arguments.

### List All Subscriptions
```sh
python subscription_manager.py list
```

### Create a Subscription
```sh
python subscription_manager.py create --name "MySubscription" --event_type "JOB_STATUS_CHANGE" --webhook_url "https://your-webhook-url.com"
```

### Get Subscription by ID
```sh
python subscription_manager.py get_by_id --subscription_id <SUBSCRIPTION_ID>
```

### Get Subscription by Name
```sh
python subscription_manager.py get_by_name --name "MySubscription"
```

### Delete a Subscription
```sh
python subscription_manager.py delete --subscription_id <SUBSCRIPTION_ID>
```

## Error Handling
- If an invalid subscription ID or name is provided, an error message will be displayed.
- If no subscriptions are found when listing, an appropriate message will be printed.



## Author
Your Name

