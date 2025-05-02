import asyncio
from langchain.tools import RunnableTool
from app.utils.logger import logger
from app.utils.markdown_logger import save_tool_output

def create_unit_test_generator_tool():
    async def unit_test_generator(code: str) -> str:
        """
        Generates unit test cases for source code.
        """

        logger.info("Unit Test Generator Tool invoked.")

        from app.chains.unit_test_generation_chain import run_unit_test_generation_pipeline
        result = await asyncio.to_thread(run_unit_test_generation_pipeline, code)

        output = ["## === UNIT TEST GENERATION REPORT ===\n"]
        for step in result["test_generation_steps"]:
            output.append(f"--- {step['step']} ---\n")
            output.append(step['generated_code'])
            output.append("\n")
        output.append("## === FINAL UNIT TEST CODE ===\n")
        output.append(result["final_code"])
        final_output = "\n".join(output)

        await asyncio.to_thread(save_tool_output, "unit_test_generator", code, final_output)
        return final_output

    return RunnableTool.from_function(
        unit_test_generator,
        name="unit_test_generator",
        description="Generates unit test cases for positive, negative and edge cases."
    )