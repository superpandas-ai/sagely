"""
Sagely - LLM-powered assistant for every Python package you import.

Just add .sage.ask("your question") to any module.
"""

from .import_hook import install_hook
from .sage_agent import SageAgent
from .langgraph_agent import LangGraphAgent, create_agent
from .cache import ResponseCache, ModuleInfoCache
from .prompts import (
    INITIAL_RESPONSE_PROMPT,
    ORCHESTRATOR_EVALUATION_PROMPT,
    FINAL_RESPONSE_WITH_WEB_PROMPT,
    FINAL_RESPONSE_WITHOUT_WEB_PROMPT,
    SYSTEM_MESSAGE_TEMPLATE
)
from .config import (
    get_config,
    update_config,
    clear_caches,
    clear_module_cache,
    reset_config,
    SagelyConfig,
    config
)

# Install the import hook
install_hook(SageAgent())

# Create a default agent instance
agent = SageAgent()

__version__ = "0.1.0"
__all__ = [
    "SageAgent",
    "LangGraphAgent", 
    "create_agent",
    "ResponseCache",
    "ModuleInfoCache",
    "INITIAL_RESPONSE_PROMPT",
    "ORCHESTRATOR_EVALUATION_PROMPT", 
    "FINAL_RESPONSE_WITH_WEB_PROMPT",
    "FINAL_RESPONSE_WITHOUT_WEB_PROMPT",
    "SYSTEM_MESSAGE_TEMPLATE",
    "get_config",
    "update_config", 
    "clear_caches",
    "clear_module_cache",
    "reset_config",
    "SagelyConfig",
    "config"
] 