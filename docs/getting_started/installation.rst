Installation
===========

This guide will walk you through installing Sagely and setting up all required dependencies.

Prerequisites
------------

* Python 3.8 or higher
* pip (Python package installer)
* OpenAI API key

Installing Sagely
----------------

Install Sagely using pip:

.. code-block:: bash

   pip install sagely

Or install from the latest development version:

.. code-block:: bash

   pip install git+https://github.com/superpandas-ai/sagely.git

For development installation with all dependencies:

.. code-block:: bash

   git clone https://github.com/superpandas-ai/sagely.git
   cd sagely
   pip install -e ".[dev]"

API Key Setup
-------------

Sagely requires an OpenAI API key to function. You can set it up in several ways:

**Environment Variable (Recommended):**

.. code-block:: bash

   export OPENAI_API_KEY='your-api-key-here'

**In your shell profile (bash/zsh):**

Add to your ``~/.bashrc`` or ``~/.zshrc``:

.. code-block:: bash

   echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc
   source ~/.bashrc

**In Python (temporary):**

.. code-block:: python

   import os
   os.environ['OPENAI_API_KEY'] = 'your-api-key-here'

**Using a .env file:**

Create a ``.env`` file in your project directory:

.. code-block:: text

   OPENAI_API_KEY=your-api-key-here

Then load it in your Python code:

.. code-block:: python

   from dotenv import load_dotenv
   load_dotenv()

Optional Dependencies
--------------------

**Tavily API Key (for enhanced web search):**

If you want to use Tavily as your web search provider:

.. code-block:: bash

   export TAVILY_API_KEY='your-tavily-api-key'

**LangSmith API Key (for tracing):**

For debugging and monitoring with LangSmith:

.. code-block:: bash

   export LANGCHAIN_TRACING_V2=true
   export LANGCHAIN_API_KEY='your-langsmith-api-key'
   export LANGCHAIN_PROJECT='your-project-name'

Verifying Installation
---------------------

To verify that Sagely is installed correctly:

.. code-block:: python

   import sagely
   print(f"Sagely version: {sagely.__version__}")

You should see the version number printed without any errors.

Testing Basic Functionality
--------------------------

Test that everything is working:

.. code-block:: python

   import sagely
   import json
   
   # This should work and print an answer
   json.sage.ask("What is the difference between json.dumps and json.dump?")

If you see a helpful response, your installation is working correctly!

Troubleshooting
--------------

**Import Error: No module named 'sagely'**

Make sure you installed Sagely in the correct Python environment:

.. code-block:: bash

   python -c "import sagely; print('Sagely is installed')"

**OpenAI API Key Error**

Verify your API key is set correctly:

.. code-block:: python

   import os
   print(f"API Key set: {'OPENAI_API_KEY' in os.environ}")
   if 'OPENAI_API_KEY' in os.environ:
       print(f"Key starts with: {os.environ['OPENAI_API_KEY'][:10]}...")

**Permission Errors**

If you encounter permission errors during installation, try:

.. code-block:: bash

   pip install --user sagely

Or use a virtual environment:

.. code-block:: bash

   python -m venv sagely_env
   source sagely_env/bin/activate  # On Windows: sagely_env\Scripts\activate
   pip install sagely

**Jupyter Integration Issues**

If IPython magic commands don't work:

.. code-block:: python

   %load_ext sagely
   %sagely json what is json?

Make sure you have IPython installed:

.. code-block:: bash

   pip install ipython

Next Steps
----------

Now that you have Sagely installed, check out:

* :doc:`quick_start` - Get up and running in minutes
* :doc:`basic_usage` - Learn the fundamental concepts
* :doc:`../user_guide/index` - Comprehensive usage guide 