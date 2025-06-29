# Enhanced LangGraph Agent for Sagely

This document describes the enhanced LangGraph agent implementation in Sagely, which provides a more structured and extensible approach to handling Python package queries with web search capabilities.

## ⚙️ Configuration System

Sagely provides a centralized configuration system for customizing agent behavior, model selection, cache management, and more.

### Accessing and Updating Configuration
```python
from sagely import get_config, update_config, clear_caches, clear_module_cache, reset_config, SageAgent

# View current configuration
config = get_config()
print(config.get_config())

# Update configuration (e.g., change model, disable status updates)
update_config(model_name="gpt-3.5-turbo", show_status_updates=False)

# Create a new agent with the updated model
agent = SageAgent(model_name=get_config().model_name)

# Reset configuration to defaults
reset_config()
```

### Available Configuration Options
- `model_name`: LLM model to use (default: "gpt-4")
- `show_status_updates`: Show status outputs (default: True)
- `enable_response_cache`: Enable/disable response caching (default: True)
- `enable_module_cache`: Enable/disable module info caching (default: True)
- `enable_web_search`: Enable/disable web search (default: True)
- `web_search_timeout`: Timeout for web search requests (default: 10)
- `enable_langsmith_tracing`: Enable LangSmith tracing (default: False)
- `langsmith_project`: LangSmith project name (default: None)

### Cache Management
```python
# Clear all caches
clear_caches()

# Clear only response cache
clear_caches("response")

# Clear only module cache
clear_caches("module")

# Clear module cache for a specific module
clear_module_cache("json")
```

### Environment Variable Configuration
You can also configure Sagely using environment variables:
- `SAGELY_MODEL`
- `SAGELY_SHOW_STATUS`
- `SAGELY_ENABLE_RESPONSE_CACHE`
- `SAGELY_ENABLE_MODULE_CACHE`
- `SAGELY_ENABLE_WEB_SEARCH`
- `SAGELY_WEB_SEARCH_TIMEOUT`
- `SAGELY_ENABLE_LANGSMITH`
- `SAGELY_LANGSMITH_PROJECT`

Example:
```bash
export SAGELY_MODEL=gpt-4
export SAGELY_SHOW_STATUS=false
export SAGELY_ENABLE_WEB_SEARCH=false
export SAGELY_WEB_SEARCH_TIMEOUT=15
```

## LangSmith Tracing Support

