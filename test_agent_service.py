#!/usr/bin/env python3
"""
Test script to demonstrate the usage of agentService.py
"""

import json

from agentService import agent_service_function

def load_file_as_bytes(file_path):
    """Helper function to load a file as bytes."""
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: {file_path} not found, using dummy data")
        return b"dummy zip data"

def load_file_as_text(file_path):
    """Helper function to load a file as text."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: {file_path} not found, using dummy data")
        return "# Dummy Rubric\n\nThis is a sample rubric for testing."

def test_agent_service():
    """Test the agent service function with sample inputs."""
    
    
    
    # Load actual file data instead of using file paths
    github_link = "https://github.com/ayushTheunc/comp523testrepo.git"
    
    with open("rubric.json", 'r', encoding='utf-8') as f:
        rubric = json.load(f)
    
    
    # Call the function with actual data instead of file paths
    result = agent_service_function(github_link, rubric)
    
    # Display results
    
    return result

def test_with_sample_data():
    """Test with hardcoded sample data for demonstration."""
    
    # Sample rubric text
    sample_rubric = """
# FastAPI Repository Evaluation Rubric

## Simple Pass/Fail Criteria for FastAPI Route and Pydantic Model Standards

**Scoring:** Each criterion is either **PASS** ✓ or **FAIL** ✗

## 1. HTTP Method Usage (8 criteria)
- All GET routes only retrieve data (no modifications)
- All POST routes create new resources
- All PUT routes update entire resources
- All DELETE routes remove resources

## 2. Pydantic Models (10 criteria)
- All POST request bodies use Pydantic models
- All PUT request bodies use Pydantic models
- Models use proper type hints
- No raw dictionaries used
    """
    
    # For demo purposes - in real usage you'd have actual zip file bytes
    sample_zip_data = b"PK\x03\x04\x14\x00\x00\x00\x08\x00"  # Partial zip header (dummy data)
    
    batch_array = [
        ["main.py", "models.py"],
        ["routes.py", "utils.py"]
    ]
    
    print("\nTesting with Sample Data")
    print("=" * 50)
    print(f"Sample Rubric Length: {len(sample_rubric)} characters")
    print(f"Sample Zip Data Length: {len(sample_zip_data)} bytes")
    print(f"Batch Array: {batch_array}")
    
    # This will likely fail because the zip data is dummy data,
    # but it demonstrates the correct interface
    try:
        result = agent_service_function(sample_zip_data, sample_rubric, batch_array)
        print("✅ Sample test completed successfully")
        return result
    except Exception as e:
        print(f"❌ Expected error with dummy data: {e}")
        return None

if __name__ == "__main__":
    # Test with actual files if available
    print(test_agent_service())
    
