Core API
========

This page documents the core API functions and classes in Sagely.

Main Functions
--------------

.. function:: sagely.agent.ask(module_name: str, question: str) -> str

   Ask a question about a specific module.
   
   **Parameters:**
   
   * **module_name** (str) - The name of the module to ask about
   * **question** (str) - The question to ask
   
   **Returns:**
   
   * **str** - The answer to the question
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import agent
      
      # Ask about a module
      answer = agent.ask("pandas", "How do I read a CSV file?")
      print(answer)
   
   **Note:** This function will automatically import the module if it's not already imported.

.. function:: sagely.get_config() -> SageConfig

   Get the current configuration object.
   
   **Returns:**
   
   * **SageConfig** - The current configuration object
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import get_config
      
      config = get_config()
      print(f"Current model: {config.model_name}")
      print(f"Status updates: {config.show_status_updates}")

.. function:: sagely.update_config(**kwargs) -> None

   Update multiple configuration settings at once.
   
   **Parameters:**
   
   * **kwargs** - Configuration key-value pairs to update
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import update_config
      
      # Update multiple settings
      update_config(
          model_name="gpt-3.5-turbo",
          show_status_updates=False,
          enable_web_search=True
      )

.. function:: sagely.reset_config() -> None

   Reset all configuration settings to their default values.
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import reset_config
      
      # Reset to defaults
      reset_config()

.. function:: sagely.save_config() -> None

   Save the current configuration to the configuration file.
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import save_config
      
      # Save current configuration
      save_config()

.. function:: sagely.load_config() -> None

   Load configuration from the configuration file.
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import load_config
      
      # Load saved configuration
      load_config()

Cache Management
----------------

.. function:: sagely.clear_caches(cache_type: str = "all") -> None

   Clear specified caches.
   
   **Parameters:**
   
   * **cache_type** (str, optional) - Type of cache to clear. Options: "all", "response", "module". Default: "all"
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import clear_caches
      
      # Clear all caches
      clear_caches()
      
      # Clear only response cache
      clear_caches("response")
      
      # Clear only module cache
      clear_caches("module")

.. function:: sagely.clear_module_cache(module_name: str = None) -> None

   Clear module cache for specific module or all modules.
   
   **Parameters:**
   
   * **module_name** (str, optional) - Name of specific module to clear cache for. If None, clears all module caches.
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import clear_module_cache
      
      # Clear cache for specific module
      clear_module_cache("pandas")
      
      # Clear all module caches
      clear_module_cache()

Usage Tracking
--------------

.. function:: sagely.get_session_total() -> UsageStats

   Get total usage statistics for the current session.
   
   **Returns:**
   
   * **UsageStats** - Usage statistics object
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import get_session_total
      
      stats = get_session_total()
      print(f"Total tokens: {stats.total_tokens}")
      print(f"Input tokens: {stats.input_tokens}")
      print(f"Output tokens: {stats.output_tokens}")

.. function:: sagely.get_session_summary() -> str

   Get a formatted summary of current session usage.
   
   **Returns:**
   
   * **str** - Formatted usage summary
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import get_session_summary
      
      summary = get_session_summary()
      print(summary)

.. function:: sagely.get_model_usage(model_name: str) -> UsageStats

   Get usage statistics for a specific model.
   
   **Parameters:**
   
   * **model_name** (str) - Name of the model to get usage for
   
   **Returns:**
   
   * **UsageStats** - Usage statistics for the specified model
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import get_model_usage
      
      gpt4_usage = get_model_usage("gpt-4")
      print(f"GPT-4 tokens: {gpt4_usage.total_tokens}")

.. function:: sagely.get_all_model_usage() -> Dict[str, UsageStats]

   Get usage statistics for all models used in the session.
   
   **Returns:**
   
   * **Dict[str, UsageStats]** - Dictionary mapping model names to usage statistics
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import get_all_model_usage
      
      all_usage = get_all_model_usage()
      for model_name, stats in all_usage.items():
          print(f"{model_name}: {stats.total_tokens} tokens")

.. function:: sagely.get_session_id() -> str

   Get the current session ID.
   
   **Returns:**
   
   * **str** - Current session ID
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import get_session_id
      
      session_id = get_session_id()
      print(f"Session ID: {session_id}")

.. function:: sagely.get_session_file_path() -> str

   Get the file path where current session usage data is stored.
   
   **Returns:**
   
   * **str** - File path for current session data
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import get_session_file_path
      
      file_path = get_session_file_path()
      print(f"Session file: {file_path}")