Sagely supports [LangSmith](https://smith.langchain.com/) for tracing and experiment tracking. To enable LangSmith tracing:

1. **Install dependencies** (already included):
   - `langsmith`
   - `langchain-core`

2. **Set environment variables** (in your shell or `.env` file):
   ```sh
   export LANGCHAIN_TRACING_V2=true
   export LANGCHAIN_API_KEY=your-langsmith-api-key
   export LANGCHAIN_PROJECT=your-project-name  # optional
   ```

3. **Run your code as usual**. All LangChain and LangGraph runs will be traced to your LangSmith dashboard.

For more details, see the [LangSmith docs](https://docs.smith.langchain.com/docs/tracing/).

## Status Outputs

The LangGraph agent provides real-time status updates throughout the workflow execution, giving users visibility into what's happening at each step:

### Status Types
- **ℹ️ info**: General information about the process
- **✅ success**: Successful completion of a step
- **⚠️ warning**: Warnings or non-critical issues
- **❌ error**: Errors that occurred
- **🔍 search**: Web search operations
- **🤔 thinking**: AI processing and decision-making
- **📦 cache**: Cache operations (hits/misses)

### Example Status Flow
```
ℹ️ Processing question about 'requests': How do I send a POST request?...
ℹ️ Starting LangGraph workflow execution...
ℹ️ Starting context analysis for module: requests
ℹ️ Analyzing module 'requests'...
✅ Successfully analyzed module 'requests'
✅ Context analysis completed
🤔 Generating initial response...
✅ Initial response generated
🤔 Evaluating if web search is needed...
🔍 Web search needed for comprehensive answer
🔍 Starting web search for additional information...
🔍 Web search 1/3: requests python How do I send a POST request?...
🔍 Web search 2/3: requests documentation How do I send a POST request?...
🔍 Web search 3/3: python requests best practices How do I send a POST request?...
✅ Web search completed with results
🤔 Generating final response with web search results...
✅ Final response generated successfully
📦 Answer cached for future use
✅ Displaying final answer
```

### Benefits
- **Transparency**: Users know exactly what the agent is doing
- **Debugging**: Easy to identify where issues occur
- **Performance**: Can see cache hits and workflow efficiency
- **Trust**: Users understand the reasoning process

## Overview

The `LangGraphAgent` class uses LangGraph to create a sophisticated workflow-based approach to answering questions about Python packages. It provides:

- **Structured workflow**: Clear separation of concerns with distinct nodes for context analysis, response generation, and web search
- **Intelligent orchestration**: Automatically decides when web search is needed for comprehensive answers
- **Tool integration**: Built-in tools for module analysis, error context extraction, and web search
- **Caching**: Automatic caching of responses for improved performance
- **Extensibility**: Easy to add new nodes and tools to the workflow
- **Separated prompts**: All prompts are stored in a separate file for easy customization and maintenance
- **Real-time status updates**: Comprehensive feedback throughout the workflow execution

## Features

### 1. Enhanced LangGraph Workflow
The agent uses a five-node workflow:
- **analyze_context**: Gathers traceback, context summary, and module information
- **generate_response**: Creates initial response using available information
- **orchestrator**: Evaluates if the answer is sufficient or needs web search
- **web_search_tool**: (Conditional) Performs web search for additional information
- **generate_final_response**: Creates comprehensive final answer

### 2. Built-in Tools
- `analyze_module`: Extracts comprehensive documentation and structure from Python modules
- `get_error_context`: Retrieves recent traceback information
- `web_search`: Searches the web for additional information using DuckDuckGo API

### 3. Enhanced Module Analysis
The `analyze_module` tool provides comprehensive module analysis including:
- **Module documentation**: Full module docstring
- **Functions**: List of functions with docstrings (truncated for readability)
- **Classes**: List of classes with docstrings (truncated for readability)
- **Submodules**: List of submodules within the module
- **Smart truncation**: Limits output to prevent overwhelming responses while showing totals

### 4. Intelligent Orchestration
The orchestrator node uses AI to evaluate whether the initial answer is sufficient:
- Checks if the answer directly addresses the question
- Evaluates if enough detail and examples are provided
- Considers if edge cases and best practices are covered
- Determines if the information is up-to-date

### 5. Separated Prompts
All prompts are stored in `sagely.prompts` for easy customization:
- `INITIAL_RESPONSE_PROMPT`: Template for generating initial responses
- `ORCHESTRATOR_EVALUATION_PROMPT`: Template for evaluating answer sufficiency
- `FINAL_RESPONSE_WITH_WEB_PROMPT`: Template for final responses with web search
- `FINAL_RESPONSE_WITHOUT_WEB_PROMPT`: Template for final responses without web search
- `SYSTEM_MESSAGE_TEMPLATE`: Template for system messages

### 6. Caching
Responses are automatically cached using the existing `ResponseCache` system.

### 7. Status Outputs
Real-time feedback throughout the workflow execution with categorized status messages.

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

# Analyze a module with comprehensive information
module_info = analyze_module.invoke({"module_name": "json"})
print(module_info)
# Output includes: documentation, functions with docstrings, classes, and submodules

# Get error context
error_info = get_error_context.invoke({})
print(error_info)

# Search the web
web_result = web_search.invoke({"query": "python pandas performance optimization"})
print(web_result)
```

### Using Prompts Directly

```python
from sagely.prompts import (
    INITIAL_RESPONSE_PROMPT,
    ORCHESTRATOR_EVALUATION_PROMPT,
    SYSTEM_MESSAGE_TEMPLATE
)

# Use prompts for custom implementations
system_msg = SYSTEM_MESSAGE_TEMPLATE.format(module_name="numpy")
initial_prompt = INITIAL_RESPONSE_PROMPT.format(
    traceback="No errors",
    context_summary="Working with arrays",
    module_info="NumPy module info",
    question="How to create arrays?"
)
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
- Analyzes target module using enhanced analysis
- Prepares system message

#### generate_response Node
- Builds comprehensive prompt using `INITIAL_RESPONSE_PROMPT`
- Calls LLM for initial response
- Returns initial answer

#### orchestrator Node
- Evaluates initial answer quality using `ORCHESTRATOR_EVALUATION_PROMPT`
- Uses AI to determine if web search is needed
- Sets `needs_web_search` flag

#### web_search_tool Node (Conditional)
- Performs multiple web searches with different queries
- Combines results from DuckDuckGo API
- Handles search failures gracefully

#### generate_final_response Node
- Combines initial answer with web search results
- Uses `FINAL_RESPONSE_WITH_WEB_PROMPT` or `FINAL_RESPONSE_WITHOUT_WEB_PROMPT`
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

## Module Analysis Features

### Comprehensive Analysis
The `extended_module_summary` function provides:
- **Functions**: All functions with their docstrings
- **Classes**: All classes with their docstrings  
- **Submodules**: All submodules within the module
- **Documentation**: Full module docstring

### Smart Output Formatting
- **Truncated docstrings**: Long docstrings are truncated to 100 characters for readability
- **Limited listings**: Shows first 15 functions, 10 classes, and 10 submodules
- **Total counts**: Shows total number of items in each category
- **Structured output**: Clear sections for functions, classes, and submodules

### Example Output
```
Module: json
Documentation: JSON (JavaScript Object Notation) is a subset of JavaScript syntax...

Functions (5 total):
- dump: Serialize ``obj`` as a JSON formatted stream to ``fp``...
- dumps: Serialize ``obj`` to a JSON formatted ``str``...
- load: Deserialize ``fp`` (a ``.read()``-supporting file-like object...
- loads: Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance...

Classes (3 total):
- JSONDecodeError: Subclass of ValueError with the following additional properties...
- JSONDecoder: Simple JSON decoder...
- JSONEncoder: Extensible JSON encoder for Python data structures...

Submodules (4 total):
- codecs
- decoder
- encoder
- scanner
```

## Prompt Customization

### Available Prompts
All prompts are available in the `sagely.prompts` module:

```python
from sagely.prompts import (
    INITIAL_RESPONSE_PROMPT,
    ORCHESTRATOR_EVALUATION_PROMPT,
    FINAL_RESPONSE_WITH_WEB_PROMPT,
    FINAL_RESPONSE_WITHOUT_WEB_PROMPT,
    SYSTEM_MESSAGE_TEMPLATE
)
```

### Customizing Prompts
You can customize prompts for specific use cases:

```python
# Modify system message for specific domain
custom_system = SYSTEM_MESSAGE_TEMPLATE.format(module_name="pandas") + "\nFocus on data analysis."

# Create custom evaluation prompt
custom_eval = ORCHESTRATOR_EVALUATION_PROMPT + "\nAlso consider performance implications."
```

### Prompt Templates
All prompts use Python's string formatting with named parameters:
- `{question}`: User's question
- `{module_name}`: Target module name
- `{answer}`: Current answer for evaluation
- `{traceback}`: Recent error traceback
- `{context_summary}`: Summary of context object
- `{module_info}`: Analyzed module information
- `{initial_answer}`: Initial response
- `{web_results}`: Web search results

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

### Adding New Prompts

```python
# In sagely.prompts
CUSTOM_PROMPT = """
Custom prompt template with {parameter1} and {parameter2}.
"""

# In your agent
from .prompts import CUSTOM_PROMPT
prompt = CUSTOM_PROMPT.format(parameter1="value1", parameter2="value2")
```

## Dependencies

The enhanced LangGraph agent requires these additional dependencies:
- `langgraph>=0.0.20`
- `langchain-openai>=0.0.5`
- `langchain-core>=0.1.0`
- `requests>=2.25.0`

These are automatically included when installing Sagely.

## Examples

See the following example files:
- `examples/enhanced_agent_example.py`: Complete usage examples demonstrating the enhanced agent
- `examples/prompts_example.py`: Examples of using prompts directly

## Performance Considerations

- **Caching**: All responses are cached to avoid repeated API calls
- **Conditional Web Search**: Web search only occurs when needed
- **Timeout Protection**: Web searches have 10-second timeout
- **Multiple Queries**: Uses multiple search strategies for comprehensive results
- **Smart Module Analysis**: Comprehensive analysis with intelligent truncation
- **Separated Prompts**: Easy to customize and maintain prompts without code changes 