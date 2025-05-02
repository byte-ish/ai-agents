from langchain.tools import tool
from app.chains.unit_test_generation_chain import run_unit_test_generation_pipeline
from app.utils.logger import logger
from app.utils.markdown_logger import save_tool_output


@tool
def unit_test_generator(code: str) -> str:
    """
    Generates unit test cases for the provided source code.
    Covers positive, negative and edge cases and returns a complete unittest class code.
    """

    logger.info("Unit Test Generator Tool invoked.")

    result = run_unit_test_generation_pipeline(code)

    output = ["## === UNIT TEST GENERATION REPORT ===\n"]

    for step in result["test_generation_steps"]:
        output.append(f"--- {step['step']} ---\n")
        output.append(step['generated_code'])
        output.append("\n")

    output.append("## === FINAL UNIT TEST CODE ===\n")
    output.append(result["final_code"])

    final_output = "\n".join(output)

    # --- SAVE TO MARKDOWN ---
    save_tool_output("unit_test_generator", code, final_output)

    return final_output
