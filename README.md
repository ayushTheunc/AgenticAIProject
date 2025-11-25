# AI Code Grading Agent

An AI-powered code grading system using Azure OpenAI with a FastAPI web service layer.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create an `.env` file in the project root with these variables:

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

## Usage

### Option 1: Run as FastAPI Web Service (Recommended)

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Or run directly:

```bash
python main.py
```

The API will be available at `http://localhost:8000`

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Endpoints:**

- `GET /` - API status
- `GET /health` - Health check
- `POST /grade` - Grade a code submission

**Example API Request:**

```bash
curl -X POST "http://localhost:8000/grade" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "class Animal:\n    def __init__(self, name):\n        self.name = name",
    "rubric": "Grade based on: 1) Class exists 2) Constructor defined 3) Attributes set",
    "test_results": "All tests passed"
  }'
```

**Example with Python:**

```python
import requests

response = requests.post(
    "http://localhost:8000/grade",
    json={
        "code": "def hello():\n    print('Hello, World!')",
        "rubric": "Grade based on function definition and output",
        "test_results": "All tests passed"  # Optional
    }
)

result = response.json()
print(result["analysis"])
```

**Example with JavaScript/Frontend:**

```javascript
fetch('http://localhost:8000/grade', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    code: 'def hello():\n    print("Hello, World!")',
    rubric: 'Grade based on function definition and output',
    test_results: 'All tests passed'  // Optional
  })
})
.then(response => response.json())
.then(data => {
  console.log(data.analysis);
})
.catch(error => console.error('Error:', error));
```

### Option 2: Run Standalone Script

Run the original standalone grading script:

```bash
python sample.py
```

This will grade the code in `sampleCode.py` using the rubric in `sample.txt`.

## Project Structure

```
├── main.py              # FastAPI application entry point
├── grading_service.py   # Core grading logic with Azure OpenAI
├── models.py            # Pydantic models for API validation
├── sample.py            # Original standalone grading script
├── sample.txt           # Example rubric
├── sampleCode.py        # Example student submission
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (create this)
```

## API Response Format

**Success Response:**
```json
{
  "success": true,
  "analysis": "CRITERION 1: Class Structure Requirements (15/20 points)...",
  "error": null
}
```

**Error Response:**
```json
{
  "success": false,
  "analysis": "",
  "error": "Error message describing what went wrong"
}
```

## CORS Configuration

The API is configured to accept requests from common frontend development servers:
- http://localhost:3000 (React)
- http://localhost:5173 (Vite)
- http://localhost:8080 (Vue)

For production, update the `allow_origins` list in `main.py` to include only your frontend domain.

## Troubleshooting

**Service Unavailable Error:**
- Check that all environment variables are set in `.env`
- Verify your Azure OpenAI API key and endpoint are correct
- Ensure your deployment name matches your Azure resource

**Import Errors:**
- Run `pip install -r requirements.txt` to install all dependencies

**CORS Errors:**
- Add your frontend URL to the `allow_origins` list in `main.py`