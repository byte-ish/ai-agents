from app.agents.langgraph_code_assistant import code_assistant_agent as langgraph_agent
from app.agents.langchain_code_assistant_agent import get_agent as normal_agent
from app.configs.settings import AGENT_TYPE
from app.utils.logger import logger


def get_selected_agent():
    """
    Returns the selected agent instance based on AGENT_TYPE configuration.

    Supported agent types:
    - langgraph: Async LangGraph-based agent (recommended for complex use cases and async tools)
    - normal: Simple LangChain-based agent (recommended for simple synchronous scenarios)

    Raises:
        ValueError: If an unsupported AGENT_TYPE is configured.
    """

    logger.info(f"Agent selection triggered based on AGENT_TYPE='{AGENT_TYPE}'")

    if AGENT_TYPE == "langgraph":
        logger.info("Selected agent: LangGraph Agent (Async)")
        return langgraph_agent

    elif AGENT_TYPE == "normal":
        logger.info("Selected agent: LangChain Agent (Sync)")
        return normal_agent()

    else:
        error_message = f"Unsupported AGENT_TYPE configured: {AGENT_TYPE}"
        logger.error(error_message)
        raise ValueError(error_message)