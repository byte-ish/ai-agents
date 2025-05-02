from app.agents.langgraph_code_assistant import code_assistant_agent, AgentState

if __name__ == "__main__":
    print("=== Performance Optimization Test via LangGraph Agent ===")

    user_input = """
Please optimize this code to improve CPU and memory usage:

data = []
for i in range(1000000):
    data.append(i)
"""

    result = code_assistant_agent.invoke(AgentState(input=user_input))

    print("\n=== Final Optimized Code ===")
    print(result["output"])