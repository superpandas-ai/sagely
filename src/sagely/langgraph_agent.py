from .tracing import *
from typing import Dict, Any, List, Optional, TypedDict, Literal
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
import inspect
import sys
import requests
from urllib.parse import quote_plus
import re
from .cache import ResponseCache, ModuleInfoCache
from .context import get_recent_traceback, summarize_object
from .widgets import display_with_highlight
from .prompts import (
    INITIAL_RESPONSE_PROMPT,
    ORCHESTRATOR_EVALUATION_PROMPT,
    FINAL_RESPONSE_WITH_WEB_PROMPT,
    FINAL_RESPONSE_WITHOUT_WEB_PROMPT,
    SYSTEM_MESSAGE_TEMPLATE
)
from .config import get_config, print_status

# Global module info cache instance
_module_info_cache = ModuleInfoCache()


def extended_module_summary(module):
    """Provide a comprehensive summary of a Python module including functions, classes, and submodules."""
    members = inspect.getmembers(module)
    summary = {"functions": [], "classes": [], "submodules": []}
    for name, obj in members:
        if inspect.isfunction(obj):
            summary["functions"].append((name, inspect.getdoc(obj)))
        elif inspect.isclass(obj):
            summary["classes"].append((name, inspect.getdoc(obj)))
        elif inspect.ismodule(obj):
            summary["submodules"].append(name)
    return summary


@tool
def analyze_module(module_name: str) -> str:
    """Analyze a Python module to extract its documentation and structure."""
    config = get_config()
    if config.show_status_updates:
        print_status(f"Analyzing module '{module_name}'...", "info")
    
    # Check cache first
    cached_info = _module_info_cache.get(module_name)
    if cached_info:
        if config.show_status_updates:
            print_status(f"Using cached module info for '{module_name}'", "cache")
        return cached_info
    
    try:
        __import__(module_name)
        mod = sys.modules[module_name]
        doc = inspect.getdoc(mod)
        
        # Use the extended module summary
        summary = extended_module_summary(mod)
        
        # Format the summary
        result = f"Module: {module_name}\n"
        if doc:
            result += f"Documentation: {doc}\n\n"
        
        # Add functions (limit to first 15 for readability)
        if summary["functions"]:
            result += f"Functions ({len(summary['functions'])} total):\n"
            for name, func_doc in summary["functions"][:15]:
                result += f"- {name}"
                if func_doc:
                    # Truncate long docstrings
                    doc_preview = func_doc[:100] + "..." if len(func_doc) > 100 else func_doc
                    result += f": {doc_preview}"
                result += "\n"
            if len(summary["functions"]) > 15:
                result += f"... and {len(summary['functions']) - 15} more functions\n"
            result += "\n"
        
        # Add classes (limit to first 10 for readability)
        if summary["classes"]:
            result += f"Classes ({len(summary['classes'])} total):\n"
            for name, class_doc in summary["classes"][:10]:
                result += f"- {name}"
                if class_doc:
                    # Truncate long docstrings
                    doc_preview = class_doc[:100] + "..." if len(class_doc) > 100 else class_doc
                    result += f": {doc_preview}"
                result += "\n"
            if len(summary["classes"]) > 10:
                result += f"... and {len(summary['classes']) - 10} more classes\n"
            result += "\n"
        
        # Add submodules
        if summary["submodules"]:
            result += f"Submodules ({len(summary['submodules'])} total):\n"
            for name in summary["submodules"][:10]:
                result += f"- {name}\n"
            if len(summary["submodules"]) > 10:
                result += f"... and {len(summary['submodules']) - 10} more submodules\n"
            result += "\n"
        
        # Cache the result
        _module_info_cache.set(module_name, result)
        if config.show_status_updates:
            print_status(f"Successfully analyzed module '{module_name}'", "success")
        
        return result
        
    except Exception as e:
        error_result = f"Error analyzing module {module_name}: {str(e)}"
        # Cache the error result too to avoid repeated failed attempts
        _module_info_cache.set(module_name, error_result)
        if config.show_status_updates:
            print_status(f"Failed to analyze module '{module_name}': {str(e)}", "error")
        return error_result


