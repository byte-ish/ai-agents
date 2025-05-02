from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

from app.llm.llm_provider import get_llm
from app.tools import all_tools
import os
from app.utils.logger import logger

def get_agent():
    """
    Initializes and returns the AI Agent with all available tools.
    """

    logger.info("Initializing AI Code Assistant Agent...")

    # Initialize LLM (OpenAI assumed here)
    llm = get_llm()

    # Tools - dynamically loaded
    tools = all_tools()

    logger.info(f"Loaded {len(tools)} tools into the agent.")

    # Initialize agent with tools
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )

    return agent


if __name__ == "__main__":
    agent = get_agent()

    # Example multi-query input
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

    result = agent.invoke({
        "input": user_input
    })

    print("\n==== Agent Output ====\n")
    print(result)