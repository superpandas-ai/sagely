<!-- <p align="center">
  <img src="https://raw.githubusercontent.com/superpandas-ai/sagely/main/assets/banner.png" alt="sagely Agent Banner" width="100%" />
</p> -->

<p align="center">
  <b>LLM-powered assistant for every Python package!</b><br/>
  Just add <code>.sage.ask("your question")</code> to talk to any module.
</p>

<p align="center">
  <a href="https://pypi.org/project/sagely/">
    <img src="https://img.shields.io/pypi/v/sagely.svg?color=blue" alt="PyPI version">
  </a>
  <!-- <a href="https://github.com/superpandas-ai/sagely/actions">
    <img src="https://github.com/superpandas-ai/sagely/workflows/Tests/badge.svg" alt="CI Status">
  </a> -->
  <a href="https://github.com/superpandas-ai/sagely">
    <img src="https://img.shields.io/github/stars/superpandas-ai/sagely?style=social" alt="GitHub stars">
  </a>
</p>

---

# 🧠 Sagely Agent

Sagely Agent automatically injects a `.sage` assistant into every package you import. Ask questions about the library you're using, get help with errors, and explore code with syntax-highlighted answers — all powered by an LLM.

---

## 🎥 Demo (TODO!)

> _(Click to view full video)_

https://github.com/superpandas-ai/sagely/assets/demo.gif  
_or_  
https://loom.com/share/sagely-demo-link

---

## ❓ Why Sagely?

There are thousands of Python libraries, but their docs aren't always intuitive. Moreover, getting help about errors or finding usage requires (atleast) asking an LLM manually. With sagely, you can do all that right from the REPL or the jupyter notebook:

- You don't need to search Stack Overflow, or ask ChatGPT, every time you forget a method or run into an error.
- You get context-aware help, including recent exceptions and object summaries.
- It's built for exploration — whether you're using a notebook, or REPL.

---

## ✨ Features

- 🧠 Ask any module `.sage.ask("How do I do X?")` (prints the answer)
- 💡 Smart context: recent errors + object summaries
- 🧩 Auto-attaches to every import
- 💾 Caches answers to avoid repeated API calls
- 📦 Caches module analysis for faster subsequent queries
- 🎨 Syntax-highlighted output with `rich`
- 🧠 IPython magic: `%sagely pandas how to merge?`
- 🔍 **Real-time status updates** showing agent flow progress
- 🌐 **Web search integration** with multiple providers (OpenAI web-search, Tavily)
- 📊 **LangSmith tracing** for debugging and monitoring
- ⚙️ **Centralized configuration system** for customizing agent behavior
- 🎛️ **Direct configuration access** via `sagely.config.attribute = value`
- 📝 **Configurable line numbers** in console display
- 💰 **Token usage tracking** with model-specific breakdowns and persistent storage
- 📈 **Usage analytics** with session management and historical data
- 🔄 **Real-time usage display** in status updates

---

## 🚀 Getting Started

### 1. Install

```bash
pip install sagely
```

### 2. Set up OpenAI API Key
```bash
export OPENAI_API_KEY='your-api-key-here'
```
> **Note**: Sagely currently uses OpenAI's models (gpt-4.1-mini by default), so you must have your OpenAI API key set in the environment. Later we plan to introduce other LLM providers.

### 3. Import It
```python
import sagely
```
It hooks into all future module imports.

## 🧪 Usage Examples
### Inline Python
```python
import matplotlib

matplotlib.sage.ask("how to make a scatter plot?")  # This will print the answer
```

### In Jupyter / IPython
```python
%load_ext sagely

%sagely numpy how to generate random numbers?
```

### Programmatic
```python
from sagely import agent

agent.ask("requests", "how do I send a POST request?")  # Prints the answer
```

### Status Outputs
The agent provides real-time feedback about what it's doing:

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