@tool
def get_error_context() -> str:
    """Get the recent traceback and error context."""
    config = get_config()
    if config.show_status_updates:
        print_status("Gathering error context...", "info")
    traceback = get_recent_traceback()
    if traceback and traceback.strip():
        if config.show_status_updates:
            print_status("Found recent error traceback", "warning")
    else:
        if config.show_status_updates:
            print_status("No recent errors found", "success")
    return traceback


@tool
def web_search(query: str) -> str:
    """Search the web for information about Python libraries and programming topics."""
    config = get_config()
    if not config.enable_web_search:
        return "Web search is disabled in configuration"
    
    if config.show_status_updates:
        print_status(f"Searching web for: '{query}'", "search")
    try:
        # Use DuckDuckGo Instant Answer API for web search
        search_url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
        response = requests.get(search_url, timeout=config.web_search_timeout)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract relevant information
        result = ""
        
        if data.get("Abstract"):
            result += f"Abstract: {data['Abstract']}\n\n"
        
        if data.get("Answer"):
            result += f"Answer: {data['Answer']}\n\n"
        
        if data.get("RelatedTopics"):
            related = data["RelatedTopics"][:3]  # Limit to first 3 related topics
            result += "Related Topics:\n"
            for topic in related:
                if isinstance(topic, dict) and topic.get("Text"):
                    result += f"- {topic['Text']}\n"
        
        if not result.strip():
            result = f"No specific information found for: {query}"
            if config.show_status_updates:
                print_status(f"No web results found for: '{query}'", "warning")
        else:
            if config.show_status_updates:
                print_status(f"Found web results for: '{query}'", "success")
        
        return result
        
    except Exception as e:
        error_msg = f"Web search failed: {str(e)}"
        if config.show_status_updates:
            print_status(error_msg, "error")
        return error_msg


# Define the state schema as a TypedDict
class AgentState(TypedDict):
    module_name: str
    question: str
    context_obj: Optional[Any]
    traceback: str
    module_info: str
    context_summary: str
    messages: List[Dict[str, str]]
    answer: str
    web_search_results: str
    needs_web_search: bool
    final_answer: str


