"""
Pydantic models for API request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, Union, List, Any


class GradeRequest(BaseModel):
    """Request model for grading submission."""
    github_link: str = Field(..., description="The github link of the students code", min_length=1)
    rubric: dict = Field(..., description="The grading rubric text", min_length=1)
    test_results: Optional[str] = Field(None, description="Optional test results to include in grading")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "github_link": "https://github.com/whatever.git",
                    "rubric": {
                        "batches" : ["code1.py", "code2.py"],
                        "rubric" : "grade this like you mean it",
                        "total_points" : 100
                    },
                    "test_results": "All tests passed"
                }
            ]
        }
    }


class GradeResponse(BaseModel):
    """Response model for grading results."""
    success: bool = Field(..., description="Whether the grading was successful")
    analysis: list[Any] = Field(..., description="The detailed grading analysis from AI (string or list of batch results)")
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