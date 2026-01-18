# StreamSets SDK 3.x - Pipeline Management

## Overview
This repository provides a structured Python implementation for interacting with StreamSets Control Hub using the StreamSets SDK (3.x). It allows users to authenticate, retrieve Data Collector instances, and manage pipelines efficiently.

## Features
- Authenticate with StreamSets Control Hub using environment variables.
- Retrieve Data Collector instances.
- Fetch pipelines by ID, name, or commit ID.
- Retrieve all pipelines and display their details.

## Prerequisites
Ensure you have the following installed:
- Python 3.x
- `pip` (Python package manager)
- Required Python packages: `streamsets.sdk`, `python-dotenv`

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/wshamim1/Streamsets.git
   cd Streamsets/Streamsets\ SDK/3.x
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Setup
Create a `.env` file in the root directory with the following variables:
```
CONTROL_HUB_URL=https://your-streamsets-url.com
CONTROL_HUB_USER=your-username
CONTROL_HUB_PW=your-password
ENGINE_ID=your-engine-id
```

## Usage
Run the script to authenticate and retrieve pipelines:
```sh
python streamsets_pipeline.py
```

## Code Structure
### `StreamSetsAuth`
Handles authentication and environment variable loading.

### `DataCollectorManager`
Retrieves the Data Collector instance.

### `PipelineManager`
- Fetches pipelines by ID, name, or commit ID.
- Retrieves and prints details of all pipelines.

## Example Output
```
Pipeline Name: SamplePipeline
Pipeline Commit ID: abc123
Pipeline Version: 1
Pipeline ID: 1234-5678-9012-3456
----------------------------------------------------------
```

## License


## Contributions
Feel free to contribute by submitting issues and pull requests!

