#!/usr/bin/env python3
"""
Test script to demonstrate the usage of agentService.py
"""

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
    zip_file_path = "testing-materials.zip"
    rubric_file_path = "rubric2.txt"
    
    # Load zip file as binary data
    zip_repo_data = load_file_as_bytes(zip_file_path)
    
    # Load rubric file as text content
    rubric_text = load_file_as_text(rubric_file_path)
    
    # Define batches
    batch_array = [
        ["organizations.py", "organizationModel.py"],
        ["chatbot.py", "chatMessage.py", "chatSession.py"]
    ]
    
    print("Testing Agent Service Function")
    print("=" * 50)
    print(f"Zip Repository: {len(zip_repo_data)} bytes of data")
    print(f"Rubric: {len(rubric_text)} characters of text")
    print(f"Batch Array: {batch_array}")
    print("=" * 50)
    
    # Call the function with actual data instead of file paths
    result = agent_service_function(zip_repo_data, rubric_text, batch_array)
    
    # Display results
    print("\n" + "=" * 60)
    print("FINAL RESULTS SUMMARY")
    print("=" * 60)
    
    if result["success"]:
        print(f"✅ Success: {result['summary']}")
        print(f"Total Batches: {result['total_batches']}")
        print(f"Successful Batches: {result['successful_batches']}")
        print(f"Failed Batches: {result['failed_batches']}")
        print(f"Total Files Processed: {result['total_files_processed']}")
    else:
        print(f"❌ Error: {result['error']}")
    
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
    test_agent_service()
    
    # Test with sample data to demonstrate interface
    test_with_sample_data()