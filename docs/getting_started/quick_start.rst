Quick Start
==========

Get up and running with Sagely in just a few minutes!

Basic Usage
----------

Once you have Sagely installed and your API key configured, you can start using it immediately:

.. code-block:: python

   import sagely
   import requests
   
   # Ask any module a question
   requests.sage.ask("How do I send a POST request?")

That's it! Sagely will automatically:

1. Analyze the `requests` module
2. Generate a helpful response
3. Display it with syntax highlighting
4. Cache the result for future use

Different Ways to Use Sagely
---------------------------

**1. Module Assistant (Most Common)**

.. code-block:: python

   import pandas as pd
   import numpy as np
   import matplotlib.pyplot as plt
   
   # Ask about any imported module
   pd.sage.ask("How do I merge two DataFrames?")
   np.sage.ask("What's the difference between array and asarray?")
   plt.sage.ask("How do I create a scatter plot?")

**2. IPython Magic Commands**

.. code-block:: python

   %load_ext sagely
   
   # Ask about any module (even if not imported)
   %sagely json how to parse JSON?
   %sagely pandas how to read CSV files?
   %sagely requests how to handle errors?

**3. Programmatic Usage**

.. code-block:: python

   from sagely import agent
   
   # Ask about any module by name
   agent.ask("numpy", "How do I create random arrays?")
   agent.ask("pandas", "What are the main data structures?")

**4. Error Context**

Sagely automatically captures recent errors and provides context-aware help:

.. code-block:: python

   import pandas as pd
   
   try:
       df = pd.read_csv("nonexistent.csv")
   except FileNotFoundError:
       # Sagely will include the error context in its response
       pd.sage.ask("How do I handle missing files when reading CSV?")

Real Examples
------------

**Working with Data Analysis:**

.. code-block:: python

   import sagely
   import pandas as pd
   import numpy as np
   
   # Create some sample data
   data = {'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8]}
   df = pd.DataFrame(data)
   
   # Ask for help with operations
   df.sage.ask("How do I calculate the mean of column A?")
   df.sage.ask("How do I filter rows where A > 2?")
   df.sage.ask("How do I create a new column C as A + B?")

**Web Development:**

.. code-block:: python

   import sagely
   import requests
   import json
   
   # Ask about API interactions
   requests.sage.ask("How do I send a GET request with parameters?")
   requests.sage.ask("How do I handle JSON responses?")
   json.sage.ask("How do I pretty print JSON data?")

**Visualization:**

.. code-block:: python

   import sagely
   import matplotlib.pyplot as plt
   import seaborn as sns
   
   # Ask about plotting
   plt.sage.ask("How do I create a line plot?")
   sns.sage.ask("How do I create a heatmap?")
   plt.sage.ask("How do I save a plot to a file?")

Status Updates
-------------

Sagely provides real-time feedback about what it's doing:

.. code-block:: python

   import sagely
   import requests
   
   # You'll see status updates like this:
   requests.sage.ask("How do I handle timeouts?")
   
   # Output includes:
   # ℹ️ Processing question about 'requests': How do I handle timeouts?...
   # ℹ️ Starting LangGraph workflow execution...
   # ℹ️ Starting context analysis for module: requests
   # ✅ Successfully analyzed module 'requests'
   # 🤔 Generating initial response...
   # ✅ Initial response generated
   # 📦 Answer cached for future use
   # ✅ Displaying final answer 