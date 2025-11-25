"""
Pydantic models for API request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional


class GradeRequest(BaseModel):
    """Request model for grading submission."""
    code: str = Field(..., description="The student's code submission", min_length=1)
    rubric: str = Field(..., description="The grading rubric text", min_length=1)
    test_results: Optional[str] = Field(None, description="Optional test results to include in grading")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": "def hello():\n    print('Hello, World!')",
                    "rubric": "Grade based on: 1) Function exists 2) Prints correctly",
                    "test_results": "All tests passed"
                }
            ]
        }
    }


class GradeResponse(BaseModel):
    """Response model for grading results."""
    success: bool = Field(..., description="Whether the grading was successful")
    analysis: str = Field(..., description="The detailed grading analysis from AI")
    error: Optional[str] = Field(None, description="Error message if grading failed")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": True,
                    "analysis": "CRITERION 1: Class Structure Requirements (15/20 points)...",
                    "error": None
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")