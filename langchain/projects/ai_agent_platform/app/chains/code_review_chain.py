from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.llm.llm_provider import get_llm

# Reusable markdown guidelines (same as before)
MARKDOWN_GUIDELINES = """
Please format the entire response properly in Markdown using the following guidelines:

Markdown Guidelines:
- Use clear markdown headers (###, ##)
- Use bullet points and numbered lists
- Use inline code (like `function_name` or `value`) for function names and small values
- Use code blocks only for multi-line code
- Add blank lines between sections for readability
- Make markdown clean and elegant
- Do not add ```markdown in the output
"""

REVIEW_STEPS = [
    ("General Standards Check", f"""
Review the code for coding standards and style:
- Consistent naming
- Proper indentation
- Good comments

CODE:
{{code}}

{MARKDOWN_GUIDELINES}
"""),

    ("Best Practices Check", f"""
Check for best practices:
- Avoid anti-patterns
- Improve readability
- Use proper idioms

CODE:
{{code}}

{MARKDOWN_GUIDELINES}
"""),

    ("Security Vulnerabilities Check", f"""
Review the code for security issues:
- Hardcoded secrets
- Input validation
- Unsafe operations

CODE:
{{code}}

{MARKDOWN_GUIDELINES}
"""),

    ("Performance Smells Check", f"""
Check for performance issues:
- Unnecessary computations
- Inefficient loops

CODE:
{{code}}

{MARKDOWN_GUIDELINES}
"""),

    ("Final Review and Polish", f"""
Final review:
- Clean and readable
- Remove redundant code
- Summary of improvements

CODE:
{{code}}

{MARKDOWN_GUIDELINES}
""")
]

llm = get_llm()
review_chains = []

for step_name, prompt_text in REVIEW_STEPS:
    prompt = PromptTemplate(input_variables=["code"], template=prompt_text)
    chain = LLMChain(llm=llm, prompt=prompt, output_key="code")
    review_chains.append((step_name, chain))

def run_code_review_pipeline(code_input: str) -> dict:
    from app.utils.logger import logger

    current_code = code_input
    review_report = []

    for step_name, chain in review_chains:
        logger.info(f"Running review step: {step_name}")
        result = chain.invoke({"code": current_code})
        reviewed_code = result["code"]

        review_report.append({
            "step": step_name,
            "reviewed_code": reviewed_code
        })

        current_code = reviewed_code

    return {
        "final_code": current_code,
        "review_steps": review_report
    }