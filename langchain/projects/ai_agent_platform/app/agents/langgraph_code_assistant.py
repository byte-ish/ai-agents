from typing import TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from app.tools import all_tools
from app.llm.llm_provider import get_llm
from app.utils.markdown_logger import save_tool_output


# ---------------------------
# Define Agent State properly
# ---------------------------

class AgentState(TypedDict, total=False):
    input: str
    tool_to_use: str
    output: str


# ---------------------------
# Load tools and LLM
# ---------------------------

tools = all_tools()
tool_map = {tool.name: tool for tool in tools}

llm = get_llm()

# ---------------------------
# Planner Node
# ---------------------------

planner_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a planner. Decide which tool to use based on user input. Available tools: {tool_names}. Respond ONLY with tool name."),
    ("human", "{input}")
])

planner_chain = planner_prompt | llm

def planner_node(state: AgentState) -> AgentState:
    user_input = state["input"]
    tool_names = ", ".join(tool_map.keys())

    response = planner_chain.invoke({
        "input": user_input,
        "tool_names": tool_names
    })

    # FIXED → make sure response is safely treated as string
    tool_name = str(response).strip()

    if tool_name not in tool_map:
        tool_name = None

    return {
        "input": user_input,
        "tool_to_use": tool_name
    }


# ---------------------------
# Tool Executor Node
# ---------------------------

def tool_node(state: AgentState) -> AgentState:
    user_input = state["input"]
    tool_name = state["tool_to_use"]

    if tool_name:
        tool = tool_map[tool_name]
        result = tool.invoke({"code": user_input})
        save_tool_output(tool_name, user_input, result)

        return {
            "input": user_input,
            "tool_to_use": tool_name,
            "output": result
        }

    else:
        output = f"No valid tool found for input. User said:\n\n{user_input}"
        save_tool_output("agent_response", user_input, output)

        return {
            "input": user_input,
            "tool_to_use": "none",
            "output": output
        }


# ---------------------------
# Define Graph and Compile
# ---------------------------

graph = StateGraph(AgentState)

graph.add_node("planner", planner_node)
graph.add_node("tool_executor", tool_node)

graph.add_edge("planner", "tool_executor")
graph.add_edge("tool_executor", END)

graph.set_entry_point("planner")

code_assistant_agent = graph.compile()