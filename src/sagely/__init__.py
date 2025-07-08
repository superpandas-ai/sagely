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
from .usage_info import (
    get_usage_tracker,
    add_usage,
    get_session_total,
    get_session_summary,
    clear_usage_history,
    get_model_usage,
    get_all_model_usage,
    clear_model_history,
    get_model_recent_usage,
    get_session_file_path,
    get_session_id,
    get_all_session_files,
    load_session_from_file,
    load_latest_session,
    TokenUsage,
    UsageTracker
)

# Create a single agent instance to be shared
_default_agent = SageAgent()

# Install the import hook with the shared agent
install_hook(_default_agent)

# Create a default agent instance (alias to the shared one)
agent = _default_agent

# Create a usage_data attribute for easy access to session usage information
from .usage_info import get_session_total, get_session_summary, get_usage_tracker

class UsageData:
    """Easy access to current session usage information."""
    
    @property
    def total(self):
        """Get total usage for the current session."""
        return get_session_total()
    
    @property
    def summary(self):
        """Get formatted summary of session usage."""
        return get_session_summary()
    
    @property
    def tracker(self):
        """Get the usage tracker instance."""
        return get_usage_tracker()
    
    @property
    def input_tokens(self):
        """Get total input tokens for the session."""
        return get_session_total().input_tokens
    
    @property
    def output_tokens(self):
        """Get total output tokens for the session."""
        return get_session_total().output_tokens
    
    @property
    def total_tokens(self):
        """Get total tokens for the session."""
        return get_session_total().total_tokens
    
    @property
    def request_count(self):
        """Get number of requests in the session."""
        return len(get_usage_tracker().get_recent_usage())
    
    @property
    def models(self):
        """Get usage for all models."""
        return get_all_model_usage()
    
    def get_model_usage(self, model_name: str):
        """Get usage for a specific model."""
        return get_model_usage(model_name)
    
    def get_model_recent_usage(self, model_name: str, count: int = 5):
        """Get recent usage for a specific model."""
        return get_model_recent_usage(model_name, count)
    
    def clear_model_history(self, model_name: str):
        """Clear history for a specific model."""
        clear_model_history(model_name)
    
    @property
    def session_id(self):
        """Get the current session ID."""
        return get_session_id()
    
    @property
    def session_file_path(self):
        """Get the file path for the current session's usage data."""
        return get_session_file_path()
    
    def __str__(self):
        """String representation showing current usage."""
        return get_session_summary()
    
    def __repr__(self):
        """Detailed representation of usage data."""
        total = get_session_total()
        models = get_all_model_usage()
        model_count = len(models)
        return f"UsageData(input_tokens={total.input_tokens}, output_tokens={total.output_tokens}, total_tokens={total.total_tokens}, requests={self.request_count}, models={model_count}, session_id={self.session_id})"

# Create the usage_data attribute
usage_data = UsageData()

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
    "config",
    "get_usage_tracker",
    "add_usage",
    "get_session_total",
    "get_session_summary",
    "clear_usage_history",
    "get_model_usage",
    "get_all_model_usage",
    "clear_model_history",
    "get_model_recent_usage",
    "get_session_file_path",
    "get_session_id",
    "get_all_session_files",
    "load_session_from_file",
    "load_latest_session",
    "TokenUsage",
    "UsageTracker",
    "usage_data"
] 