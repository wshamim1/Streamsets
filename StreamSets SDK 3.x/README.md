# StreamSets SDK 3.x

This directory contains examples and utilities for working with StreamSets Data Collector using SDK 3.x.

## Structure

```
StreamSets SDK 3.x/
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── auth.py                     # Authentication utilities
│   └── pipeline_utils.py           # Pipeline management utilities
├── examples/                       # Example pipeline builders
│   ├── CreateTransformerPipeline.py
│   ├── CreateTRPipeline_S3_S3.py
│   ├── DEV_To_Trash_Platform.py
│   ├── GenerateSimplePipeline.py
│   ├── Get_Stage_configurations.py
│   ├── JDBC_S3_with_StreamSelector.py
│   ├── S3_Deltalake.py
│   ├── S3_To_S3.py
│   └── sdk_transformer.py
├── Old/                            # Legacy/archived examples
└── .env                            # Environment configuration

```

## Setup

1. Install StreamSets SDK:
```bash
pip install streamsets
```

2. Configure environment variables in `.env`:
```
SDC_URL=http://your-sdc-host:18630
SDC_USERNAME=admin
SDC_PASSWORD=admin
STREAMSETS_SDK_ACTIVATION_KEY=your-activation-key
```

## Usage

### Authentication

```python
from utils.auth import get_data_collector

# Get authenticated Data Collector instance
sdc = get_data_collector()
```

### Export Pipelines

```python
from utils.pipeline_utils import export_pipelines

# Export all pipelines
export_pipelines(sdc, output_file='my_pipelines.zip')

# Export filtered pipelines
export_pipelines(sdc, output_file='filtered.zip', pipeline_filter='kafka')
```

### Get Pipeline Stages

```python
from utils.pipeline_utils import get_pipeline_stages

# Print to console
get_pipeline_stages(sdc, 'my-pipeline', output_format='console')

# Export to CSV
get_pipeline_stages(sdc, 'my-pipeline', output_format='csv')
```

## Examples

See the `examples/` directory for various pipeline builder examples:
- **S3_To_S3.py**: S3 to S3 data movement
- **S3_Deltalake.py**: S3 to Delta Lake integration
- **JDBC_S3_with_StreamSelector.py**: JDBC to S3 with stream routing
- **CreateTransformerPipeline.py**: Transformer pipeline examples

## Notes

- This uses StreamSets SDK 3.x for Data Collector (on-premise)
- For Platform/Control Hub, see `StreamSets SDK Platform/` directory
- Legacy examples are in the `Old/` subdirectory