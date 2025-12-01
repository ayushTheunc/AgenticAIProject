"""
FastAPI Application for AI Code Grading Service
Main API server that accepts code submissions and returns AI-generated grades
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import uvicorn
from models.models import GradeRequest, GradeResponse, HealthResponse
from services.agentService import agent_service_function, AgentService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Code Grading API",
    description="API for grading code submissions using Azure OpenAI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS - adjust origins based on your frontend deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default
        "http://localhost:5173",  # Vite default
        "http://localhost:8080",  # Vue default
        "*"  # Allow all origins (remove in production)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize grading service
try:
    grading_service = AgentService()
    logger.info("Grading service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize grading service: {str(e)}")
    grading_service = None

@app.post("/grade", response_model=GradeResponse, status_code=status.HTTP_200_OK)
async def grade_submission(request: GradeRequest):
    """
    Grade a code submission based on the provided rubric.
    
    Args:
        request: GradeRequest containing code, rubric, and optional test results
        
    Returns:
        GradeResponse with success status, analysis, and optional error message
        
    Raises:
        HTTPException: If grading service is unavailable or validation fails
    """
    # Check if grading service is available
    if grading_service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Grading service is not initialized. Check environment variables."
        )
    
    
    try:
        # Call the grading service
        result = agent_service_function(
            github_link=request.github_link,
            rubric_json=request.rubric,
        )
        
        # Log the result
        if isinstance(result, list):
            logger.info(f"Grading completed successfully for {len(result)} batches")
            return GradeResponse(
                success=True,
                analysis=result,
                error=None
            )
        elif isinstance(result, dict) and not result.get("success", True):
            logger.warning(f"Grading failed: {result.get('error', 'Unknown error')}")
            return GradeResponse(**result)
        else:
            return GradeResponse(
                success=True,
                analysis=result,
                error=None
            )
        
    except Exception as e:
        logger.error(f"Unexpected error during grading: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "analysis": "",
            "error": "An internal server error occurred. Please try again later."
        }
    )


if __name__ == "__main__":
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
