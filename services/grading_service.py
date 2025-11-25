"""
Grading Service Module
Handles the core grading logic using Azure OpenAI
"""

import os
from typing import Optional
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate


class GradingService:
    """Service for grading code submissions using Azure OpenAI."""
    
    def __init__(self):
        """Initialize the grading service with Azure OpenAI configuration."""
        load_dotenv()
        
        # Validate environment variables
        required_vars = [
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT", 
            "AZURE_OPENAI_DEPLOYMENT_NAME"
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                "Please set these in your .env file."
            )
        
        # Initialize Azure OpenAI client
        self.llm = AzureChatOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
            temperature=0
        )
        
        # Define the prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["code", "rubric", "tests"],
            template="""
You are a strict grader. 
Grade the following Python code according to the rubric.

Rubric:
{rubric}

Student's Code:
{code}

{tests}

Provide a detailed analysis for each criterion in the rubric, assign points, and calculate the total score.
"""
        )
    
    async def grade_submission(
        self, 
        code: str, 
        rubric: str, 
        test_results: Optional[str] = None
    ) -> dict:
        """
        Grade a code submission based on the provided rubric.
        
        Args:
            code: The student's code submission
            rubric: The grading rubric text
            test_results: Optional test results to include in grading
            
        Returns:
            dict: Contains 'success' (bool), 'analysis' (str), and optionally 'error' (str)
        """
        try:
            # Format the prompt
            tests_section = f"Test Results:\n{test_results}" if test_results else ""
            prompt = self.prompt_template.format(
                code=code,
                rubric=rubric,
                tests=tests_section
            )
            
            # Call Azure OpenAI
            response = self.llm.invoke(prompt)
            
            if response and hasattr(response, 'content'):
                return {
                    "success": True,
                    "analysis": response.content
                }
            else:
                return {
                    "success": False,
                    "error": "No response received from Azure OpenAI",
                    "analysis": ""
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error during grading: {str(e)}",
                "analysis": ""
            }
