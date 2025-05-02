from app.agents.langgraph_code_assistant import code_assistant_agent as langgraph_agent
from app.agents.code_assistant_agent import get_agent as normal_agent
from app.configs.settings import AGENT_TYPE


def get_selected_agent():
    """
    Based on AGENT_TYPE config, returns agent instance.
    """
    if AGENT_TYPE == "langgraph":
        return langgraph_agent
    elif AGENT_TYPE == "normal":
        return normal_agent()
    else:
        raise ValueError(f"Unsupported AGENT_TYPE configured: {AGENT_TYPE}")
