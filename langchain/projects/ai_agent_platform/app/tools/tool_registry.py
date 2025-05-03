import importlib
import pkgutil
import inspect
import logging
from typing import List, Dict, Optional

from langchain.tools import BaseTool

logger = logging.getLogger("tool_registry")


class ToolInfo:
    """
    Metadata holder for each tool.
    """

    def __init__(self, name: str, description: str, tags: Optional[List[str]], tool_obj: BaseTool, is_async: bool):
        self.name = name
        self.description = description
        self.tags = tags or []
        self.tool = tool_obj
        self.is_async = is_async

    def __repr__(self):
        return f"ToolInfo(name={self.name}, async={self.is_async}, description={self.description}, tags={self.tags})"


class ToolRegistry:
    """
    Discovers and registers all tools in the tools module and provides metadata.
    """

    def __init__(self, package: str = "app.tools"):
        self.package = package
        self.tools: Dict[str, ToolInfo] = {}

    def discover_tools(self) -> None:
        """
        Scans the tools package and auto-discovers all tools (RunnableTool, StructuredTool, etc)
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

            for name, obj in inspect.getmembers(module):

                if isinstance(obj, BaseTool):

                    description = obj.description or "No description available"
                    tags = getattr(obj, "tags", [])

                    # --- Safe Async Detection ---
                    is_async = self._is_async_tool(obj)

                    # Register tool
                    self.tools[obj.name] = ToolInfo(obj.name, description, tags, obj, is_async)
                    logger.info(f"Registered tool: {obj.name} | Async: {is_async} | Tags: {tags}")

    def _is_async_tool(self, tool: BaseTool) -> bool:
        """
        Detect if tool supports async execution safely.
        """
        if hasattr(tool, "acall") and inspect.iscoroutinefunction(tool.acall):
            return True
        if inspect.iscoroutinefunction(tool.invoke):
            return True
        return False

    def get_all_tools(self) -> List[BaseTool]:
        """
        Returns all registered tool objects.
        """
        return [tool_info.tool for tool_info in self.tools.values()]

    def get_tool_by_name(self, name: str) -> Optional[BaseTool]:
        """
        Get a single tool by name.
        """
        tool_info = self.tools.get(name)
        return tool_info.tool if tool_info else None

    def get_tool_metadata(self) -> List[ToolInfo]:
        """
        Get all tool metadata.
        """
        return list(self.tools.values())

    def get_tool_map(self) -> Dict[str, BaseTool]:
        """
        Get mapping of tool name → tool object
        """
        return {name: info.tool for name, info in self.tools.items()}


# --- Singleton Registry ---
tool_registry = ToolRegistry()
tool_registry.discover_tools()


# --- Public Accessors ---
def all_tools() -> List[BaseTool]:
    return tool_registry.get_all_tools()


def tool_map() -> Dict[str, BaseTool]:
    return tool_registry.get_tool_map()


def tool_metadata() -> List[ToolInfo]:
    return tool_registry.get_tool_metadata()