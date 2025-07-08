.. Sagely documentation master file, created by
   sphinx-quickstart on Tue Jan 14 10:00:00 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Sagely's documentation!
==================================

.. image:: _static/banner.png
   :alt: Sagely Banner
   :width: 100%
   :align: center

**LLM-powered assistant for every Python package!**

Just add ``.sage.ask("your question")`` to talk to any module.

.. raw:: html

   <div style="text-align: center; margin: 20px 0;">
     <a href="https://pypi.org/project/sagely/">
       <img src="https://img.shields.io/pypi/v/sagely.svg?color=blue" alt="PyPI version">
     </a>
     <a href="https://github.com/superpandas-ai/sagely">
       <img src="https://img.shields.io/github/stars/superpandas-ai/sagely?style=social" alt="GitHub stars">
     </a>
   </div>

Sagely Agent automatically injects a ``.sage`` assistant into every package you import. Ask questions about the library you're using, get help with errors, and explore code with syntax-highlighted answers — all powered by an LLM.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started/index
   user_guide/index
   api_reference/index
   configuration/index
   examples/index
   advanced/index
   contributing/index

.. admonition:: Quick Start

   **Install Sagely:**
   
   .. code-block:: bash
   
      pip install sagely
   
   **Set up your API key:**
   
   .. code-block:: bash
   
      export OPENAI_API_KEY='your-api-key-here'
   
   **Start using it:**
   
   .. code-block:: python
   
      import sagely
      import matplotlib
      
      matplotlib.sage.ask("how to make a scatter plot?")

.. admonition:: Why Sagely?

   There are thousands of Python libraries, but their docs aren't always intuitive. Moreover, getting help about errors or finding usage requires (at least) asking an LLM manually. With Sagely, you can do all that right from the REPL or the Jupyter notebook:

   * You don't need to search Stack Overflow, or ask ChatGPT, every time you forget a method or run into an error.
   * You get context-aware help, including recent exceptions and object summaries.
   * It's built for exploration — whether you're using a notebook, or REPL.

.. admonition:: Key Features

   * 🧠 Ask any module ``.sage.ask("How do I do X?")`` (prints the answer)
   * 💡 Smart context: recent errors + object summaries
   * 🧩 Auto-attaches to every import
   * 💾 Caches answers to avoid repeated API calls
   * 📦 Caches module analysis for faster subsequent queries
   * 🎨 Syntax-highlighted output with `rich`
   * 🧠 IPython magic: ``%sagely pandas how to merge?``
   * 🔍 **Real-time status updates** showing agent flow progress
   * 🌐 **Web search integration** with multiple providers
   * 📊 **LangSmith tracing** for debugging and monitoring
   * ⚙️ **Centralized configuration system** for customizing agent behavior
   * 💰 **Token usage tracking** with model-specific breakdowns
   * 📈 **Usage analytics** with session management and historical data

.. admonition:: Requirements

   * OpenAI API key (set as ``OPENAI_API_KEY`` environment variable)
   * Tavily API key (optional, for Tavily web search provider)
   * LangSmith API key (optional, for tracing)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 