.. function:: sagely.clear_usage_history() -> None

   Clear all usage history for the current session.
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import clear_usage_history
      
      # Clear usage history
      clear_usage_history()

.. function:: sagely.clear_model_history(model_name: str) -> None

   Clear usage history for a specific model.
   
   **Parameters:**
   
   * **model_name** (str) - Name of the model to clear history for
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import clear_model_history
      
      # Clear history for specific model
      clear_model_history("gpt-3.5-turbo")

Session Management
-----------------

.. function:: sagely.get_all_session_files() -> List[Path]

   Get all session files sorted by date (newest first).
   
   **Returns:**
   
   * **List[Path]** - List of session file paths
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import get_all_session_files
      
      session_files = get_all_session_files()
      for file_path in session_files[:5]:  # Show first 5
          print(f"Session: {file_path.name}")

.. function:: sagely.load_session_from_file(file_path: Path) -> UsageTracker

   Load usage data from a specific session file.
   
   **Parameters:**
   
   * **file_path** (Path) - Path to the session file to load
   
   **Returns:**
   
   * **UsageTracker** - Usage tracker object with loaded data
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import get_all_session_files, load_session_from_file
      
      session_files = get_all_session_files()
      if session_files:
          tracker = load_session_from_file(session_files[0])
          print(f"Loaded tokens: {tracker.get_session_total().total_tokens}")

.. function:: sagely.load_latest_session() -> UsageTracker

   Load usage data from the most recent session file.
   
   **Returns:**
   
   * **UsageTracker** - Usage tracker object with latest session data
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import load_latest_session
      
      latest = load_latest_session()
      print(f"Latest session: {latest.get_session_id()}")

Core Classes
------------

.. class:: sagely.sage_agent.SageAgent

   The main agent class for handling questions about modules.
   
   **Parameters:**
   
   * **model_name** (str, optional) - The LLM model to use. Default: from configuration
   * **config** (SageConfig, optional) - Configuration object. Default: from global config
   
   **Methods:**
   
   .. method:: ask(module_name: str, question: str) -> str
      
      Ask a question about a specific module.
      
      **Parameters:**
      
      * **module_name** (str) - The name of the module to ask about
      * **question** (str) - The question to ask
      
      **Returns:**
      
      * **str** - The answer to the question
   
   **Example:**
   
   .. code-block:: python
   
      from sagely.sage_agent import SageAgent
      
      # Create agent with specific model
      agent = SageAgent(model_name="gpt-4")
      
      # Ask a question
      answer = agent.ask("pandas", "How do I read a CSV file?")
      print(answer)

.. class:: sagely.config.SageConfig

   Configuration class for Sagely settings.
   
   **Attributes:**
   
   * **model_name** (str) - The LLM model to use
   * **show_status_updates** (bool) - Whether to show status updates
   * **show_line_numbers** (bool) - Whether to show line numbers in output
   * **enable_response_cache** (bool) - Whether to enable response caching
   * **enable_module_cache** (bool) - Whether to enable module caching
   * **enable_web_search** (bool) - Whether to enable web search
   * **web_search_provider** (str) - Web search provider to use
   * **web_search_timeout** (int) - Web search timeout in seconds
   * **enable_langsmith_tracing** (bool) - Whether to enable LangSmith tracing
   * **langsmith_project** (str) - LangSmith project name
   
   **Methods:**
   
   .. method:: to_dict() -> Dict[str, Any]
      
      Convert configuration to dictionary.
      
      **Returns:**
      
      * **Dict[str, Any]** - Configuration as dictionary
   
   .. method:: from_dict(data: Dict[str, Any]) -> None
      
      Load configuration from dictionary.
      
      **Parameters:**
      
      * **data** (Dict[str, Any]) - Configuration data
   
   **Example:**
   
   .. code-block:: python
   
      from sagely.config import SageConfig
      
      # Create configuration
      config = SageConfig()
      config.model_name = "gpt-4"
      config.show_status_updates = False
      
      # Convert to dictionary
      config_dict = config.to_dict()
      print(config_dict)

.. class:: sagely.usage_info.UsageStats

   Class representing usage statistics.
   
   **Attributes:**
   
   * **input_tokens** (int) - Number of input tokens
   * **output_tokens** (int) - Number of output tokens
   * **total_tokens** (int) - Total number of tokens
   * **request_count** (int) - Number of requests
   * **model_name** (str) - Name of the model
   * **request_type** (str) - Type of request
   * **timestamp** (datetime) - Timestamp of the usage
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import get_session_total
      
      stats = get_session_total()
      print(f"Input tokens: {stats.input_tokens}")
      print(f"Output tokens: {stats.output_tokens}")
      print(f"Total tokens: {stats.total_tokens}")
      print(f"Request count: {stats.request_count}")

