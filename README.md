# AI Code Grading Agent

An AI-powered code grading system using Azure OpenAI with a FastAPI backend and React frontend.

## Overview

This application provides Teaching Assistants (TAs) in upper-level computer science courses with an intelligent grading assistant that evaluates code quality aspects that traditional autograders cannot assess. While autograders excel at checking correctness and test case compliance, they struggle with evaluating:

- **Code style and formatting** - Naming conventions, indentation, PEP 8 compliance
- **Documentation quality** - Docstrings, inline comments, and code clarity
- **Design patterns** - Code organization, modularity, and architecture
- **Best practices** - Pythonic idioms, proper use of language features
- **Readability** - Variable naming, function structure, overall maintainability

The AI grading agent analyzes student submissions from GitHub repositories against custom rubrics, providing detailed feedback on these qualitative aspects of code quality. This allows TAs to focus on higher-level educational interactions while ensuring consistent, comprehensive feedback on coding style and form.

## Prerequisites

### Installing Python 3.12

**macOS:**
```bash
# Using Homebrew
brew install python@3.12
```
*Alternative:* Download and install from [python.org](https://www.python.org/downloads/)

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv
```
*Alternative:* Download and install from [python.org](https://www.python.org/downloads/)

**Windows:**
Download and install from [python.org](https://www.python.org/downloads/)

### Installing Node.js and npm

**macOS:**
```bash
# Using Homebrew
brew install node
```
*Alternative:* Download and install from [nodejs.org](https://nodejs.org/)

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```
*Alternative:* Download and install from [nodejs.org](https://nodejs.org/)

**Windows:**
Download and install from [nodejs.org](https://nodejs.org/)

### Installing Git

**macOS:**
```bash
# Using Homebrew
brew install git
```
*Alternative:* Download and install from [git-scm.com](https://git-scm.com/)

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install git
```
*Alternative:* Download and install from [git-scm.com](https://git-scm.com/)

**Windows:**
Download and install from [git-scm.com](https://git-scm.com/)

### Installing Visual Studio Code

**macOS:**
```bash
# Using Homebrew
brew install --cask visual-studio-code
```
*Alternative:* Download and install from [code.visualstudio.com](https://code.visualstudio.com/)

**Linux (Ubuntu/Debian):**
```bash
# Download and install the .deb package
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code
```
*Alternative:* Download and install from [code.visualstudio.com](https://code.visualstudio.com/)

**Windows:**
Download and install from [code.visualstudio.com](https://code.visualstudio.com/)

> **Note:** After installing these prerequisites, you may want to restart your computer to ensure all programs are properly loaded in your system PATH and available in your terminal.

## Backend Setup

### 1. Create Python Virtual Environment

```bash
# Create virtual environment with Python 3.12
python3.12 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root with these variables:

```bash
# Your Azure OpenAI API key (found in Keys and Endpoint section)
AZURE_OPENAI_API_KEY="your-api-key"

# Your Azure OpenAI endpoint URL
AZURE_OPENAI_ENDPOINT=https://azureaiapi.cloud.unc.edu

# Your model deployment name
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# API version
AZURE_OPENAI_API_VERSION=2024-10-21
```

### 4. Run FastAPI Server

```bash
# Start the server with auto-reload
uvicorn main:app --reload

# Or run directly
python main.py
```

The API will be available at `http://localhost:8000`

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Frontend Setup

### 1. Navigate to Frontend Directory

```bash
cd frontend/agent
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Start Development Server

```bash
npm start
```

The frontend will be available at `http://localhost:3000`

### Frontend Input Parameters

The frontend accepts the following inputs for grading submissions:

#### GitHub Repository Link
- **Type:** String (URL)
- **Required:** Yes
- **Format:** `https://github.com/username/repository.git`
- **Description:** The GitHub repository URL containing the student's code to be graded

> **⚠️ Important:** The repository must be **public** for the system to access and clone it. If working with a private repository, you can fork it and change the fork's visibility to public, or temporarily make the original repository public during grading.

#### Rubric JSON Object
The rubric is a JSON object with the following attributes:

**`batches`** (Array of Arrays)
- **Type:** `string[][]`
- **Required:** Yes
- **Description:** A 2D array where each sub-array contains file names to be graded together in one batch
- **Example:** 
  ```json
  [
    ["animal_v1_basic.py"],
    ["animal_v2_verbose.py"],
    ["animal_v3_functional.py"]
  ]
  ```

**`totalPoints`** (Number)
- **Type:** `integer`
- **Required:** Yes
- **Description:** The total possible points for the entire assignment
- **Example:** `6`

**`rubric`** (String)
- **Type:** `string`
- **Required:** Yes
- **Description:** A text description of the grading criteria with point values
- **Example:** 
  ```
  "RUBRIC: Total possible points: 6 Each question is 1 point NO PARTIAL CREDIT: 
  _/1: Docstrings are used for both classes and functions Score, 
  _/1: All variables are descriptive and not too short (like a or b), 
  _/1: All functions specify the input parameter type and return type, 
  _/1: At least either the parent or child class has an init method, 
  _/1: No redundant or duplicated code, 
  _/1: No immediate syntax errors"
  ```

**Complete Rubric Example** (see `sampleRubric.json`):
```json
{
  "batches": [
    ["animal_v1_basic.py"],
    ["animal_v2_verbose.py"],
    ["animal_v3_functional.py"]
  ],
  "totalPoints": 6,
  "rubric": "RUBRIC: Total possible points: 6 Each question is 1 point NO PARTIAL CREDIT: _/1: Docstrings are used for both classes and functions Score, _/1: All variables are descriptive and not too short (like a or b), _/1: All functions specify the input parameter type and return type, _/1: At least either the parent or child class has an init method, _/1: No redundant or duplicated code, _/1: No immediate syntax errors"
}
```

#### Test Results (Optional)
- **Type:** String
- **Required:** No
- **Description:** Optional test results or additional context to include in grading
- **Example:** `"All tests passed"` or `"5/6 tests passed, 1 timeout"`

### Testing the Application

You can test the application using the following sample data:

**Test GitHub Repository:**
```
https://github.com/ayushTheunc/comp523testrepo
```

**Test Rubric:**
Use the contents from `sampleRubric.json` in the project root, which includes:
- File batches: `["animal_v1_basic.py"]`, `["animal_v2_verbose.py"]`, `["animal_v3_functional.py"]`
- Total points: 6
- Grading criteria for docstrings, variable naming, type annotations, init methods, code redundancy, and syntax

Simply copy the JSON from `sampleRubric.json` and paste it into the frontend rubric field, then use the test GitHub link above.

## API Usage

### Endpoints

- `GET /` - API status
- `GET /health` - Health check
- `POST /grade` - Grade a code submission

### Example API Request

```bash
curl -X POST "http://localhost:8000/grade" \
  -H "Content-Type: application/json" \
  -d '{
    "github_link": "https://github.com/username/repo.git",
    "rubric": {
      "batches": [
        ["file1.py"],
        ["file2.py"],
        ["file3.py"]
      ],
      "totalPoints": 6,
      "rubric": "RUBRIC: Total possible points: 6..."
    },
    "test_results": "All tests passed"
  }'
```

### Example Response

```json
{
  "success": true,
  "analysis": [
    {
      "rubric_score": "4/6",
      "hundred_point_score": 67,
      "review": "Criterion 1 (1/1 points): Docstrings present...",
      "file_name": ["file1.py"]
    }
  ],
  "error": null
}
```

## Project Structure

```
├── main.py                    # FastAPI application entry point
├── services/
│   └── agent_service.py       # Core grading logic with Azure OpenAI
├── models/
│   └── models.py              # Pydantic models for API validation
├── frontend/
│   └── agent/                 # React frontend application
│       ├── src/
│       ├── public/
│       └── package.json
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
└── README.md
```

## Troubleshooting

**Service Unavailable Error:**
- Verify all environment variables are set in `.env`
- Check Azure OpenAI API key and endpoint are correct
- Ensure deployment name matches your Azure resource

**Import Errors:**
- Activate virtual environment: `source venv/bin/activate`
- Run `pip install -r requirements.txt`

**Python Version Issues:**
- Ensure Python 3.12 is installed: `python --version`
- Recreate virtual environment if needed

**CORS Errors:**
- Backend is configured to accept requests from `localhost:3000`
- For production, update `allow_origins` in `main.py`

**Frontend Connection Issues:**
- Ensure backend is running on `http://localhost:8000`
- Check API base URL in frontend configuration
