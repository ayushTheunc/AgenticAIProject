"""
Pytest tests for main.py FastAPI application
Tests the /grade endpoint and error handling
"""

import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def valid_grade_request():
    """Sample valid grade request data."""
    return {
        "github_link": "https://github.com/test/repo.git",
        "rubric": {
            "batches": [["code1.py", "code2.py"]],
            "rubric": "Grade based on code quality and structure",
            "total_points": 100
        },
        "test_results": "All tests passed"
    }


@pytest.fixture
def mock_agent_service():
    """Mock the agent service to avoid actual API calls."""
    with patch('main.grading_service') as mock_service:
        mock_service.return_value = MagicMock()
        yield mock_service


class TestGradeEndpoint:
    """Tests for the /grade endpoint."""
    
    def test_grade_endpoint_success_single_batch(self, client, valid_grade_request):
        """Test successful grading with a single batch."""
        mock_result = [{
            "batch_number": 1,
            "files_analyzed": ["code1.py", "code2.py"],
            "rubric_score": "85/100",
            "hundred_point_score": 85,
            "review": "Good code structure with minor improvements needed"
        }]
        
        with patch('main.agent_service_function', return_value=mock_result):
            response = client.post("/grade", json=valid_grade_request)
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["error"] is None
            assert len(data["analysis"]) == 1
            assert data["analysis"][0]["rubric_score"] == "85/100"
    
    def test_grade_endpoint_success_multiple_batches(self, client, valid_grade_request):
        """Test successful grading with multiple batches."""
        valid_grade_request["rubric"]["batches"] = [
            ["code1.py"],
            ["code2.py", "code3.py"]
        ]
        
        mock_result = [
            {
                "batch_number": 1,
                "files_analyzed": ["code1.py"],
                "rubric_score": "90/100",
                "hundred_point_score": 90,
                "review": "Excellent work"
            },
            {
                "batch_number": 2,
                "files_analyzed": ["code2.py", "code3.py"],
                "rubric_score": "80/100",
                "hundred_point_score": 80,
                "review": "Good effort"
            }
        ]
        
        with patch('main.agent_service_function', return_value=mock_result):
            response = client.post("/grade", json=valid_grade_request)
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert len(data["analysis"]) == 2
    
    def test_grade_endpoint_without_test_results(self, client, valid_grade_request):
        """Test grading without optional test results."""
        del valid_grade_request["test_results"]
        
        mock_result = [{
            "batch_number": 1,
            "rubric_score": "75/100",
            "hundred_point_score": 75,
            "review": "Satisfactory"
        }]
        
        with patch('main.agent_service_function', return_value=mock_result):
            response = client.post("/grade", json=valid_grade_request)
            
            assert response.status_code == 200
            assert response.json()["success"] is True
    
    def test_grade_endpoint_invalid_github_link(self, client, valid_grade_request):
        """Test with invalid GitHub link."""
        valid_grade_request["github_link"] = ""
        
        response = client.post("/grade", json=valid_grade_request)
        
        assert response.status_code == 422
    
    def test_grade_endpoint_missing_rubric(self, client, valid_grade_request):
        """Test with missing rubric."""
        del valid_grade_request["rubric"]
        
        response = client.post("/grade", json=valid_grade_request)
        
        assert response.status_code == 422 
    
    def test_grade_endpoint_service_unavailable(self, client, valid_grade_request):
        """Test when grading service is not initialized."""
        with patch('main.grading_service', None):
            response = client.post("/grade", json=valid_grade_request)
            
            assert response.status_code == 503
            assert "not initialized" in response.json()["detail"]
    
    def test_grade_endpoint_agent_service_exception(self, client, valid_grade_request):
        """Test when agent_service_function raises an exception."""
        with patch('main.agent_service_function', side_effect=Exception("Service error")):
            response = client.post("/grade", json=valid_grade_request)
            
            assert response.status_code == 500
            assert "unexpected error" in response.json()["detail"].lower()
    
    def test_grade_endpoint_returns_error_dict(self, client, valid_grade_request):
        """Test when agent_service returns an error dictionary."""
        mock_result = {
            "success": False,
            "error": "Failed to clone repository",
            "analysis": []
        }
        
        with patch('main.agent_service_function', return_value=mock_result):
            response = client.post("/grade", json=valid_grade_request)
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is False
            assert data["error"] == "Failed to clone repository"
    
    def test_grade_endpoint_with_special_characters_in_rubric(self, client, valid_grade_request):
        """Test with special characters in rubric text."""
        valid_grade_request["rubric"]["rubric"] = "Grade with 100% accuracy! Check: \n- Quality\n- Style"
        
        mock_result = [{
            "batch_number": 1,
            "rubric_score": "88/100",
            "hundred_point_score": 88,
            "review": "Good work"
        }]
        
        with patch('main.agent_service_function', return_value=mock_result):
            response = client.post("/grade", json=valid_grade_request)
            
            assert response.status_code == 200
            assert response.json()["success"] is True
    
    def test_grade_endpoint_large_batch_array(self, client, valid_grade_request):
        """Test with a large number of batches."""
        valid_grade_request["rubric"]["batches"] = [
            [f"code{i}.py"] for i in range(10)
        ]
        
        mock_result = [
            {
                "batch_number": i,
                "rubric_score": f"{80+i}/100",
                "hundred_point_score": 80+i,
                "review": f"Batch {i} review"
            }
            for i in range(1, 11)
        ]
        
        with patch('main.agent_service_function', return_value=mock_result):
            response = client.post("/grade", json=valid_grade_request)
            
            assert response.status_code == 200
            data = response.json()
            assert len(data["analysis"]) == 10

class TestRequestValidation:
    """Tests for request validation using Pydantic models."""
    
    def test_invalid_json_format(self, client):
        """Test with invalid JSON format."""
        response = client.post(
            "/grade",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_extra_fields_ignored(self, client, valid_grade_request):
        """Test that extra fields in request are handled properly."""
        valid_grade_request["extra_field"] = "should be ignored"
        
        mock_result = [{"batch_number": 1, "rubric_score": "80/100"}]
        
        with patch('main.agent_service_function', return_value=mock_result):
            response = client.post("/grade", json=valid_grade_request)
            
            assert response.status_code == 200
    
    def test_null_values_in_optional_fields(self, client, valid_grade_request):
        """Test with null values in optional fields."""
        valid_grade_request["test_results"] = None
        
        mock_result = [{"batch_number": 1, "rubric_score": "80/100"}]
        
        with patch('main.agent_service_function', return_value=mock_result):
            response = client.post("/grade", json=valid_grade_request)
            
            assert response.status_code == 200
