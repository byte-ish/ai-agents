import os
import logging
from langchain.agents import initialize_agent, AgentType
from app.llm.llm_provider import get_llm
from app.tools.tool_registry import all_tools
from app.utils.logger import logger

# Load tools
tools = all_tools()

logger.info(f"Discovered {len(tools)} tools for AI Agent: {[tool.name for tool in tools]}")

def get_agent():
    """
    Initializes and returns the AI Code Assistant Agent with all registered tools.
    
    This agent uses OpenAI function calling and supports multi-tool selection.
    """
    logger.info("Initializing AI Code Assistant Agent...")

    # Initialize LLM
    llm = get_llm()

    # Initialize agent with all available tools
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )

    logger.info("AI Code Assistant Agent initialized successfully.")

    return agent


if __name__ == "__main__":
    logger.info("Running standalone test for AI Agent.")

    agent = get_agent()

    # Example multi-query input (demonstrates multi tool use)
    user_input = """
Please review this code for best practices and security:

def foo(password):
    print('User password is', password)

Also, optimize this code for performance:

def fetch_data(urls):
    results = []
    for url in urls:
        data = requests.get(url).text
        results.append(data)
    return results
"""

    # Call agent
    result = agent.invoke({
        "input": user_input
    })

    # Output result
    print("\n==== AI Agent Output ====\n")
    print(result)