class LangGraphAgent:
    """A simple LangGraph agent for handling Python package queries."""
    
    def __init__(self, model_name: str = "gpt-4"):
        config = get_config()
        if config.show_status_updates:
            print_status(f"Initializing LangGraph agent with model: {model_name}", "info")
        self.llm = ChatOpenAI(model=model_name)
        self.cache = ResponseCache()
        self.module_cache = ModuleInfoCache()
        self.graph = self._build_graph()
        if config.show_status_updates:
            print_status("LangGraph agent initialized successfully", "success")
    
    def _build_graph(self):
        """Build the LangGraph workflow."""
        config = get_config()
        if config.show_status_updates:
            print_status("Building LangGraph workflow...", "info")
        
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyze_context", self._analyze_context_node)
        workflow.add_node("generate_response", self._generate_response_node)
        workflow.add_node("orchestrator", self._orchestrator_node)
        workflow.add_node("web_search_tool", self._web_search_tool_node)
        workflow.add_node("generate_final_response", self._generate_final_response_node)
        
        # Define the flow
        workflow.set_entry_point("analyze_context")
        workflow.add_edge("analyze_context", "generate_response")
        workflow.add_edge("generate_response", "orchestrator")
        
        # Conditional edge from orchestrator
        workflow.add_conditional_edges(
            "orchestrator",
            self._should_use_web_search,
            {
                "web_search": "web_search_tool",
                "final": "generate_final_response"
            }
        )
        
        workflow.add_edge("web_search_tool", "generate_final_response")
        workflow.add_edge("generate_final_response", END)
        
        compiled_graph = workflow.compile()
        if config.show_status_updates:
            print_status("LangGraph workflow built successfully", "success")
        return compiled_graph
    
    def _analyze_context_node(self, state: AgentState) -> AgentState:
        """Node to analyze the context and gather information."""
        config = get_config()
        module_name = state["module_name"]
        context_obj = state.get("context_obj")
        
        if config.show_status_updates:
            print_status(f"Starting context analysis for module: {module_name}", "info")
        
        # Get traceback
        traceback = get_recent_traceback()
        
        # Get context summary
        context_summary = summarize_object(context_obj) if context_obj else "None"
        
        # Check module cache first, then analyze if needed
        module_info = self.module_cache.get(module_name)
        if not module_info:
            module_info = analyze_module.invoke({"module_name": module_name})
            # The analyze_module function already caches the result
        
        if config.show_status_updates:
            print_status("Context analysis completed", "success")
        
        return {
            "module_name": module_name,
            "question": state["question"],
            "context_obj": context_obj,
            "traceback": traceback,
            "context_summary": context_summary,
            "module_info": module_info,
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_MESSAGE_TEMPLATE.format(module_name=module_name)
                }
            ],
            "answer": "",
            "web_search_results": "",
            "needs_web_search": False,
            "final_answer": ""
        }
    
    def _generate_response_node(self, state: AgentState) -> AgentState:
        """Node to generate the initial response."""
        config = get_config()
        question = state["question"]
        traceback = state["traceback"]
        context_summary = state["context_summary"]
        module_info = state["module_info"]
        
        if config.show_status_updates:
            print_status("Generating initial response...", "thinking")
        
        # Build the prompt using the template
        prompt = INITIAL_RESPONSE_PROMPT.format(
            traceback=traceback,
            context_summary=context_summary,
            module_info=module_info,
            question=question
        )
        
        # Get response from LLM
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        if config.show_status_updates:
            print_status("Initial response generated", "success")
        
        return {
            "module_name": state["module_name"],
            "question": question,
            "context_obj": state["context_obj"],
            "traceback": traceback,
            "context_summary": context_summary,
            "module_info": module_info,
            "messages": state["messages"],
            "answer": response.content,
            "web_search_results": "",
            "needs_web_search": False,
            "final_answer": ""
        }
    
    def _orchestrator_node(self, state: AgentState) -> AgentState:
        """Orchestrator node that decides whether web search is needed."""
        config = get_config()
        question = state["question"]
        answer = state["answer"]
        module_name = state["module_name"]
        
        if config.show_status_updates:
            print_status("Evaluating if web search is needed...", "thinking")
        
        # Create a prompt to evaluate if the answer is sufficient
        evaluation_prompt = ORCHESTRATOR_EVALUATION_PROMPT.format(
            question=question,
            module_name=module_name,
            answer=answer
        )
        
        evaluation_response = self.llm.invoke([HumanMessage(content=evaluation_prompt)])
        evaluation = evaluation_response.content.strip().upper()
        
        needs_web_search = "NEEDS_WEB_SEARCH" in evaluation
        
        if needs_web_search:
            if config.show_status_updates:
                print_status("Web search needed for comprehensive answer", "search")
        else:
            if config.show_status_updates:
                print_status("Initial answer is sufficient", "success")
        
        return {
            "module_name": state["module_name"],
            "question": question,
            "context_obj": state["context_obj"],
            "traceback": state["traceback"],
            "context_summary": state["context_summary"],
            "module_info": state["module_info"],
            "messages": state["messages"],
            "answer": answer,
            "web_search_results": "",
            "needs_web_search": needs_web_search,
            "final_answer": ""
        }
    
    def _should_use_web_search(self, state: AgentState) -> Literal["web_search", "final"]:
        """Determine if web search is needed."""
        config = get_config()
        if not config.enable_web_search:
            return "final"
        return "web_search" if state["needs_web_search"] else "final"
    
    def _web_search_tool_node(self, state: AgentState) -> AgentState:
        """Node that performs web search for additional information."""
        config = get_config()
        question = state["question"]
        module_name = state["module_name"]
        
        if config.show_status_updates:
            print_status("Starting web search for additional information...", "search")
        
        # Create search queries
        search_queries = [
            f"{module_name} python {question}",
            f"{module_name} documentation {question}",
            f"python {module_name} best practices {question}"
        ]
        
        web_results = []
        for i, query in enumerate(search_queries, 1):
            if config.show_status_updates:
                print_status(f"Web search {i}/{len(search_queries)}: {query[:50]}...", "search")
            try:
                result = web_search.invoke({"query": query})
                if result and "No specific information found" not in result:
                    web_results.append(f"Search: {query}\n{result}\n")
            except Exception as e:
                web_results.append(f"Search failed for '{query}': {str(e)}\n")
        
        combined_results = "\n".join(web_results) if web_results else "No additional web information found."
        
        if combined_results and "No additional web information found" not in combined_results:
            if config.show_status_updates:
                print_status("Web search completed with results", "success")
        else:
            if config.show_status_updates:
                print_status("No additional web information found", "warning")
        
        return {
            "module_name": state["module_name"],
            "question": question,
            "context_obj": state["context_obj"],
            "traceback": state["traceback"],
            "context_summary": state["context_summary"],
            "module_info": state["module_info"],
            "messages": state["messages"],
            "answer": state["answer"],
            "web_search_results": combined_results,
            "needs_web_search": state["needs_web_search"],
            "final_answer": ""
        }
    
    def _generate_final_response_node(self, state: AgentState) -> AgentState:
        """Node to generate the final comprehensive response."""
        config = get_config()
        question = state["question"]
        initial_answer = state["answer"]
        web_results = state["web_search_results"]
        module_info = state["module_info"]
        traceback = state["traceback"]
        context_summary = state["context_summary"]
        
        if web_results and "No additional web information found" not in web_results:
            if config.show_status_updates:
                print_status("Generating final response with web search results...", "thinking")
            # Combine initial answer with web search results
            prompt = FINAL_RESPONSE_WITH_WEB_PROMPT.format(
                question=question,
                initial_answer=initial_answer,
                web_results=web_results,
                module_info=module_info,
                traceback=traceback,
                context_summary=context_summary
            )
        else:
            if config.show_status_updates:
                print_status("Generating final response from initial answer...", "thinking")
            # Use the initial answer as the final answer
            prompt = FINAL_RESPONSE_WITHOUT_WEB_PROMPT.format(
                question=question,
                initial_answer=initial_answer
            )
        
        final_response = self.llm.invoke([HumanMessage(content=prompt)])
        
        if config.show_status_updates:
            print_status("Final response generated successfully", "success")
        
        return {
            "module_name": state["module_name"],
            "question": question,
            "context_obj": state["context_obj"],
            "traceback": traceback,
            "context_summary": context_summary,
            "module_info": module_info,
            "messages": state["messages"],
            "answer": initial_answer,
            "web_search_results": web_results,
            "needs_web_search": state["needs_web_search"],
            "final_answer": final_response.content
        }
    
    def ask(self, module_name: str, question: str, context_obj: Optional[Any] = None, use_cache: bool = True) -> None:
        """Ask a question about a Python module."""
        config = get_config()
        
        if config.show_status_updates:
            print_status(f"Processing question about '{module_name}': {question[:50]}...", "info")
        
        # Check cache first
        if use_cache and config.enable_response_cache:
            cached = self.cache.get(module_name, question)
            if cached:
                if config.show_status_updates:
                    print_status("Using cached answer", "cache")
                display_with_highlight(f"📦 Cached Answer:\n{cached}")
                return
        
        if config.show_status_updates:
            print_status("Starting LangGraph workflow execution...", "info")
        
        # Prepare state
        state: AgentState = {
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
        result = self.graph.invoke(state)
        answer = result["final_answer"]
        
        # Cache the result
        if config.enable_response_cache:
            self.cache.set(module_name, question, answer)
            if config.show_status_updates:
                print_status("Answer cached for future use", "cache")
        
        # Display the result without returning it
        if config.show_status_updates:
            print_status("Displaying final answer", "success")
        display_with_highlight(answer)

    def clear_module_cache(self, module_name: Optional[str] = None) -> None:
        """Clear the module info cache.
        
        Args:
            module_name: If provided, clear cache for this specific module only.
                        If None, clear all module cache.
        """
        config = get_config()
        if module_name:
            self.module_cache.clear_module(module_name)
            if config.show_status_updates:
                print_status(f"Cleared module cache for '{module_name}'", "cache")
        else:
            self.module_cache.clear()
            if config.show_status_updates:
                print_status("Cleared all module cache", "cache")

    def is_module_cached(self, module_name: str) -> bool:
        """Check if module info is cached.
        
        Args:
            module_name: Name of the module to check
            
        Returns:
            True if the module info is cached, False otherwise
        """
        return self.module_cache.get(module_name) is not None


# Convenience function to create an agent instance
def create_agent(model_name: str = "gpt-4") -> LangGraphAgent:
    """Create a new LangGraph agent instance."""
    return LangGraphAgent(model_name) 