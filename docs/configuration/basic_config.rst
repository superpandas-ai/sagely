Basic Configuration
==================

Sagely provides a centralized configuration system that allows you to customize its behavior. This guide covers the basic configuration options and how to use them.

Quick Configuration
------------------

The easiest way to configure Sagely is through direct attribute assignment:

.. code-block:: python

   import sagely
   
   # Change the model
   sagely.config.model_name = "gpt-3.5-turbo"
   
   # Disable status updates
   sagely.config.show_status_updates = False
   
   # Disable line numbers in output
   sagely.config.show_line_numbers = False
   
   # Disable caching
   sagely.config.enable_response_cache = False

Available Configuration Options
-----------------------------

**Model Configuration**

.. code-block:: python

   import sagely
   
   # Set the LLM model to use
   sagely.config.model_name = "gpt-4"  # Default: "gpt-4.1-mini"
   sagely.config.model_name = "gpt-3.5-turbo"
   sagely.config.model_name = "gpt-4o"

**Display Configuration**

.. code-block:: python

   import sagely
   
   # Show/hide status updates during execution
   sagely.config.show_status_updates = True  # Default: True
   
   # Show/hide line numbers in console output
   sagely.config.show_line_numbers = True  # Default: True

**Cache Configuration**

.. code-block:: python

   import sagely
   
   # Enable/disable response caching
   sagely.config.enable_response_cache = True  # Default: True
   
   # Enable/disable module information caching
   sagely.config.enable_module_cache = True  # Default: True

**Web Search Configuration**

.. code-block:: python

   import sagely
   
   # Enable/disable web search
   sagely.config.enable_web_search = True  # Default: True
   
   # Set web search provider
   sagely.config.web_search_provider = "openai_websearch"  # Default
   sagely.config.web_search_provider = "tavily"
   
   # Set web search timeout
   sagely.config.web_search_timeout = 10  # Default: 10 seconds

**LangSmith Configuration**

.. code-block:: python

   import sagely
   
   # Enable/disable LangSmith tracing
   sagely.config.enable_langsmith_tracing = False  # Default: False
   
   # Set LangSmith project name
   sagely.config.langsmith_project = "my-sagely-project"  # Default: None

Programmatic Configuration
-------------------------

You can also configure Sagely programmatically using functions:

.. code-block:: python

   from sagely import get_config, update_config, reset_config
   
   # Get current configuration
   config = get_config()
   print(config.to_dict())
   
   # Update multiple settings at once
   update_config(
       model_name="gpt-3.5-turbo",
       show_status_updates=False,
       enable_web_search=False
   )
   
   # Reset to defaults
   reset_config()

Configuration Object
-------------------

The configuration object provides easy access to all settings:

.. code-block:: python

   import sagely
   
   # Access configuration object
   config = sagely.config
   
   # View all current settings
   print(f"Model: {config.model_name}")
   print(f"Status updates: {config.show_status_updates}")
   print(f"Line numbers: {config.show_line_numbers}")
   print(f"Response cache: {config.enable_response_cache}")
   print(f"Module cache: {config.enable_module_cache}")
   print(f"Web search: {config.enable_web_search}")
   print(f"Web search provider: {config.web_search_provider}")
   print(f"Web search timeout: {config.web_search_timeout}")
   print(f"LangSmith tracing: {config.enable_langsmith_tracing}")
   print(f"LangSmith project: {config.langsmith_project}")

Common Configuration Patterns
---------------------------

**Development Configuration**

For development with faster responses:

.. code-block:: python

   import sagely
   
   # Use faster model
   sagely.config.model_name = "gpt-3.5-turbo"
   
   # Disable web search for faster responses
   sagely.config.enable_web_search = False
   
   # Keep status updates for debugging
   sagely.config.show_status_updates = True

**Production Configuration**

For production with comprehensive responses:

.. code-block:: python

   import sagely
   
   # Use more capable model
   sagely.config.model_name = "gpt-4"
   
   # Enable web search for up-to-date information
   sagely.config.enable_web_search = True
   
   # Disable status updates for cleaner output
   sagely.config.show_status_updates = False

**Debugging Configuration**

