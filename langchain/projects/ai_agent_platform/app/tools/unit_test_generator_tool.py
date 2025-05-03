# app/tools/unit_test_generator_tool.py

from langchain_core.tools import tool
from app.utils.logger import logger
from app.utils.markdown_logger import save_tool_output
import asyncio

from app.chains.unit_test_generation_chain import run_unit_test_generation_pipeline

@tool
async def unit_test_generator(code: str) -> str:
    """
    Generates unit test cases for the provided source code.
    Covers positive, negative and edge cases and returns a complete unittest class code.
    """

    logger.info("Unit Test Generator Tool invoked.")

    result = await asyncio.to_thread(run_unit_test_generation_pipeline, code)

    output = ["## === UNIT TEST GENERATION REPORT ===\n"]
    for step in result["test_generation_steps"]:
        output.append(f"## --- {step['step']} ---\n{step['generated_code']}\n")
    output.append("## === FINAL UNIT TEST CODE ===\n")
    output.append(result["final_code"])

    final_output = "\n".join(output)

    await asyncio.to_thread(save_tool_output, "unit_test_generator", code, final_output)

    return final_output