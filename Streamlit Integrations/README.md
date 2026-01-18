# Streamlit Integrations

Streamlit web application for StreamSets job management and orchestration.

## Overview

This directory contains a Streamlit-based web interface that provides an intuitive way to start and manage StreamSets jobs from templates with customizable runtime parameters.

## Files

- **streamsets_job_launcher.py** - Main Streamlit application
- **.env.example** - Environment variable template (to be created)

## Features

### User Interface
- 🎨 Clean, modern web interface
- 📋 Job template selection dropdown
- 🔧 Runtime parameter editor
- ⚙️ Configuration sidebar
- 📊 Job details display
- ✅ Success/error notifications

### Functionality
- **Job Template Discovery** - Search and list available job templates
- **Runtime Parameters** - View and edit job parameters in JSON format
- **Multi-Instance Launch** - Start multiple job instances simultaneously
- **Environment Selection** - Choose deployment environment (DEV/SIT/UAT/PROD)
- **Scheduling** - Configure cron expressions for recurring jobs
- **Date Selection** - Set job start dates

## Setup

### Prerequisites

```bash
# Install Streamlit
pip install streamlit

# Install StreamSets SDK
pip install streamsets

# Install other dependencies
pip install python-dotenv
```

### Configuration

1. Create environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your credentials:
```bash
SCH_URL=https://na01.hub.streamsets.com
CRED_ID=your-credential-id
CRED_TOKEN=your-api-token
LOGO_PATH=/path/to/logo.png  # Optional
```

## Usage

### Run the Application

```bash
streamlit run streamsets_job_launcher.py
```

The application will open in your default browser at `http://localhost:8501`

### Using the Interface

1. **Configure Settings** (Sidebar)
   - Set job template search pattern
   - Choose number of instances
   - Select engine label
   - Configure cron expression
   - Set start date

2. **Select Job Template**
   - Choose from available templates in dropdown
   - Templates are filtered by search pattern

3. **Edit Runtime Parameters**
   - View default parameters
   - Modify JSON as needed
   - Parameters are validated on submission

4. **Launch Job**
   - Click "🚀 Start Job" button
   - View job details and confirmation
   - Check for any errors

### Example Workflow

```
1. Open application → http://localhost:8501
2. Select job template → "S3_to_Snowflake"
3. Edit parameters → {"table": "customers", "batch_size": 1000}
4. Set instances → 3
5. Click "Start Job" → ✅ Success!
```

## Configuration Options

### Sidebar Settings

| Setting | Description | Default |
|---------|-------------|---------|
| Search Pattern | Filter job templates | `***` |
| Number of Instances | Parallel job instances | `1` |
| Engine Label | Deployment environment | `DEV` |
| Cron Expression | Schedule pattern | `*/5 * * * *` |
| Start Date | Job start date | Today |

### Runtime Parameters

Runtime parameters should be in JSON format:
```json
{
  "source_table": "customers",
  "target_table": "customers_processed",
  "batch_size": 1000,
  "enable_logging": true
}
```

## Customization

### Add Custom Logo

1. Set logo path in `.env`:
```bash
LOGO_PATH=/path/to/your/logo.png
```

2. Logo will appear in the header

### Modify UI Theme

Edit Streamlit config (`.streamlit/config.toml`):
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Add Custom Validations

Extend the `StreamSetsJobLauncher` class:
```python
def validate_parameters(self, params: str) -> bool:
    """Add custom parameter validation logic"""
    try:
        parsed = json.loads(params)
        # Add your validation rules
        return True
    except:
        return False
```

## Troubleshooting

### Common Issues

**Issue**: Application won't start
```bash
# Check Streamlit installation
streamlit --version

# Verify Python version (3.7+)
python --version
```

**Issue**: Authentication errors
- Verify CRED_ID and CRED_TOKEN in `.env`
- Check token hasn't expired
- Ensure SCH_URL is correct

**Issue**: No job templates found
- Check search pattern in sidebar
- Verify you have access to job templates
- Ensure templates exist in Control Hub

**Issue**: Runtime parameters error
- Validate JSON syntax
- Check parameter names match template
- Ensure required parameters are provided

## Advanced Features

### Session State Management

Streamlit maintains session state for:
- Selected job template
- Runtime parameters
- Configuration settings

### Error Handling

The application includes:
- Connection error handling
- Parameter validation
- Job start failure recovery
- User-friendly error messages

### Performance Optimization

- Caching of job template lists
- Lazy loading of runtime parameters
- Efficient API calls

## Deployment

### Local Development
```bash
streamlit run streamsets_job_launcher.py
```

### Production Deployment

**Option 1: Streamlit Cloud**
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Add secrets in dashboard
4. Deploy

**Option 2: Docker**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamsets_job_launcher.py"]
```

**Option 3: Server Deployment**
```bash
# Run with nohup
nohup streamlit run streamsets_job_launcher.py --server.port 8501 &

# Or use systemd service
sudo systemctl start streamlit-app
```

## Security Best Practices

1. **Never commit `.env` files** with credentials
2. **Use environment variables** for sensitive data
3. **Implement authentication** for production deployments
4. **Use HTTPS** in production
5. **Rotate tokens** regularly

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [StreamSets SDK Documentation](https://docs.streamsets.com/sdk/)
- [Streamlit Cloud](https://streamlit.io/cloud)