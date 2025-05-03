# app/tools/performance_optimizer_tool.py

from langchain_core.tools import tool
from app.utils.logger import logger
from app.utils.markdown_logger import save_tool_output
import asyncio

from app.chains.performance_optimization_chain import run_performance_optimization_pipeline

@tool
async def performance_optimizer(code: str) -> str:
    """
    Optimizes source code for performance.

    Applies multi-step optimization:
    - General performance improvements
    - CPU and memory optimizations
    - I/O optimizations
    - Concurrency suggestions
    - Caching/memoization suggestions
    - Final polishing and summary

    Provide the source code as input. Returns optimized code and optimization report.
    """

    logger.info("Performance Optimizer Tool invoked.")

    result = await asyncio.to_thread(run_performance_optimization_pipeline, code)

    output = ["## === PERFORMANCE OPTIMIZATION REPORT ===\n"]
    for step in result["optimization_steps"]:
        output.append(f"## --- {step['step']} ---\n{step['optimized_code']}\n")
    output.append("## === FINAL OPTIMIZED CODE ===\n")
    output.append(result["final_code"])

    final_output = "\n".join(output)

    await asyncio.to_thread(save_tool_output, "performance_optimizer", code, final_output)

    return final_output