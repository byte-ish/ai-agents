from langchain_core.tools import RunnableTool
from app.utils.logger import logger
from app.utils.markdown_logger import save_tool_output

async def your_tool_name_here(code: str) -> str:
    """
    Description of your tool here.

    - Explain what this tool does.
    - Mention expected input and output.
    """

    logger.info("Your Tool invoked.")

    # ---- your implementation here ----
    result = f"Processed code: {code}"

    # Save to markdown log
    save_tool_output("your_tool_name_here", code, result)

    return result

your_tool = RunnableTool.from_function(
    your_tool_name_here,
    name="your_tool_name_here",
    description="Description of your tool here.\n\n- Explain what this tool does.\n- Mention expected input and output."
)