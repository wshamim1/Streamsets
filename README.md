# StreamSets Integration Examples

A comprehensive collection of StreamSets integration examples, utilities, and automation scripts for various platforms and use cases.

## 📁 Repository Structure

### 🔷 StreamSets SDK Platform
Enterprise-grade utilities for StreamSets Control Hub (Platform SDK).

**Features:**
- ✅ Centralized authentication utilities
- ✅ Deployment management
- ✅ Job management and templates
- ✅ ACL (Access Control List) management
- ✅ Connection management
- ✅ Scheduler management
- ✅ Subscription management
- ✅ User and group management
- ✅ Pipeline builders and utilities

**Structure:**
```
StreamSets SDK Platform/
├── utils/              # Core utilities (auth, config)
├── deployments/        # Deployment management
├── jobs/              # Job and template management
├── acls/              # Access control management
├── connections/       # Connection management
├── scheduler/         # Scheduling utilities
├── subscriptions/     # Subscription management
├── user_groups/       # User/group management
└── pipelines/         # Pipeline builders
```

[📖 Full Documentation](StreamSets%20SDK%20Platform/readme.md)

### 🔶 StreamSets SDK 3.x
Examples and utilities for StreamSets Data Collector (on-premise SDK 3.x).

**Features:**
- ✅ Data Collector authentication
- ✅ Pipeline export/import utilities
- ✅ Stage configuration extraction
- ✅ Multiple pipeline builder examples

**Structure:**
```
StreamSets SDK 3.x/
├── utils/             # Core utilities
├── examples/          # Pipeline builder examples
└── Old/              # Legacy examples
```

[📖 Full Documentation](StreamSets%20SDK%203.x/README.md)

### 🔵 IBM Watsonx Data Integrations (WXDI)
Integration examples for IBM Watsonx Data Integration platform.

**Features:**
- Connection management (HTTP, JDBC, SingleStore)
- Flow creation (batch and streaming)
- Python code generation utilities

**Structure:**
```
IBM Watsonx Data Integrations (WXDI)/
├── Connections/       # Connection examples
├── Flows/            # Flow creation examples
└── PythonGenerator/  # Code generation utilities
```

### 🟢 Airflow Integrations
Apache Airflow integration examples for StreamSets job orchestration.

### 🟣 Streamlit Integrations
Streamlit-based UI examples for StreamSets job management.

### ⚙️ Automations
Automation scripts and deployment utilities.

## 🚀 Quick Start

### Prerequisites
```bash
# Install StreamSets SDK
pip install streamsets

# Install IBM Watsonx SDK (if needed)
pip install ibm-watsonx-data-integration

# Install other dependencies
pip install python-dotenv
```

### Configuration

1. **StreamSets Platform SDK:**
   ```bash
   cp "StreamSets SDK Platform/.env.example" "StreamSets SDK Platform/.env"
   # Edit .env with your credentials
   ```

2. **StreamSets SDK 3.x:**
   ```bash
   cp "StreamSets SDK 3.x/.env.example" "StreamSets SDK 3.x/.env"
   # Edit .env with your Data Collector URL
   ```

### Usage Examples

#### StreamSets Platform - Job Management
```python
from StreamSets_SDK_Platform.utils.auth import get_control_hub
from StreamSets_SDK_Platform.jobs.job_manager import JobManager

# Authenticate
sch = get_control_hub()
job_manager = JobManager(sch)

# List all jobs
jobs = job_manager.get_all_jobs()
job_manager.print_job_details(jobs)
```

#### StreamSets 3.x - Export Pipelines
```python
from StreamSets_SDK_3x.utils.auth import get_data_collector
from StreamSets_SDK_3x.utils.pipeline_utils import export_pipelines

# Authenticate
sdc = get_data_collector()

# Export pipelines
export_pipelines(sdc, output_file='my_pipelines.zip')
```

## 📚 Documentation

- [StreamSets Platform SDK Documentation](StreamSets%20SDK%20Platform/readme.md)
- [StreamSets SDK 3.x Documentation](StreamSets%20SDK%203.x/README.md)
- [StreamSets Official Documentation](https://docs.streamsets.com/)

## 🔧 Project Organization

This repository follows a modular structure:
- **Utilities** are centralized in `utils/` directories
- **Examples** are organized by functionality
- **Legacy code** is preserved in `Old/` directories
- **Documentation** is provided at each level

## 🤝 Contributing

When adding new examples or utilities:
1. Follow the existing directory structure
2. Add appropriate documentation
3. Include example usage
4. Update relevant README files

## 📝 Notes

- **Platform SDK** is for StreamSets Control Hub (cloud/enterprise)
- **SDK 3.x** is for on-premise Data Collector instances
- Environment files (`.env`) are gitignored - use `.env.example` as templates
- Import errors in IDE are expected if StreamSets SDK is not installed

## 🔐 Security

- Never commit `.env` files with actual credentials
- Use environment variables for sensitive data
- Review `.gitignore` before committing

## 📄 License

This is a collection of examples and utilities. Please refer to StreamSets licensing for SDK usage.