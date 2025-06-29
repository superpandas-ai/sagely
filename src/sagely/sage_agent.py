from .tracing import *
import openai
from .cache import ResponseCache
from .langgraph_agent import LangGraphAgent

class SageAgent:
    def __init__(self, model_name: str = "gpt-4"):
        self.cache = ResponseCache()
        self.client = openai.OpenAI()
        self.langgraph_agent = LangGraphAgent(model_name)

    def ask(self, module_name, question, context_obj=None, use_cache=True):
        # Use the LangGraph agent for processing
        return self.langgraph_agent.ask(module_name, question, context_obj, use_cache) 