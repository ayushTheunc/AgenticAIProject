import subprocess, json, os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()

# ----------------------------
# 1. Load rubric from file
# ----------------------------
with open("sample.txt", "r") as f:
    rubric_text = f.read()

# ----------------------------
# 2. Load student submission
# ----------------------------
with open("sampleCode.py", "r") as f:
    student_code = f.read()

# ----------------------------
# 3. Run unit tests
# ----------------------------
# def run_tests(file_path: str):
#     try:
#         result = subprocess.run(
#             ["pytest", file_path],
#             capture_output=True,
#             text=True,
#             timeout=10
#         )
#         return result.stdout
#     except Exception as e:
#         return str(e)

# test_results = run_tests("student_submission.py")

# ----------------------------
# 4. Build grading prompt
# ----------------------------
# rubric_text is already loaded from sample.txt above

prompt_template = PromptTemplate(
    input_variables=["code", "rubric", "tests"],
    template="""
You are a strict grader. 
Grade the following Python code according to the rubric.

Rubric:
{rubric}

Student's Code:
{code}



"""
)

# ----------------------------
# 5. Configure and call Azure OpenAI
# ----------------------------

# Check for required environment variables
required_vars = [
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_ENDPOINT", 
    "AZURE_OPENAI_DEPLOYMENT_NAME"
]

missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
    print("Please set these in your .env file:")
    print("- AZURE_OPENAI_API_KEY: Your Azure OpenAI API key")
    print("- AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint URL")
    print("- AZURE_OPENAI_DEPLOYMENT_NAME: Your model deployment name")
    print("- AZURE_OPENAI_API_VERSION: API version (optional, defaults to 2024-10-21)")
    exit(1)

try:
    
    # Initialize Azure OpenAI
    llm = AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        temperature=0
    )

    prompt = prompt_template.format(
        code=student_code, rubric=rubric_text, tests="")

    print("Analyzing code with Azure OpenAI...")
    print("This may take a moment...")
    
    response = llm.invoke(prompt)

except Exception as e:
    print(f"Error calling Azure OpenAI: {str(e)}")
    print("\nPossible issues:")
    print("1. Check your API key and endpoint are correct")
    print("2. Verify your deployment name matches your Azure resource")
    print("3. Ensure you have sufficient quota/credits")
    print("4. Check if your Azure resource is active")
    exit(1)

# ----------------------------
# 6. Display results
# ----------------------------

if response and hasattr(response, 'content'):
    print("\n" + "="*60)
    print("AZURE OPENAI CODE ANALYSIS RESULTS")
    print("="*60)
    print(response.content)
    print("\n" + "="*60)
    print("Analysis completed successfully!")
else:
    print("Error: No response received from Azure OpenAI")
    print("Raw response:", response)