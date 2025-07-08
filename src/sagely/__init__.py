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

# Create a single agent instance to be shared
_default_agent = SageAgent()

# Install the import hook with the shared agent
install_hook(_default_agent)

# Create a default agent instance (alias to the shared one)
agent = _default_agent

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