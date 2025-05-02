import asyncio
from langchain.tools import RunnableTool
from app.utils.logger import logger
from app.utils.markdown_logger import save_tool_output

def create_performance_optimizer_tool():
    async def performance_optimizer(code: str) -> str:
        """
        Optimizes source code for performance.
        """

        logger.info("Performance Optimizer Tool invoked.")

        from app.chains.performance_optimization_chain import run_performance_optimization_pipeline
        result = await asyncio.to_thread(run_performance_optimization_pipeline, code)

        output = ["## === PERFORMANCE OPTIMIZATION REPORT ===\n"]
        for step in result["optimization_steps"]:
            output.append(f"--- {step['step']} ---\n")
            output.append(step['optimized_code'])
            output.append("\n")
        output.append("## === FINAL OPTIMIZED CODE ===\n")
        output.append(result["final_code"])
        final_output = "\n".join(output)

        await asyncio.to_thread(save_tool_output, "performance_optimizer", code, final_output)
        return final_output

    return RunnableTool.from_function(
        performance_optimizer,
        name="performance_optimizer",
        description="Optimizes source code performance using multi-step optimizations."
    )