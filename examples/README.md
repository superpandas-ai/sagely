# Sagely Example Notebooks

This directory contains interactive Jupyter notebooks demonstrating various features and functionalities of Sagely. Each notebook is designed to be self-contained and provides hands-on examples that you can run and experiment with.

## Available Notebooks

### 1. Basic LangGraph Agent (`getting_started_example.ipynb`)
Covers the fundamental usage of the LangGraph agent:
- Working with standard library modules
- Handling third-party modules
- Using different language models
- Examining agent features and capabilities

### 2. Enhanced Agent (`enhanced_agent_example.ipynb`)
Explores the enhanced agent with web search functionality:
- Basic vs. complex questions
- Web search integration
- Best practices queries
- Direct web search tool usage
- Workflow visualization and explanation

### 3. Configuration System (`config_example.ipynb`)
Demonstrates how to configure Sagely's behavior, including:
- Setting model preferences
- Toggling status updates and line numbers
- Managing cache settings
- Configuring web search providers (OpenAI vs Tavily)
- Direct configuration access via `sagely.config.attribute = value`
- Using environment variables
- Resetting to defaults

### 4. Module Cache System (`module_cache_example.ipynb`)
Demonstrates the module information caching system:
- First-time vs. cached analysis performance
- Cache status verification
- Clearing specific module cache
- Managing multiple module caches
- Cache persistence between sessions

### 5. Status Outputs (`status_outputs_example.ipynb`)
Shows how the LangGraph agent provides real-time feedback during execution:
- Basic question handling with status tracking
- Web search integration status
- Cache utilization feedback
- Module cache operations and status

### 6. Configuration Save/Load (`config_save_load_example.ipynb`)
Demonstrates the persistent configuration system:
- Saving configuration to `~/.sage/config.json`
- Loading configuration from file
- Automatic loading on startup
- Global functions for easy access
- Configuration file management
- Environment variable override behavior

## Getting Started

1. Make sure you have Jupyter installed in your environment
2. Install Sagely and its dependencies
3. You have OpenAI API key available.
4. Launch Jupyter Notebook or Jupyter Lab
5. Navigate to this directory
6. Open any notebook to start exploring

## Usage Tips

- Run the notebooks in order (1-6) for the best learning experience
- Each notebook is self-contained but may reference concepts from earlier notebooks
- Feel free to modify the examples and experiment with different inputs
- Pay attention to the markdown cells for explanations and context
- Use the status outputs to understand what's happening behind the scenes

## Requirements

- Python 3.8+
- Jupyter Notebook/Lab
- Sagely package and its dependencies
- Internet connection (for web search examples)
- OpenAI API key set as environment variable (`OPENAI_API_KEY`)

> **Note**: Sagely currently uses OpenAI's models (GPT-4 by default), so you must have your OpenAI API key set in the environment:
> ```bash
> export OPENAI_API_KEY='your-api-key-here'
> ```

## Note

These notebooks are designed to be both educational and practical. They serve as:
- Interactive documentation
- Learning resources
- Code examples
- Testing/verification tools

Feel free to use these notebooks as templates for your own Sagely applications! 