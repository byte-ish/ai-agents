import importlib
import pkgutil
import inspect
import logging
from langchain.tools import BaseTool
from typing import List, Dict, Optional, Union

logger = logging.getLogger("tool_registry")


class ToolInfo:
    """
    Metadata holder for each tool.
    """
    def __init__(self, name: str, description: str, tags: Optional[List[str]], tool_obj: BaseTool):
        self.name = name
        self.description = description
        self.tags = tags or []
        self.tool = tool_obj

    def __repr__(self):
        return f"ToolInfo(name={self.name}, description={self.description}, tags={self.tags})"


class ToolRegistry:
    """
    Discovers and registers all tools in the tools module and provides metadata.
    """

    def __init__(self, package: str = "app.tools"):
        self.package = package
        self.tools: Dict[str, ToolInfo] = {}

    def discover_tools(self) -> None:
        """
        Scans the tools package and auto-discovers all tools decorated with @tool or RunnableTool.from_function
        """
        logger.info(f"Discovering tools in package: {self.package}")

        # Import the main tools package
        package = importlib.import_module(self.package)

        # Iterate through all modules
        for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
            if is_pkg:
                continue

            full_module_name = f"{self.package}.{module_name}"
            logger.info(f"Loading module: {full_module_name}")
            module = importlib.import_module(full_module_name)

            # Inspect module for tool objects
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, BaseTool):
                    description = obj.description or "No description available"
                    tags = getattr(obj, "tags", [])  # Optional tags attribute
                    self.tools[obj.name] = ToolInfo(obj.name, description, tags, obj)
                    logger.info(f"Registered tool: {obj.name} with tags: {tags}")

    def get_all_tools(self) -> List[BaseTool]:
        """
        Returns all registered tool objects.
        """
        return [tool_info.tool for tool_info in self.tools.values()]

    def get_tool_by_name(self, name: str) -> Optional[BaseTool]:
        """
        Retrieve a tool by name.
        """
        tool_info = self.tools.get(name)
        return tool_info.tool if tool_info else None

    def get_tool_metadata(self) -> List[ToolInfo]:
        """
        Retrieve metadata for all registered tools.
        """
        return list(self.tools.values())

    def get_tool_map(self) -> Dict[str, BaseTool]:
        """
        Returns a mapping of tool name to tool object.
        """
        return {name: info.tool for name, info in self.tools.items()}


# Singleton registry instance
tool_registry = ToolRegistry()
tool_registry.discover_tools()


# --- Public methods ---

def all_tools() -> List[BaseTool]:
    return tool_registry.get_all_tools()

def tool_map() -> Dict[str, BaseTool]:
    return tool_registry.get_tool_map()

def tool_metadata() -> List[ToolInfo]:
    return tool_registry.get_tool_metadata()