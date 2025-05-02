import asyncio
from langchain.tools import RunnableTool
from app.utils.logger import logger
from app.utils.markdown_logger import save_tool_output

def create_code_reviewer_tool():
    async def code_reviewer(code: str) -> str:
        """
        Reviews source code for:
        - Coding standards
        - Best practices
        - Security vulnerabilities
        - Performance smells
        - Final polishing

        Provide source code as input. Returns reviewed and improved code with summary.
        """
        logger.info("Code Reviewer Tool invoked.")

        from app.chains.code_review_chain import run_code_review_pipeline
        result = await asyncio.to_thread(run_code_review_pipeline, code)

        output = ["## === CODE REVIEW REPORT ===\n"]
        for step in result["review_steps"]:
            output.append(f"--- {step['step']} ---\n")
            output.append(step['reviewed_code'])
            output.append("\n")
        output.append("## === FINAL REVIEWED CODE ===\n")
        output.append(result["final_code"])
        final_output = "\n".join(output)

        await asyncio.to_thread(save_tool_output, "code_reviewer", code, final_output)
        return final_output

    return RunnableTool.from_function(
        code_reviewer,
        name="code_reviewer",
        description="Reviews source code for standards, best practices, security and performance issues."
    )