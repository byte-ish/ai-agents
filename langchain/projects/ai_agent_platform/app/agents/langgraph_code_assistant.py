import asyncio
from typing import TypedDict, Optional
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from app.tools.tool_registry import all_tools, tool_map, tool_metadata
from app.llm.llm_provider import get_llm
from app.utils.markdown_logger import save_tool_output
from app.utils.logger import logger


# ---------------------------
# Define Agent State
# ---------------------------

class AgentState(TypedDict, total=False):
    input: str
    tool_to_use: Optional[str]
    output: Optional[str]


# ---------------------------
# Load tools and LLM
# ---------------------------

tools = all_tools()
llm = get_llm()

logger.info(f"Loaded {len(tools)} tools into LangGraph agent.")


# ---------------------------
# Planner Node
# ---------------------------

def get_tool_descriptions() -> str:
    """
    Builds tool descriptions for planner prompt.
    """
    tools_meta = tool_metadata()
    desc_lines = []
    for tool in tools_meta:
        desc_lines.append(f"- {tool.name} → {tool.description.strip()}")
    return "\n".join(desc_lines)

planner_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a planner. Your job is to decide which tool (if any) to use based on the user input.

Available tools:

{tool_descriptions}

If no tool applies → reply exactly with "none".

IMPORTANT:
- Only respond with the tool name (exact name above) or "none".
- No explanations.
"""),
    ("human", "{input}")
])

planner_chain = planner_prompt | llm


async def planner_node(state: AgentState) -> AgentState:
    user_input = state["input"]
    tool_descriptions = get_tool_descriptions()

    logger.info(f"[Planner] User input → {user_input}")

    response = await planner_chain.ainvoke({
        "input": user_input,
        "tool_descriptions": tool_descriptions
    })

    tool_name = str(response).strip()

    if tool_name == "none" or tool_name not in tool_map():
        logger.info("[Planner] No tool selected.")
        tool_name = None
    else:
        logger.info(f"[Planner] Selected tool → {tool_name}")

    return {
        "input": user_input,
        "tool_to_use": tool_name
    }


# ---------------------------
# Tool Executor Node
# ---------------------------

async def tool_node(state: AgentState) -> AgentState:
    user_input = state["input"]
    tool_name = state["tool_to_use"]

    if tool_name:
        tool = tool_map()[tool_name]

        logger.info(f"[Tool Executor] Running tool → {tool_name}")

        # Run the tool async
        result = await tool.ainvoke({"code": user_input})

        # Save to markdown (async safe version → already handled by tool internally or use asyncio if needed)
        # await asyncio.to_thread(save_tool_output, tool_name, user_input, result)

        return {
            "input": user_input,
            "tool_to_use": tool_name,
            "output": result
        }

    else:
        fallback_output = f"No valid tool found for input. User said:\n\n{user_input}"
        logger.info("[Tool Executor] No valid tool. Returning fallback output.")

        await save_tool_output("agent_response", user_input, fallback_output)

        return {
            "input": user_input,
            "tool_to_use": "none",
            "output": fallback_output
        }


# ---------------------------
# Build LangGraph
# ---------------------------

graph = StateGraph(AgentState)

graph.add_node("planner", planner_node)
graph.add_node("tool_executor", tool_node)

graph.add_edge("planner", "tool_executor")
graph.add_edge("tool_executor", END)

graph.set_entry_point("planner")

# Compile the graph to use as agent
code_assistant_agent = graph.compile()

logger.info("LangGraph Code Assistant Agent is ready.")