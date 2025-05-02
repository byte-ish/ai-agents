from app.tools.code_reviewer_tool import code_reviewer
from app.tools.performance_optimizer_tool import performance_optimizer
from app.tools.unit_test_generator_tool import unit_test_generator


def all_tools():
    """
    Returns all tools available in the system.
    Add new tools here and they will be automatically available in the agent.
    """
    return [
        code_reviewer,
        performance_optimizer,
        unit_test_generator
        # Add more tools here in future
    ]