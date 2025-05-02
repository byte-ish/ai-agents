from langchain.tools import tool
from app.chains.performance_optimization_chain import run_performance_optimization_pipeline
from app.utils.logger import logger
from app.utils.markdown_logger import save_tool_output


@tool
def performance_optimizer(code: str) -> str:
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

    result = run_performance_optimization_pipeline(code)

    output = ["## === PERFORMANCE OPTIMIZATION REPORT ===\n"]

    for step in result["optimization_steps"]:
        output.append(f"--- {step['step']} ---\n")
        output.append(step['optimized_code'])
        output.append("\n")

    output.append("## === FINAL OPTIMIZED CODE ===\n")
    output.append(result["final_code"])
    final_output = "\n".join(output)
    # --- SAVE TO MARKDOWN ---
    save_tool_output("performance_optimizer", code, final_output)

    return final_output
