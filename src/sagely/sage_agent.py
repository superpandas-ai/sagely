from .tracing import *
import openai
from .cache import ResponseCache
from .langgraph_agent import LangGraphAgent
from .config import get_config, print_status

class SageAgent:
    def __init__(self, model_name: str = "gpt-4"):
        config = get_config()
        if config.show_status_updates:
            print_status(f"Initializing SageAgent with model: {model_name}", "info")
        self.cache = ResponseCache()
        self.client = openai.OpenAI()
        self.langgraph_agent = LangGraphAgent(model_name)
        if config.show_status_updates:
            print_status("SageAgent initialized successfully", "success")

    def ask(self, module_name, question, context_obj=None, use_cache=True):
        config = get_config()
        if config.show_status_updates:
            print_status(f"SageAgent processing question about '{module_name}'", "info")
        
        # Check cache first
        if use_cache and config.enable_response_cache:
            cached = self.cache.get(module_name, question)
            if cached:
                if config.show_status_updates:
                    print_status("Using cached answer from SageAgent", "cache")
                from .widgets import display_with_highlight
                cached_response = f"📦 Cached Answer:\n{cached}"
                display_with_highlight(cached_response)
                return  # Do not return any value
        
        if config.show_status_updates:
            print_status("No cached answer found, proceeding with LangGraph workflow", "info")
        
        # Prepare state for LangGraph agent
        state = {
            "module_name": module_name,
            "question": question,
            "context_obj": context_obj,
            "traceback": "",
            "module_info": "",
            "context_summary": "",
            "messages": [],
            "answer": "",
            "web_search_results": "",
            "needs_web_search": False,
            "final_answer": ""
        }
        
        # Run the graph
        result = self.langgraph_agent.graph.invoke(state)
        answer = result["final_answer"]
        
        # Cache the result
        if config.enable_response_cache:
            self.cache.set(module_name, question, answer)
            if config.show_status_updates:
                print_status("Answer cached in SageAgent for future use", "cache")
        
        # Display the result
        from .widgets import display_with_highlight
        display_with_highlight(answer)
        # Do not return any value 