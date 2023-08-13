# AzureOpenAIMeasuringTime
## What this?
This repository measures the response speed between regions of Azure OpenAI Service. It compares the Japan East region with the East US region.

## Preparation
### Environment
Please install Python3.10.x or later version.
### Dependencies
Run command `pip install -r requirements.txt`.
### Azure Resources
- Azure OpenAI Service hosting on Japan East region.  
- Azure OpenAI Service hosting on East US region.  
Each resource should have deployment `gpt-3.5-turbo` model named `gpt35`.

### Update Program
Copy endpoint and key from each resouce. You can copy them by `Key and Endpoint` tab on Azure Portal.
After that, Paste them to app.py.
```python
ENDPOINT_JP = "<Insert Japan East URL>"
ENDPOINT_US = "<Insert East US URL>"
KEY_JP = "<Insert Japan East Key>"
KEY_US = "<Insert East US Key>"
```

