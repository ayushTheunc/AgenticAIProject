# LangChain AI Agent for Python Code Analysis

This project contains a LangChain AI Agent that uses Ollama's Llama 3.2 model to analyze Python files against text-based rubrics.

## Project Structure

```
SemanticKernelNotes/
├── sample.py          # Main analysis script
├── sampleCode.py      # Sample Python code to analyze
├── sample.txt         # Rubric for evaluation
├── venv/             # Virtual environment (created during setup)
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Prerequisites

Before setting up this project, make sure you have:

1. **Python 3.9+** installed on your system
2. **Ollama** installed and running
3. **Llama 3.2 model** pulled in Ollama

### Installing Ollama and Llama 3.2

If you don't have Ollama installed:

```bash
# Install Ollama (macOS)
brew install ollama

# Or download from: https://ollama.ai/download

# Start Ollama service
ollama serve

# Pull Llama 3.2 model (in a new terminal)
ollama pull llama3.2
```

## Setup Instructions


### 1. Create and Activate Virtual Environment

**Option A: Using the existing venv (if available)**
```bash
# Activate the virtual environment
source venv/bin/activate
```

**Option B: Create a new virtual environment**
```bash
# Remove existing venv if present
rm -rf venv

# Create new virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### 2. Make sure Ollama is running

```bash
# In a separate terminal, start Ollama if not already running
ollama serve
```

### 3. Activate virtual environment (if not already active)

```bash
source venv/bin/activate
```

### 4. Run the analysis script

```bash
python sample.py
```

## What the Script Does

1. **Loads rubric** from `sample.txt` (objective grading criteria)
2. **Reads Python code** from `sampleCode.py` (sample student submission)
3. **Connects to Ollama** using Llama 3.2 model
4. **Analyzes code** against the rubric criteria
5. **Returns JSON output** with scores and detailed feedback

## Sample Output

```json
{
  "criteria_scores": [
    {
      "criterion": "Code Structure and Organization",
      "score": 15,
      "max_score": 20,
      "feedback": "Good class hierarchy with clear inheritance..."
    }
  ],
  "total_score": 85,
  "percentage": 85.0,
  "overall_feedback": "Well-structured code with room for improvement..."
}
```

## Customizing the Analysis

### Modify the Rubric (sample.txt)
- Edit `sample.txt` to change evaluation criteria
- Uses objective, measurable criteria (counts classes, methods, docstrings, etc.)
- Each criterion has clear point values (0, 5, 10, 15, 20)

### Analyze Different Code (sampleCode.py)
- Replace `sampleCode.py` with your own Python file
- Or modify the script to accept command-line arguments

### Change the Model
- Edit `sample.py` line with `Ollama(model="llama3.2")`
- Available models: `ollama list`

## Troubleshooting

### Virtual Environment Issues
```bash
# If activation fails
chmod +x venv/bin/activate

# If venv is corrupted, recreate it
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Ollama Connection Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama service
ollama serve

# Check available models
ollama list

# Pull Llama 3.2 if missing
ollama pull llama3.2
```

### Import Errors
```bash
# Reinstall langchain packages
pip uninstall langchain langchain-community langchain-core
pip install langchain langchain-community langchain-core
```

## Deactivating Virtual Environment

When you're done working:

```bash
deactivate
```