### ⚙️ Configuration System
Sagely provides a centralized configuration system for customizing agent behavior, model selection, cache management, and more.

#### Direct Configuration Access (Recommended)
The easiest way to configure Sagely is through direct attribute assignment:

```python
import sagely

# Direct configuration updates
sagely.config.enable_module_cache = False
sagely.config.show_line_numbers = False
sagely.config.model_name = "gpt-3.5-turbo"
sagely.config.web_search_provider = "tavily"
sagely.config.show_status_updates = False

# Changes take effect immediately and affect all future operations
```

#### Programmatic Configuration
```python
from sagely import get_config, update_config, clear_caches, clear_module_cache, reset_config, SageAgent

# View current configuration
config = get_config()
print(config.to_dict())

# Update configuration (e.g., change model, disable status updates)
update_config(model_name="gpt-3.5-turbo", show_status_updates=False)

# Create a new agent with the updated model
agent = SageAgent(model_name=get_config().model_name)

# Reset configuration to defaults
reset_config()
```

#### Available Configuration Options
- `model_name`: LLM model to use (default: "gpt-4.1-mini")
- `show_status_updates`: Show status outputs (default: True)
- `show_line_numbers`: Show line numbers in console display (default: True)
- `enable_response_cache`: Enable/disable response caching (default: True)
- `enable_module_cache`: Enable/disable module info caching (default: True)
- `enable_web_search`: Enable/disable web search (default: True)
- `web_search_provider`: Web search provider ("openai_websearch" or "tavily", default: "openai_websearch")
- `web_search_timeout`: Timeout for web search requests (default: 10)
- `enable_langsmith_tracing`: Enable LangSmith tracing (default: False)
- `langsmith_project`: LangSmith project name (default: None)

#### Cache Management
Sagely uses two types of caches to improve performance:

1. **Response Cache**: Stores answers to questions to avoid repeated API calls
2. **Module Cache**: Stores analyzed module information for faster subsequent queries

To manage caches, import the cache functions:

```python
from sagely import clear_caches, clear_module_cache

# Clear all caches
clear_caches()

# Clear only response cache
clear_caches("response")

# Clear only module cache
clear_caches("module")

# Clear module cache for a specific module
clear_module_cache("json")

# Clear module cache for all modules
clear_module_cache()
```

#### Environment Variable Configuration
You can also configure Sagely using environment variables:
- `SAGELY_MODEL`
- `SAGELY_SHOW_STATUS`
- `SAGELY_SHOW_LINE_NUMBERS`
- `SAGELY_ENABLE_RESPONSE_CACHE`
- `SAGELY_ENABLE_MODULE_CACHE`
- `SAGELY_ENABLE_WEB_SEARCH`
- `SAGELY_WEB_SEARCH_PROVIDER`
- `SAGELY_WEB_SEARCH_TIMEOUT`
- `SAGELY_ENABLE_LANGSMITH`
- `SAGELY_LANGSMITH_PROJECT`
- `TAVILY_API_KEY` (for Tavily web search)
- `OPENAI_API_KEY`

Example:
```bash
export SAGELY_MODEL=gpt-4.1-mini
export SAGELY_SHOW_STATUS=false
export SAGELY_SHOW_LINE_NUMBERS=false
export SAGELY_ENABLE_WEB_SEARCH=true
export SAGELY_WEB_SEARCH_PROVIDER=tavily
export SAGELY_WEB_SEARCH_TIMEOUT=15
export TAVILY_API_KEY=your-tavily-api-key
```

#### Web Search Providers
Sagely supports multiple web search providers for up-to-date information:

**OpenAI Web Search (Default)**
- Uses OpenAI's built-in web search tool
- No additional API key required (uses your OpenAI API key)
- Set with: `sagely.config.web_search_provider = "openai_websearch"`

**Tavily Search**
- Uses Tavily's search API for comprehensive web results
- Requires a Tavily API key: `export TAVILY_API_KEY=your-key`
- Set with: `sagely.config.web_search_provider = "tavily"`

