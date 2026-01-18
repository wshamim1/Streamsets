# IBM Watsonx Data Integrations (WXDI)

Examples and utilities for IBM Watsonx Data Integration platform.

## Structure

```
IBM Watsonx Data Integrations (WXDI)/
├── Connections/           # Connection management examples
│   ├── create_http_connections.py
│   ├── create_jdbc_connections.py
│   └── create_singlestore_connections.py
├── Flows/                # Flow creation examples
│   ├── batch_and_stream_flow_job.py
│   └── stream_flow_fraud_detection.py
└── PythonGenerator/      # Code generation utilities
    └── stage_generator.py
```

## Setup

1. Install IBM Watsonx Data Integration SDK:
```bash
pip install ibm-watsonx-data-integration
```

2. Configure environment variables:
```bash
# Add to your .env file
IBM_WATSONX_API_KEY=your-api-key-here
```

## Features

### Connection Management
- **HTTP Connections**: Create and manage HTTP-based connections
- **JDBC Connections**: Database connection management
- **SingleStore Connections**: SingleStore database integration

### Flow Management
- **Batch and Stream Flows**: Create hybrid batch/streaming flows
- **Fraud Detection**: Real-time fraud detection flow examples
- **Job Management**: Start, stop, and monitor flow jobs

### Code Generation
- **Stage Generator**: Automatically generate Python code for pipeline stages

## Usage Examples

### Create a StreamSets Flow
```python
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration import Platform

# Authenticate
auth = IAMAuthenticator(api_key='your-api-key')
platform = Platform(auth, base_api_url='https://api.ca-tor.dai.cloud.ibm.com')

# Get project
project = platform.projects.get(name="Your Project Name")

# Create flow
flow = project.create_flow(name="My Flow", flow_type="streamsets")
```

### Create Connections
See examples in the `Connections/` directory for specific connection types.

## Notes

- Requires IBM Watsonx Data Integration platform access
- API key must have appropriate permissions
- Base API URL varies by region (ca-tor, us-south, etc.)

## Documentation

- [IBM Watsonx Data Integration Documentation](https://www.ibm.com/docs/en/watsonx/data-integration)
- [Python SDK Reference](https://ibm.github.io/watsonx-data-integration-python-sdk/)