# LangGraph Agent for Sagely

This document describes the new LangGraph agent implementation in Sagely, which provides a more structured and extensible approach to handling Python package queries.

## Overview

The `LangGraphAgent` class uses LangGraph to create a workflow-based approach to answering questions about Python packages. It provides:

- **Structured workflow**: Clear separation of concerns with distinct nodes for context analysis and response generation
- **Tool integration**: Built-in tools for module analysis and error context extraction
- **Caching**: Automatic caching of responses for improved performance
- **Extensibility**: Easy to add new nodes and tools to the workflow

## Features

### 1. LangGraph Workflow
The agent uses a two-node workflow:
- **analyze_context**: Gathers traceback, context summary, and module information
- **generate_response**: Creates the final response using the gathered context

### 2. Built-in Tools
- `analyze_module`: Extracts documentation and functions from Python modules
- `get_error_context`: Retrieves recent traceback information

### 3. Caching
Responses are automatically cached using the existing `ResponseCache` system.

## Usage

### Basic Usage

```python
from sagely.agent import create_agent

# Create an agent
agent = create_agent("gpt-4")

# Ask a question
response = agent.ask("numpy", "How do I create a 2D array?")
print(response)
```

### Advanced Usage

```python
from sagely.agent import LangGraphAgent

# Create agent with custom model
agent = LangGraphAgent("gpt-3.5-turbo")

# Ask with context object
context_obj = {"data": [1, 2, 3]}
response = agent.ask("pandas", "How do I convert this to a DataFrame?", context_obj)
```

### Using Tools Directly

```python
from sagely.agent import analyze_module, get_error_context

# Analyze a module
module_info = analyze_module.invoke({"module_name": "math"})
print(module_info)

# Get error context
error_info = get_error_context.invoke({})
print(error_info)
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
- `answer`: Final response

### Workflow Nodes

#### analyze_context Node
- Retrieves traceback information
- Summarizes context objects
- Analyzes target module
- Prepares system message

#### generate_response Node
- Builds comprehensive prompt
- Calls LLM for response
- Returns final answer

## Integration with SageAgent

The `SageAgent` class has been updated to use the `LangGraphAgent` internally:

```python
from sagely import SageAgent

# Create SageAgent (now uses LangGraph internally)
sage = SageAgent("gpt-4")

# Use as before
response = sage.ask("numpy", "How do I create an array?")
```

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
def my_custom_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Custom node implementation."""
    # Process state
    return {"new_field": "value"}

# Add to workflow
workflow.add_node("my_custom_node", my_custom_node)
workflow.add_edge("analyze_context", "my_custom_node")
workflow.add_edge("my_custom_node", "generate_response")
```

## Dependencies

The LangGraph agent requires these additional dependencies:
- `langgraph>=0.0.20`
- `langchain-openai>=0.0.5`
- `langchain-core>=0.1.0`

These are automatically included when installing Sagely.

## Examples

See `examples/langgraph_agent_example.py` for complete usage examples. 