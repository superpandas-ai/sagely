from .sage_agent import SageAgent
from .langgraph_agent import LangGraphAgent, create_agent, web_search
from .prompts import (
    INITIAL_RESPONSE_PROMPT,
    ORCHESTRATOR_EVALUATION_PROMPT,
    FINAL_RESPONSE_WITH_WEB_PROMPT,
    FINAL_RESPONSE_WITHOUT_WEB_PROMPT,
    SYSTEM_MESSAGE_TEMPLATE
)
from .ipython_magics import load_ipython_extension
from .import_hook import install_hook

sage_agent = SageAgent()

install_hook(sage_agent)

__all__ = [
    "sage_agent", 
    "LangGraphAgent", 
    "create_agent", 
    "web_search", 
    "load_ipython_extension",
    "INITIAL_RESPONSE_PROMPT",
    "ORCHESTRATOR_EVALUATION_PROMPT", 
    "FINAL_RESPONSE_WITH_WEB_PROMPT",
    "FINAL_RESPONSE_WITHOUT_WEB_PROMPT",
    "SYSTEM_MESSAGE_TEMPLATE"
] 