.. class:: sagely.usage_info.UsageTracker

   Class for tracking and managing usage data.
   
   **Methods:**
   
   .. method:: get_session_total() -> UsageStats
      
      Get total usage for the session.
      
      **Returns:**
      
      * **UsageStats** - Total usage statistics
   
   .. method:: get_model_usage(model_name: str) -> UsageStats
      
      Get usage for a specific model.
      
      **Parameters:**
      
      * **model_name** (str) - Name of the model
      
      **Returns:**
      
      * **UsageStats** - Usage statistics for the model
   
   .. method:: get_model_recent_usage(model_name: str, count: int = 10) -> List[UsageStats]
      
      Get recent usage for a specific model.
      
      **Parameters:**
      
      * **model_name** (str) - Name of the model
      * **count** (int) - Number of recent entries to return
      
      **Returns:**
      
      * **List[UsageStats]** - List of recent usage statistics
   
   .. method:: get_session_id() -> str
      
      Get the session ID.
      
      **Returns:**
      
      * **str** - Session ID
   
   **Example:**
   
   .. code-block:: python
   
      from sagely import get_usage_tracker
      
      tracker = get_usage_tracker()
      
      # Get total usage
      total = tracker.get_session_total()
      print(f"Total tokens: {total.total_tokens}")
      
      # Get model usage
      gpt4_usage = tracker.get_model_usage("gpt-4")
      print(f"GPT-4 tokens: {gpt4_usage.total_tokens}")
      
      # Get recent usage
      recent = tracker.get_model_recent_usage("gpt-4", 5)
      for usage in recent:
          print(f"{usage.timestamp}: {usage.total_tokens} tokens")

Module Attributes
-----------------

When you import Sagely, every module gets a `.sage` attribute that provides the assistant functionality:

.. attribute:: module.sage

   The Sage assistant attached to every imported module.
   
   **Methods:**
   
   .. method:: ask(question: str) -> None
      
      Ask a question about the module.
      
      **Parameters:**
      
      * **question** (str) - The question to ask
      
      **Note:** This method prints the answer directly to the console.
   
   **Example:**
   
   .. code-block:: python
   
      import sagely
      import pandas as pd
      
      # Ask about the module
      pd.sage.ask("How do I read a CSV file?")
      
      # Ask about specific functionality
      pd.sage.ask("What is the difference between merge and join?")

Configuration Object
--------------------

The main configuration object is available as:

.. attribute:: sagely.config

   The global configuration object for Sagely.
   
   **Example:**
   
   .. code-block:: python
   
      import sagely
      
      # Access configuration
      print(f"Model: {sagely.config.model_name}")
      print(f"Status updates: {sagely.config.show_status_updates}")
      
      # Modify configuration
      sagely.config.model_name = "gpt-3.5-turbo"
      sagely.config.show_status_updates = False

Usage Data Object
-----------------

Current session usage data is available as:

.. attribute:: sagely.usage_data

   The current session usage data object.
   
   **Attributes:**
   
   * **input_tokens** (int) - Total input tokens
   * **output_tokens** (int) - Total output tokens
   * **total_tokens** (int) - Total tokens
   * **request_count** (int) - Number of requests
   * **session_id** (str) - Current session ID
   * **session_file_path** (str) - Path to session file
   * **models** (Dict[str, UsageStats]) - Usage by model
   
   **Methods:**
   
   .. method:: get_model_usage(model_name: str) -> UsageStats
      
      Get usage for a specific model.
   
   .. method:: get_model_recent_usage(model_name: str, count: int = 10) -> List[UsageStats]
      
      Get recent usage for a specific model.
   
   .. method:: summary -> str
      
      Get a formatted summary of usage.
   
   **Example:**
   
   .. code-block:: python
   
      import sagely
      
      # Access usage data
      print(f"Total tokens: {sagely.usage_data.total_tokens}")
      print(f"Session ID: {sagely.usage_data.session_id}")
      
      # Get model usage
      gpt4_usage = sagely.usage_data.get_model_usage("gpt-4")
      print(f"GPT-4 tokens: {gpt4_usage.total_tokens}")
      
      # Get summary
      print(sagely.usage_data.summary) 