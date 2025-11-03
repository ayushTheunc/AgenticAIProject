1. Run 

```bash

pip install -r requirements.txt

```

2. Create an .env file and input these variables:

```bash

# Your Azure OpenAI API key (found in Keys and Endpoint section)
AZURE_OPENAI_API_KEY="your-api-key"

# Your Azure OpenAI endpoint URL (format: https://your-resource-name.openai.azure.com/)
AZURE_OPENAI_ENDPOINT=https://azureaiapi.cloud.unc.edu

# Your model deployment name (the name you gave when deploying the model)
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# API version (usually latest stable version)
AZURE_OPENAI_API_VERSION=2024-10-21


```


3. Run 

```bash

python sample.py



```