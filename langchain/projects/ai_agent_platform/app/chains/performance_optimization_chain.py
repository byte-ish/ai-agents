from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.llm.llm_provider import get_llm

# Define reusable markdown guidelines
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

PERFORMANCE_STEPS = [
    ("General Code Optimization", f"""
Review the following code and apply general performance improvements:
- Remove redundant operations
- Optimize data structures
- Improve algorithmic efficiency

Provide the improved version only.

CODE:
{{code}}

{MARKDOWN_GUIDELINES}
"""),

    ("CPU and Memory Optimization", f"""
Optimize the following code for CPU and memory usage:
- Avoid repeated calculations
- Optimize loops
- Minimize memory allocation

Provide the improved version only.

CODE:
{{code}}

{MARKDOWN_GUIDELINES}
"""),

    ("I/O Optimization", f"""
Optimize the following code for I/O performance:
- Reduce read/write calls
- Use buffered I/O if applicable
- Optimize network operations

Provide the improved version only.

CODE:
{{code}}

{MARKDOWN_GUIDELINES}
"""),

    ("Concurrency Optimization", f"""
Optimize the following code using concurrency where appropriate:
- Identify independent tasks
- Suggest async / concurrent solutions
- Ensure thread safety

Provide the improved version only.

CODE:
{{code}}

{MARKDOWN_GUIDELINES}
"""),

    ("Caching and Memoization", f"""
Review the following code and suggest caching/memoization where needed:
- Avoid redundant expensive calculations
- Suggest caching where beneficial

Provide the improved version only.

CODE:
{{code}}

{MARKDOWN_GUIDELINES}
"""),

    ("Final Review and Polish", f"""
Perform final review and polishing of the code:
- Ensure readability and maintainability
- Remove any leftover debug code
- Summarize the optimizations applied

Provide the final optimized version and a summary.

CODE:
{{code}}

{MARKDOWN_GUIDELINES}
""")
]

llm = get_llm()
optimization_chains = []

for step_name, prompt_text in PERFORMANCE_STEPS:
    prompt = PromptTemplate(input_variables=["code"], template=prompt_text)
    chain = LLMChain(llm=llm, prompt=prompt, output_key="code")
    optimization_chains.append((step_name, chain))

def run_performance_optimization_pipeline(code_input: str) -> dict:
    from app.utils.logger import logger

    current_code = code_input
    optimization_report = []

    for step_name, chain in optimization_chains:
        logger.info(f"Running performance optimization step: {step_name}")
        result = chain.invoke({"code": current_code})
        optimized_code = result["code"]

        optimization_report.append({
            "step": step_name,
            "optimized_code": optimized_code
        })

        current_code = optimized_code

    return {
        "final_code": current_code,
        "optimization_steps": optimization_report
    }