The agent automatically rebuilds its workflow when you change the web search provider.

#### Configuration Persistence
Sagely automatically creates a configuration file at `~/.sagely/config.json` on first run with default settings. You can:

```python
# Save current configuration to file
from sagely.config import save_config
save_config()

# Load configuration from file
from sagely.config import load_config
load_config()

# Or use the global functions
from sagely import save_config, load_config
save_config()
load_config()
```

The configuration file is automatically created with default settings if it doesn't exist.

### 📊 LangSmith Tracing

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

3. **Enable tracing in configuration**:
   ```python
   import sagely
   sagely.config.enable_langsmith_tracing = True
   sagely.config.langsmith_project = "my-sagely-project"  # optional
   ```

4. **Run your code as usual**. All LangChain and LangGraph runs will be traced to your LangSmith dashboard.

For more details, see the [LangSmith docs](https://docs.smith.langchain.com/docs/tracing/).

### 🔧 Direct Tool Access

You can access the built-in tools directly for custom implementations:

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

### 📝 Prompt Customization

All prompts are available in the `sagely.prompts` module for customization:

```python
from sagely.prompts import (
    INITIAL_RESPONSE_PROMPT,
    ORCHESTRATOR_EVALUATION_PROMPT,
    FINAL_RESPONSE_WITH_WEB_PROMPT,
    FINAL_RESPONSE_WITHOUT_WEB_PROMPT,
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


## 📊 Token Usage Tracking

Sagely provides comprehensive token usage tracking to help you monitor your API costs and usage patterns. The system automatically tracks all LLM requests and stores detailed usage data both in-memory and in persistent JSON files.

### 🎯 Key Features

- **Automatic Tracking**: All LLM requests are automatically tracked
- **Model-Specific Tracking**: Usage is tracked separately for each LLM model
- **Real-Time Display**: Token usage is shown in status updates when enabled
- **Persistent Storage**: Usage data is saved to JSON files in `~/.sagely/usage_data/`
- **Session Management**: Each session gets a unique file with timestamp
- **Historical Analysis**: Access to all previous session data
- **Easy Integration**: Ready for Streamlit app integration

### 🚀 Quick Start

```python
import sagely

# Check current session usage
print(f"Total tokens used: {sagely.usage_data.total_tokens:,}")
print(f"Session ID: {sagely.usage_data.session_id}")

# Make some requests (usage is tracked automatically)
import requests
requests.sage.ask("How do I send a POST request?")

# Check updated usage
print(f"Updated tokens: {sagely.usage_data.total_tokens:,}")
```

### 📈 Usage Data Access

#### Via `sagely.usage_data` (Recommended)
The easiest way to access usage information:

```python
import sagely

# Basic usage information
print(f"Input tokens: {sagely.usage_data.input_tokens:,}")
print(f"Output tokens: {sagely.usage_data.output_tokens:,}")
print(f"Total tokens: {sagely.usage_data.total_tokens:,}")
print(f"Request count: {sagely.usage_data.request_count}")

# Session information
print(f"Session ID: {sagely.usage_data.session_id}")
print(f"File path: {sagely.usage_data.session_file_path}")

# Model-specific usage
for model_name, usage in sagely.usage_data.models.items():
    print(f"{model_name}: {usage.total_tokens:,} tokens")

# Get usage for specific model
gpt4_usage = sagely.usage_data.get_model_usage("gpt-4")
print(f"gpt-4 usage: {gpt4_usage.total_tokens:,} tokens")

# Get recent usage for a model
recent = sagely.usage_data.get_model_recent_usage("gpt-4o", 3)
for usage in recent:
    print(f"{usage.total_tokens} tokens ({usage.request_type})")

# Comprehensive summary
print(sagely.usage_data.summary)
```

#### Via Functions
```python
from sagely import (
    get_session_total, 
    get_session_summary, 
    get_model_usage,
    get_all_model_usage,
    get_session_id,
    get_session_file_path
)

# Get total usage
total = get_session_total()
print(f"Total: {total.total_tokens:,} tokens")

# Get formatted summary
print(get_session_summary())

# Get model-specific usage
gpt4_usage = get_model_usage("gpt-4")
print(f"gpt-4: {gpt4_usage.total_tokens:,} tokens")

# Get all models
all_models = get_all_model_usage()
for model_name, usage in all_models.items():
    print(f"{model_name}: {usage.total_tokens:,} tokens")
```

### 💾 File-Based Storage

Usage data is automatically saved to JSON files in `~/.sagely/usage_data/` with the following structure:

```
~/.sagely/
├── config.json
└── usage_data/
    ├── usage_20250709_000629.json
    ├── usage_20250709_000607.json
    ├── usage_20250709_000557.json
    └── ...
```

#### File Naming Convention
Files are named `usage_YYYYMMDD_HHMMSS.json` where:
- `YYYYMMDD` = Date (Year-Month-Day)
- `HHMMSS` = Time (Hour-Minute-Second)

This ensures no data overwrites and provides chronological ordering.

#### JSON Structure
```json
{
  "session_id": "20250709_000629",
  "session_start": "2025-07-09T00:06:29.375616",
  "usage_history": [
    {
      "input_tokens": 150,
      "output_tokens": 75,
      "total_tokens": 225,
      "timestamp": "2025-07-09T00:06:29.375696",
      "model_name": "gpt-4",
      "request_type": "initial_response"
    }
  ],
  "model_usage": {
    "gpt-4": {
      "input_tokens": 250,
      "output_tokens": 125,
      "total_tokens": 375,
      "timestamp": "2025-07-09T00:06:29.375700",
      "model_name": "gpt-4",
      "request_type": ""
    }
  }
}
```

### 📊 Session Management

#### Working with Session Files
```python
from sagely import (
    get_all_session_files,
    load_session_from_file,
    load_latest_session
)

# Get all session files (sorted by date, newest first)
session_files = get_all_session_files()
for file_path in session_files[:5]:  # Show first 5
    print(f"Session: {file_path.name}")

# Load specific session
loaded_tracker = load_session_from_file(session_files[0])
print(f"Loaded tokens: {loaded_tracker.get_session_total().total_tokens:,}")

# Load latest session
latest = load_latest_session()
print(f"Latest session: {latest.get_session_id()}")
```

#### Session Summary Example
```
Session Token Usage:
  Total input tokens: 1,234
  Total output tokens: 567
  Total tokens: 1,801
  Session duration: 0:05:30
  Total requests: 5

Model Breakdown:
  gpt-4:
    Input tokens: 800
    Output tokens: 400
    Total tokens: 1,200
    Requests: 3
  gpt-4o:
    Input tokens: 434
    Output tokens: 167
    Total tokens: 601
    Requests: 2
```

### 🔄 Usage Management

#### Clearing Usage Data
```python
from sagely import clear_usage_history, clear_model_history

# Clear all usage history
clear_usage_history()

# Clear history for specific model
clear_model_history("gpt-3.5-turbo")
```

#### Real-Time Status Updates
When `show_status_updates` is enabled, you'll see token usage in real-time:

```
💰 Tokens used: 150 input, 75 output, 225 total
💰 Tokens used: 200 input, 100 output, 300 total
💰 Tokens used: 100 input, 50 output, 150 total
```

### 🎛️ Configuration

Token usage tracking can be configured through the main configuration system:

```python
import sagely

# Enable/disable status updates (affects usage display)
sagely.config.show_status_updates = True

# The usage tracking itself is always enabled for data collection
# Status updates only control the display of usage information
```

### 📱 Streamlit Integration

The file-based storage system is designed for easy integration with Streamlit apps:

- **JSON Format**: Easy to parse and analyze
- **Historical Data**: Access to all previous sessions
- **Model Breakdown**: Detailed model-specific usage
- **Timestamp Data**: Precise timing information
- **Session Recovery**: Load any previous session

Example Streamlit data loading:
```python
import streamlit as st
import json
from pathlib import Path

# Load all session files
usage_dir = Path.home() / ".sagely" / "usage_data"
session_files = sorted(usage_dir.glob("usage_*.json"), reverse=True)

# Load and analyze data
for file_path in session_files:
    with open(file_path, 'r') as f:
        data = json.load(f)
        st.write(f"Session: {data['session_id']}")
        st.write(f"Total tokens: {sum(usage['total_tokens'] for usage in data['usage_history'])}")
```

### 🔍 Advanced Usage

#### Custom Usage Analysis
```python
from sagely import get_usage_tracker

# Get the usage tracker for advanced operations
tracker = get_usage_tracker()

# Get recent usage for specific model
recent_gpt4 = tracker.get_model_recent_usage("gpt-4", 10)

# Analyze usage patterns
for usage in recent_gpt4:
    print(f"{usage.timestamp}: {usage.total_tokens} tokens ({usage.request_type})")
```

#### Usage Statistics
```python
import sagely

# Quick usage check
if sagely.usage_data.total_tokens > 0:
    print(f"✅ Session active with {sagely.usage_data.total_tokens:,} tokens")
else:
    print("ℹ️ No tokens used yet")

# Model comparison
models = sagely.usage_data.models
if len(models) > 1:
    print("📊 Model usage comparison:")
    for model_name, usage in models.items():
        print(f"  {model_name}: {usage.total_tokens:,} tokens")
```


## 🔧 Requirements
- OpenAI API key (set as `OPENAI_API_KEY` environment variable)
- Tavily API key (optional, for Tavily web search provider)
- LangSmith API key (optional, for tracing)

### Dependencies
- openai
- ipywidgets
- rich
- ipython
- langgraph
- langchain-openai
- langchain-tavily (for Tavily web search)
- langchain-core
- requests
- langsmith (optional, for tracing)

(All dependencies are installed automatically.)

## 🧠 Project Structure
```text
sagely/
├── src/sagely/
│   ├── langgraph_agent.py    # Main LangGraph-based agent
│   ├── sage_agent.py         # High-level agent interface
│   ├── cache.py              # Caching system
│   ├── context.py            # Context gathering
│   ├── import_hook.py        # Import hooking
│   ├── ipython_magics.py     # IPython magic commands
│   ├── prompts.py            # Prompt templates
│   ├── tracing.py            # LangSmith tracing
│   ├── widgets.py            # Display utilities
│   ├── config.py             # Centralized configuration system
│   ├── usage_info.py         # Token usage tracking system
│   └── __init__.py
├── tests/
├── examples/                 # Usage examples in Jupyter notebooks
├── pyproject.toml
├── MANIFEST.in
└── README.md
```

### 📁 Data Storage
```text
~/.sagely/
├── config.json              # Configuration file
└── usage_data/              # Token usage data
    ├── usage_20250709_000629.json
    ├── usage_20250709_000607.json
    └── ...
```

## 🤝 Contributing
Sagely is early-stage — PRs and ideas welcome! 💥

We use [Featurebase](https://sagely.featurebase.app/) for product roadmap and feature requests/tracking

### 🚀 Future Features
- Support for other LLM Providers
- Advanced caching and error tracing
- Auto-annotation of cells with answers
- Better prompts and prompt management
- Async & Parallel Context Gathering
- Streaming Response for Jupyter/REPL
- Improved context for large modules using RAG/Summarization/Selective filtering
- Enhanced web search capabilities
- Custom agent workflows
- Integration with more development tools

## 🧷 License
MIT © 2025 SuperPandas Ltd 