For debugging and development:

.. code-block:: python

   import sagely
   
   # Enable all debugging features
   sagely.config.show_status_updates = True
   sagely.config.show_line_numbers = True
   sagely.config.enable_langsmith_tracing = True
   sagely.config.langsmith_project = "debug-session"
   
   # Disable caching to see fresh responses
   sagely.config.enable_response_cache = False
   sagely.config.enable_module_cache = False

**Performance Configuration**

For maximum performance:

.. code-block:: python

   import sagely
   
   # Use faster model
   sagely.config.model_name = "gpt-3.5-turbo"
   
   # Enable all caching
   sagely.config.enable_response_cache = True
   sagely.config.enable_module_cache = True
   
   # Disable web search for speed
   sagely.config.enable_web_search = False
   
   # Disable status updates
   sagely.config.show_status_updates = False

Configuration Validation
-----------------------

Sagely validates configuration values to ensure they're valid:

.. code-block:: python

   import sagely
   
   # Valid model names
   sagely.config.model_name = "gpt-4"  # ✅ Valid
   sagely.config.model_name = "gpt-3.5-turbo"  # ✅ Valid
   sagely.config.model_name = "gpt-4o"  # ✅ Valid
   
   # Invalid model name (will raise error)
   # sagely.config.model_name = "invalid-model"  # ❌ Error
   
   # Valid web search providers
   sagely.config.web_search_provider = "openai_websearch"  # ✅ Valid
   sagely.config.web_search_provider = "tavily"  # ✅ Valid
   
   # Invalid provider (will raise error)
   # sagely.config.web_search_provider = "invalid"  # ❌ Error

Configuration Scopes
-------------------

Configuration changes affect all future operations:

.. code-block:: python

   import sagely
   import pandas as pd
   
   # Change configuration
   sagely.config.model_name = "gpt-3.5-turbo"
   
   # This will use the new model
   pd.sage.ask("How do I read a CSV file?")
   
   # Change configuration again
   sagely.config.model_name = "gpt-4"
   
   # This will use the updated model
   pd.sage.ask("How do I merge DataFrames?")

Configuration Persistence
------------------------

Configuration can be saved and loaded between sessions:

.. code-block:: python

   import sagely
   from sagely import save_config, load_config
   
   # Set your preferred configuration
   sagely.config.model_name = "gpt-4"
   sagely.config.show_status_updates = False
   sagely.config.enable_web_search = True
   
   # Save configuration to file
   save_config()
   
   # In a new session, load the configuration
   load_config()
   
   # Configuration is now restored

Troubleshooting Configuration
----------------------------

**Configuration Not Taking Effect**

Make sure you're setting the configuration before using Sagely:

.. code-block:: python

   import sagely
   
   # Set configuration FIRST
   sagely.config.model_name = "gpt-3.5-turbo"
   
   # Then import and use modules
   import pandas as pd
   pd.sage.ask("How do I read a CSV file?")
   
   # NOT like this:
   # import pandas as pd
   # sagely.config.model_name = "gpt-3.5-turbo"  # Too late!
   # pd.sage.ask("How do I read a CSV file?")
```

**Invalid Configuration Values**

Check the error message for valid options:

.. code-block:: python

   import sagely
   
   try:
       sagely.config.model_name = "invalid-model"
   except ValueError as e:
       print(f"Error: {e}")
       print("Valid models: gpt-4, gpt-3.5-turbo, gpt-4o, etc.")

**Configuration Reset**

If you need to reset to defaults:

.. code-block:: python

   from sagely import reset_config
   
   # Reset all configuration to defaults
   reset_config()
   
   # Verify reset
   import sagely
   print(f"Model: {sagely.config.model_name}")  # Should be "gpt-4.1-mini"

Next Steps
----------

Now that you understand basic configuration, explore:

* :doc:`advanced_config` - Advanced configuration options
* :doc:`environment_variables` - Using environment variables
* :doc:`persistence` - Saving and loading configuration
* :doc:`cache_management` - Managing caches
* :doc:`web_search_config` - Web search configuration
* :doc:`langsmith_config` - LangSmith tracing configuration 