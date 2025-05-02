from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.llm.llm_provider import get_llm

# Define the reusable markdown guidelines
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

UNIT_TEST_STEPS = [
    ("Identify Testable Functions", f"""
Analyze the following code and identify the functions or methods that can be unit tested.

CODE:
{{code}}

{MARKDOWN_GUIDELINES}
"""),

    ("Generate Positive Test Cases", f"""
Based on the identified testable functions, generate positive test cases.

CODE:
{{code}}

{MARKDOWN_GUIDELINES}
"""),

    ("Generate Negative Test Cases", f"""
Generate negative test cases where input is invalid or exceptions should be handled.

CODE:
{{code}}

{MARKDOWN_GUIDELINES}
"""),

    ("Generate Edge Case Test Cases", f"""
Generate edge cases for the functions like empty inputs, maximum inputs, etc.

CODE:
{{code}}

{MARKDOWN_GUIDELINES}
"""),

    ("Finalize Unit Test Code", f"""
Create a full unit test class using unittest module with all positive, negative and edge cases.

CODE:
{{code}}

{MARKDOWN_GUIDELINES}
""")
]

llm = get_llm()
test_generation_chains = []

for step_name, prompt_text in UNIT_TEST_STEPS:
    prompt = PromptTemplate(input_variables=["code"], template=prompt_text)
    chain = LLMChain(llm=llm, prompt=prompt, output_key="code")
    test_generation_chains.append((step_name, chain))


def run_unit_test_generation_pipeline(code_input: str) -> dict:
    from app.utils.logger import logger

    current_code = code_input
    test_generation_report = []

    for step_name, chain in test_generation_chains:
        logger.info(f"Running unit test generation step: {step_name}")
        result = chain.invoke({"code": current_code})
        generated_code = result["code"]

        test_generation_report.append({
            "step": step_name,
            "generated_code": generated_code
        })

        current_code = generated_code

    return {
        "final_code": current_code,
        "test_generation_steps": test_generation_report
    }
