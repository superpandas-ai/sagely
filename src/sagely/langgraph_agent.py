from typing import Dict, Any, List, Optional, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
import inspect
import sys
from .cache import ResponseCache
from .context import get_recent_traceback, summarize_object
from .widgets import display_with_highlight


@tool
def analyze_module(module_name: str) -> str:
    """Analyze a Python module to extract its documentation and functions."""
    try:
        __import__(module_name)
        mod = sys.modules[module_name]
        doc = inspect.getdoc(mod)
        members = inspect.getmembers(mod)
        functions = [name for name, obj in members if inspect.isfunction(obj)]
        return f"Documentation: {doc}\nFunctions: {functions[:20]}"
    except Exception as e:
        return f"Error analyzing module {module_name}: {str(e)}"


@tool
def get_error_context() -> str:
    """Get the recent traceback and error context."""
    return get_recent_traceback()


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


class LangGraphAgent:
    """A simple LangGraph agent for handling Python package queries."""
    
    def __init__(self, model_name: str = "gpt-4"):
        self.llm = ChatOpenAI(model=model_name)
        self.cache = ResponseCache()
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow."""
        
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyze_context", self._analyze_context_node)
        workflow.add_node("generate_response", self._generate_response_node)
        
        # Define the flow
        workflow.set_entry_point("analyze_context")
        workflow.add_edge("analyze_context", "generate_response")
        workflow.add_edge("generate_response", END)
        
        return workflow.compile()
    
    def _analyze_context_node(self, state: AgentState) -> AgentState:
        """Node to analyze the context and gather information."""
        module_name = state["module_name"]
        context_obj = state.get("context_obj")
        
        # Get traceback
        traceback = get_recent_traceback()
        
        # Get context summary
        context_summary = summarize_object(context_obj) if context_obj else "None"
        
        # Analyze module
        module_info = analyze_module.invoke({"module_name": module_name})
        
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
                    "content": f"You are an assistant for the Python library '{module_name}'. Provide helpful, accurate answers about the library."
                }
            ],
            "answer": ""
        }
    
    def _generate_response_node(self, state: AgentState) -> AgentState:
        """Node to generate the final response."""
        question = state["question"]
        traceback = state["traceback"]
        context_summary = state["context_summary"]
        module_info = state["module_info"]
        
        # Build the prompt
        prompt = f"""
Recent Error (if any):
{traceback}

Context Object:
{context_summary}

Package Info:
{module_info}

User Question:
{question}
"""
        
        # Get response from LLM
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        return {
            "module_name": state["module_name"],
            "question": question,
            "context_obj": state["context_obj"],
            "traceback": traceback,
            "context_summary": context_summary,
            "module_info": module_info,
            "messages": state["messages"],
            "answer": response.content
        }
    
    def ask(self, module_name: str, question: str, context_obj: Optional[Any] = None, use_cache: bool = True) -> str:
        """Ask a question about a Python module."""
        
        # Check cache first
        if use_cache:
            cached = self.cache.get(module_name, question)
            if cached:
                return display_with_highlight(f"📦 Cached Answer:\n{cached}")
        
        # Prepare state
        state: AgentState = {
            "module_name": module_name,
            "question": question,
            "context_obj": context_obj,
            "traceback": "",
            "module_info": "",
            "context_summary": "",
            "messages": [],
            "answer": ""
        }
        
        # Run the graph
        result = self.graph.invoke(state)
        answer = result["answer"]
        
        # Cache the result
        self.cache.set(module_name, question, answer)
        
        return display_with_highlight(answer)


# Convenience function to create an agent instance
def create_agent(model_name: str = "gpt-4") -> LangGraphAgent:
    """Create a new LangGraph agent instance."""
    return LangGraphAgent(model_name) 