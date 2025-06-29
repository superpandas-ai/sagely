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


@tool
def web_search(query: str) -> str:
    """Search the web for information about Python libraries and programming topics."""
    try:
        # Use DuckDuckGo Instant Answer API for web search
        search_url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
        response = requests.get(search_url, timeout=10)
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
        
        return result
        
    except Exception as e:
        return f"Web search failed: {str(e)}"


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
            "answer": "",
            "web_search_results": "",
            "needs_web_search": False,
            "final_answer": ""
        }
    
    def _generate_response_node(self, state: AgentState) -> AgentState:
        """Node to generate the initial response."""
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

Please provide a comprehensive answer based on the available information.
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
            "answer": response.content,
            "web_search_results": "",
            "needs_web_search": False,
            "final_answer": ""
        }
    
    def _orchestrator_node(self, state: AgentState) -> AgentState:
        """Orchestrator node that decides whether web search is needed."""
        question = state["question"]
        answer = state["answer"]
        module_name = state["module_name"]
        
        # Create a prompt to evaluate if the answer is sufficient
        evaluation_prompt = f"""
You are evaluating whether an answer to a Python programming question is sufficient.

Question: {question}
Module: {module_name}
Current Answer: {answer}

Evaluate if this answer is comprehensive and accurate enough to fully address the user's question.
Consider:
1. Does it directly answer the question?
2. Does it provide enough detail and examples?
3. Does it cover edge cases or common issues?
4. Is it up-to-date with current best practices?

Respond with either "SUFFICIENT" or "NEEDS_WEB_SEARCH" followed by a brief explanation.
"""
        
        evaluation_response = self.llm.invoke([HumanMessage(content=evaluation_prompt)])
        evaluation = evaluation_response.content.strip().upper()
        
        needs_web_search = "NEEDS_WEB_SEARCH" in evaluation
        
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
        return "web_search" if state["needs_web_search"] else "final"
    
    def _web_search_tool_node(self, state: AgentState) -> AgentState:
        """Node that performs web search for additional information."""
        question = state["question"]
        module_name = state["module_name"]
        
        # Create search queries
        search_queries = [
            f"{module_name} python {question}",
            f"{module_name} documentation {question}",
            f"python {module_name} best practices {question}"
        ]
        
        web_results = []
        for query in search_queries:
            try:
                result = web_search.invoke({"query": query})
                if result and "No specific information found" not in result:
                    web_results.append(f"Search: {query}\n{result}\n")
            except Exception as e:
                web_results.append(f"Search failed for '{query}': {str(e)}\n")
        
        combined_results = "\n".join(web_results) if web_results else "No additional web information found."
        
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
        question = state["question"]
        initial_answer = state["answer"]
        web_results = state["web_search_results"]
        module_info = state["module_info"]
        traceback = state["traceback"]
        context_summary = state["context_summary"]
        
        if web_results and "No additional web information found" not in web_results:
            # Combine initial answer with web search results
            prompt = f"""
You have an initial answer and additional web search results. Create a comprehensive final answer.

User Question: {question}

Initial Answer:
{initial_answer}

Additional Web Information:
{web_results}

Package Info:
{module_info}

Recent Error (if any):
{traceback}

Context Object:
{context_summary}

Please create a comprehensive final answer that:
1. Incorporates the best information from both sources
2. Provides clear, actionable guidance
3. Includes relevant examples and best practices
4. Addresses the user's question completely
"""
        else:
            # Use the initial answer as the final answer
            prompt = f"""
The initial answer is sufficient. Please format it nicely for the user.

User Question: {question}

Answer:
{initial_answer}
"""
        
        final_response = self.llm.invoke([HumanMessage(content=prompt)])
        
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
            "answer": "",
            "web_search_results": "",
            "needs_web_search": False,
            "final_answer": ""
        }
        
        # Run the graph
        result = self.graph.invoke(state)
        answer = result["final_answer"]
        
        # Cache the result
        self.cache.set(module_name, question, answer)
        
        return display_with_highlight(answer)


# Convenience function to create an agent instance
def create_agent(model_name: str = "gpt-4") -> LangGraphAgent:
    """Create a new LangGraph agent instance."""
    return LangGraphAgent(model_name) 