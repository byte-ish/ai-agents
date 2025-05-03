# app/tools/code_reviewer_tool.py

from langchain_core.tools import tool
from app.utils.logger import logger
from app.utils.markdown_logger import save_tool_output
import asyncio

from app.chains.code_review_chain import run_code_review_pipeline

@tool
async def code_reviewer(code: str) -> str:
    """
    Reviews source code for:
    - Coding standards
    - Best practices
    - Security vulnerabilities
    - Performance smells
    - Final polishing

    Provide the source code as input. Returns the reviewed and improved code with summary.
    """

    logger.info("Code Reviewer Tool invoked.")

    result = await asyncio.to_thread(run_code_review_pipeline, code)

    output = ["## === CODE REVIEW REPORT ===\n"]
    for step in result["review_steps"]:
        output.append(f"## --- {step['step']} ---\n{step['reviewed_code']}\n")
    output.append("## === FINAL REVIEWED CODE ===\n")
    output.append(result["final_code"])

    final_output = "\n".join(output)

    await asyncio.to_thread(save_tool_output, "code_reviewer", code, final_output)

    return final_output