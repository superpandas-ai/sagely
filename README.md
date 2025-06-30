<p align="center">
  <img src="https://raw.githubusercontent.com/superpandas-ai/sagely/main/assets/banner.png" alt="sagely Agent Banner" width="100%" />
</p>

<p align="center">
  <b>LLM-powered assistant for every Python package you import.</b><br/>
  Just add <code>.sage.ask("your question")</code> to any module.
</p>

<p align="center">
  <a href="https://pypi.org/project/sagely/">
    <img src="https://img.shields.io/pypi/v/sagely.svg?color=blue" alt="PyPI version">
  </a>
  <a href="https://github.com/superpandas-ai/sagely/actions">
    <img src="https://github.com/superpandas-ai/sagely/workflows/Tests/badge.svg" alt="CI Status">
  </a>
  <a href="https://github.com/superpandas-ai/sagely">
    <img src="https://img.shields.io/github/stars/superpandas-ai/sagely?style=social" alt="GitHub stars">
  </a>
</p>

---

# 🧠 sagely Agent

sagely Agent automatically injects a `.sage` assistant into every package you import. Ask questions about the library you're using, get help with errors, and explore code with syntax-highlighted answers — all powered by an LLM.

---

## 🎥 Demo

> _(Click to view full video)_

https://github.com/superpandas-ai/sagely/assets/demo.gif  
_or_  
https://loom.com/share/sagely-demo-link

---

## ❓ Why sagely?

There are thousands of Python libraries, but their docs aren't always intuitive. sagely fills that gap:

- You don't need to search Stack Overflow every time you forget a method.
- You get context-aware help, including recent exceptions and object summaries.
- It's built for exploration — whether you're using a notebook, REPL, or script.

---

## ✨ Features

- 🧠 Ask any module `.sage.ask("How do I do X?")` (prints the answer)
- 💡 Smart context: recent errors + object summaries
- 🧩 Auto-attaches to every import
- 💾 Caches answers to avoid repeated API calls
- 📦 Caches module analysis for faster subsequent queries
- 🎨 Syntax-highlighted output with `rich`
- 🧠 IPython magic: `%sagely pandas how to merge?`
- 🔍 **Real-time status updates** showing workflow progress
- 🌐 **Web search integration** with multiple providers (OpenAI web-search, Tavily)
- 📊 **LangSmith tracing** for debugging and monitoring
- ⚙️ **Centralized configuration system** for customizing agent behavior
- 🎛️ **Direct configuration access** via `sagely.config.attribute = value`
- 📝 **Configurable line numbers** in console display

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
> **Note**: Sagely currently uses OpenAI's models (GPT-4 by default), so you must have your OpenAI API key set in the environment.

### 3. Import It
```python
import sagely
```
It hooks into all future imports.

## 🧪 Usage Examples
### Inline Python
```python
import matplotlib

matplotlib.sage.ask("how to make a scatter plot?")  # This will print the answer, not return it
```

### In Jupyter / IPython
```python
%load_ext sagely

%sagely numpy how to generate random numbers?
```

### Programmatic
```python
from sagely import agent

agent.ask("requests", "how do I send a POST request?")  # Prints the answer, does not return it
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
- `model_name`: LLM model to use (default: "gpt-4")
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

Example:
```bash
export SAGELY_MODEL=gpt-4
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
```

The configuration file is automatically created with default settings if it doesn't exist.

#### Configuration Examples
Here are different ways to configure Sagely:

```python
import sagely

# Method 1: Direct attribute assignment (recommended)
sagely.config.model_name = "gpt-3.5-turbo"
sagely.config.show_status_updates = False
sagely.config.web_search_provider = "tavily"

# Method 2: Programmatic updates
from sagely.config import update_config
update_config(
    model_name="gpt-4",
    show_line_numbers=False,
    enable_web_search=True
)

# Method 3: Environment variables
# export SAGELY_MODEL=gpt-4
# export SAGELY_WEB_SEARCH_PROVIDER=openai_websearch

# Method 4: Configuration file
# Edit ~/.sagely/config.json directly
```

All methods work together - environment variables are loaded first, then the config file, and direct assignments take precedence.

## 🔧 Requirements
- OpenAI API key (set as `OPENAI_API_KEY` environment variable)
- Tavily API key (optional, for Tavily web search provider)
- openai
- ipywidgets
- rich
- ipython
- langgraph
- langchain-openai
- langchain-tavily (for Tavily web search)
- requests
- langsmith (optional, for tracing)

(Installed automatically.)

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
│   └── __init__.py
├── tests/
├── examples/                 # Usage examples
├── pyproject.toml
├── MANIFEST.in
└── README.md
```

## 🤝 Contributing
sagely is early-stage — PRs and ideas welcome!

- Want to support other LLMs?
- Want advanced caching or error tracing?
- Want to auto-annotate cells with answers?

Open an issue or submit a PR. 💥

## 🧷 License
MIT © 2025 SuperPandas Ltd 