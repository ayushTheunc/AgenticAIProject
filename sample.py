import subprocess, json
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

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
# 5. Call the LLM
# ----------------------------
llm = Ollama(model="llama3.2", temperature=0)  # Using Ollama from langchain-community

prompt = prompt_template.format(
    code=student_code, rubric=rubric_text, tests="")

response = llm.invoke(prompt)

# ----------------------------
# 6. Parse grade report
# ----------------------------


print(response)