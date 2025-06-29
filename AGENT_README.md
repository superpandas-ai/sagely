# Enhanced LangGraph Agent for Sagely

This document describes the enhanced LangGraph agent implementation in Sagely, which provides a more structured and extensible approach to handling Python package queries with web search capabilities.

## Overview

The `LangGraphAgent` class uses LangGraph to create a sophisticated workflow-based approach to answering questions about Python packages. It provides:

- **Structured workflow**: Clear separation of concerns with distinct nodes for context analysis, response generation, and web search
- **Intelligent orchestration**: Automatically decides when web search is needed for comprehensive answers
- **Tool integration**: Built-in tools for module analysis, error context extraction, and web search
- **Caching**: Automatic caching of responses for improved performance
- **Extensibility**: Easy to add new nodes and tools to the workflow

## Features

### 1. Enhanced LangGraph Workflow
The agent uses a five-node workflow:
- **analyze_context**: Gathers traceback, context summary, and module information
- **generate_response**: Creates initial response using available information
- **orchestrator**: Evaluates if the answer is sufficient or needs web search
- **web_search_tool**: (Conditional) Performs web search for additional information
- **generate_final_response**: Creates comprehensive final answer

### 2. Built-in Tools
- `analyze_module`: Extracts documentation and functions from Python modules
- `get_error_context`: Retrieves recent traceback information
- `web_search`: Searches the web for additional information using DuckDuckGo API

### 3. Intelligent Orchestration
The orchestrator node uses AI to evaluate whether the initial answer is sufficient:
- Checks if the answer directly addresses the question
- Evaluates if enough detail and examples are provided
- Considers if edge cases and best practices are covered
- Determines if the information is up-to-date

### 4. Caching
Responses are automatically cached using the existing `ResponseCache` system.

## Usage

### Basic Usage

```python
from sagely.langgraph_agent import create_agent

# Create an enhanced agent
agent = create_agent("gpt-4")

# Ask a question (agent will automatically decide if web search is needed)
response = agent.ask("numpy", "How do I create a 2D array?")
print(response)
```

### Advanced Usage

```python
from sagely.langgraph_agent import LangGraphAgent

# Create agent with custom model
agent = LangGraphAgent("gpt-3.5-turbo")

# Ask complex question that might benefit from web search
context_obj = {"data": [1, 2, 3]}
response = agent.ask("pandas", "What are the latest performance improvements in pandas 2.0?", context_obj)
```

### Using Tools Directly

```python
from sagely.langgraph_agent import analyze_module, get_error_context, web_search

# Analyze a module
module_info = analyze_module.invoke({"module_name": "math"})
print(module_info)

# Get error context
error_info = get_error_context.invoke({})
print(error_info)

# Search the web
web_result = web_search.invoke({"query": "python pandas performance optimization"})
print(web_result)
```

## Architecture

### State Management
The agent uses a structured state object that includes:
- `module_name`: The target Python module
- `question`: User's question
- `context_obj`: Optional context object
- `traceback`: Recent error traceback
- `module_info`: Analyzed module information
- `context_summary`: Summary of context object
- `messages`: Conversation history
- `answer`: Initial response
- `web_search_results`: Results from web search
- `needs_web_search`: Boolean flag for web search decision
- `final_answer`: Comprehensive final response

### Workflow Nodes

#### analyze_context Node
- Retrieves traceback information
- Summarizes context objects
- Analyzes target module
- Prepares system message

#### generate_response Node
- Builds comprehensive prompt
- Calls LLM for initial response
- Returns initial answer

#### orchestrator Node
- Evaluates initial answer quality
- Uses AI to determine if web search is needed
- Sets `needs_web_search` flag

#### web_search_tool Node (Conditional)
- Performs multiple web searches with different queries
- Combines results from DuckDuckGo API
- Handles search failures gracefully

#### generate_final_response Node
- Combines initial answer with web search results
- Creates comprehensive final response
- Ensures answer addresses the question completely

### Conditional Flow
The workflow uses conditional edges to decide whether to perform web search:
- If orchestrator determines answer is sufficient → go to final response
- If orchestrator determines answer needs enhancement → go to web search, then final response

## Integration with SageAgent

The `SageAgent` class has been updated to use the enhanced `LangGraphAgent` internally:

```python
from sagely import SageAgent

# Create SageAgent (now uses enhanced LangGraph internally)
sage = SageAgent("gpt-4")

# Use as before - now with automatic web search when needed
response = sage.ask("numpy", "What are the latest memory optimization techniques?")
```

## Web Search Capabilities

### DuckDuckGo Integration
The web search tool uses DuckDuckGo's Instant Answer API to provide:
- Abstract summaries
- Direct answers
- Related topics
- No API key required

### Search Strategy
The agent performs multiple searches with different query formulations:
1. `{module_name} python {question}`
2. `{module_name} documentation {question}`
3. `python {module_name} best practices {question}`

### Error Handling
- Graceful handling of network failures
- Fallback to initial answer if web search fails
- Timeout protection (10 seconds)

## Extending the Agent

### Adding New Tools

```python
from langchain_core.tools import tool

@tool
def my_custom_tool(param: str) -> str:
    """Description of what this tool does."""
    # Tool implementation
    return "result"
```

### Adding New Nodes

```python
def my_custom_node(state: AgentState) -> AgentState:
    """Custom node implementation."""
    # Process state
    return {"new_field": "value"}

# Add to workflow
workflow.add_node("my_custom_node", my_custom_node)
workflow.add_edge("orchestrator", "my_custom_node")
workflow.add_edge("my_custom_node", "generate_final_response")
```

### Modifying Orchestration Logic

```python
def custom_orchestrator_logic(state: AgentState) -> AgentState:
    """Custom logic for deciding when to use web search."""
    # Custom evaluation logic
    needs_search = custom_evaluation(state["answer"])
    return {**state, "needs_web_search": needs_search}
```

## Dependencies

The enhanced LangGraph agent requires these additional dependencies:
- `langgraph>=0.0.20`
- `langchain-openai>=0.0.5`
- `langchain-core>=0.1.0`
- `requests>=2.25.0`

These are automatically included when installing Sagely.

## Examples

See `examples/enhanced_agent_example.py` for complete usage examples demonstrating:
- Basic questions that don't need web search
- Complex questions that benefit from web search
- Direct web search tool usage
- Workflow information and node descriptions

## Performance Considerations

- **Caching**: All responses are cached to avoid repeated API calls
- **Conditional Web Search**: Web search only occurs when needed
- **Timeout Protection**: Web searches have 10-second timeout
- **Multiple Queries**: Uses multiple search strategies for comprehensive results 