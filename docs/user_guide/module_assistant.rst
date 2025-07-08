Module Assistant
===============

The module assistant is the core feature of Sagely. Every Python module you import automatically gets a `.sage` assistant attached to it, allowing you to ask questions about the module's functionality, usage patterns, and get help with errors.

Basic Usage
----------

**Simple Questions**

.. code-block:: python

   import sagely
   import pandas as pd
   
   # Ask about basic functionality
   pd.sage.ask("How do I read a CSV file?")
   
   # Ask about specific methods
   pd.sage.ask("What does the groupby method do?")
   
   # Ask about data structures
   pd.sage.ask("What is the difference between Series and DataFrame?")

**Object-Specific Questions**

You can ask questions about specific objects you've created:

.. code-block:: python

   import pandas as pd
   
   # Create a DataFrame
   df = pd.DataFrame({
       'A': [1, 2, 3, 4],
       'B': ['a', 'b', 'c', 'd'],
       'C': [1.1, 2.2, 3.3, 4.4]
   })
   
   # Ask about this specific DataFrame
   df.sage.ask("What are the data types of the columns?")
   df.sage.ask("How do I get the shape of this DataFrame?")
   df.sage.ask("What operations can I perform on this data?")

**Error Context Questions**

Sagely automatically captures recent errors and provides context-aware help:

.. code-block:: python

   import numpy as np
   
   try:
       # This will cause an error
       result = np.array([1, 2, 3]) + "string"
   except TypeError:
       # Sagely will include the TypeError context in its response
       np.sage.ask("How do I handle type errors in NumPy?")
       np.sage.ask("How do I convert arrays to strings?")

Advanced Usage
-------------

**Comparative Questions**

Ask about differences between modules or methods:

.. code-block:: python

   import pandas as pd
   import numpy as np
   
   # Compare modules
   pd.sage.ask("What's the difference between pandas and numpy for data analysis?")
   
   # Compare methods
   pd.sage.ask("When should I use merge vs join vs concat in pandas?")
   pd.sage.ask("What's the difference between apply and map methods?")

**Workflow Questions**

Ask about complete workflows and processes:

.. code-block:: python

   import matplotlib.pyplot as plt
   import pandas as pd
   
   # Ask about complete workflows
   plt.sage.ask("How do I create a complete data visualization workflow from data loading to saving?")
   pd.sage.ask("What's the complete process for cleaning and preprocessing a dataset?")

**Best Practices Questions**

Learn about recommended approaches:

.. code-block:: python

   import requests
   import pandas as pd
   
   # Ask about best practices
   requests.sage.ask("What are the best practices for making HTTP requests?")
   pd.sage.ask("What are the best practices for working with large datasets?")
   pd.sage.ask("How do I optimize pandas operations for performance?")

**Performance Questions**

Get help with optimization and performance:

.. code-block:: python

   import pandas as pd
   import numpy as np
   
   # Ask about performance
   pd.sage.ask("How do I optimize pandas operations for large datasets?")
   np.sage.ask("What are the most efficient ways to perform array operations?")
   pd.sage.ask("How do I handle memory issues with large DataFrames?")

Context Awareness
----------------

Sagely automatically captures and uses several types of context:

**Recent Exceptions**

.. code-block:: python

   import pandas as pd
   
   try:
       df = pd.read_csv("nonexistent.csv")
   except FileNotFoundError:
       # Sagely will know about the FileNotFoundError
       pd.sage.ask("How do I handle missing files when reading CSV?")
   
   try:
       result = df['column'] + 5
   except KeyError:
       # Sagely will know about the KeyError
       df.sage.ask("How do I check if a column exists before accessing it?")

**Object Information**

Sagely can analyze your objects and provide specific advice:

.. code-block:: python

   import pandas as pd
   
   df = pd.DataFrame({
       'A': [1, 2, None, 4],
       'B': ['a', 'b', 'c', None],
       'C': [1.1, 2.2, 3.3, 4.4]
   })
   
   # Sagely will know about the DataFrame structure
   df.sage.ask("How do I handle the missing values in this DataFrame?")
   df.sage.ask("What are the data types and how can I convert them?")

**Import History**

Sagely knows what modules you've imported and can provide cross-module advice:

.. code-block:: python

   import sagely
   import pandas as pd
   import numpy as np
   import matplotlib.pyplot as plt
   
   # Sagely can provide advice about using multiple libraries together
   pd.sage.ask("How do I use pandas with matplotlib for visualization?")
   np.sage.ask("How do I integrate numpy arrays with pandas DataFrames?")

Question Types
-------------

**How-to Questions**

.. code-block:: python

   pd.sage.ask("How do I merge two DataFrames?")
   pd.sage.ask("How do I filter data based on conditions?")
   pd.sage.ask("How do I group data and calculate statistics?")

**What-is Questions**

.. code-block:: python

   pd.sage.ask("What is a DataFrame?")
   pd.sage.ask("What is the difference between loc and iloc?")
   pd.sage.ask("What are the main data structures in pandas?")

**Why Questions**

.. code-block:: python

   pd.sage.ask("Why do I get SettingWithCopyWarning?")
   pd.sage.ask("Why is my merge not working as expected?")
   pd.sage.ask("Why is my code running slowly?")

**Best Practice Questions**

.. code-block:: python

   pd.sage.ask("What are the best practices for data cleaning?")
   pd.sage.ask("How should I structure my pandas code?")
   pd.sage.ask("What are the most efficient ways to work with pandas?")

**Troubleshooting Questions**

.. code-block:: python

   pd.sage.ask("How do I debug pandas operations?")
   pd.sage.ask("What are common pandas errors and how to fix them?")
   pd.sage.ask("How do I handle memory issues with large datasets?")

Tips for Effective Questions
---------------------------

**Be Specific**

Instead of asking "How do I use pandas?", ask specific questions:

.. code-block:: python

   # Good: Specific question
   pd.sage.ask("How do I merge two DataFrames on multiple columns?")
   
   # Better: Include context
   df1.sage.ask("How do I merge this DataFrame with another one on the 'id' column?")

**Include Context**

Let errors occur before asking questions:

.. code-block:: python

   try:
       result = some_operation()
   except SomeError:
       # Now ask about the error
       module.sage.ask("How do I fix this error?")

**Use Progressive Questions**

Build up from basic to advanced:

.. code-block:: python

   # Start with basics
   pd.sage.ask("What is a DataFrame?")
   
   # Then ask about operations
   pd.sage.ask("How do I perform basic operations on DataFrames?")
   
   # Finally ask about advanced features
   pd.sage.ask("How do I use advanced pandas features like multi-indexing?")

**Ask About Your Specific Data**

Reference your actual data:

.. code-block:: python

   df = pd.DataFrame(your_data)
   
   # Ask about your specific data
   df.sage.ask("How do I analyze this specific dataset?")
   df.sage.ask("What are the patterns in this data?")

Common Patterns
--------------

**Data Analysis Workflow**

.. code-block:: python

   import sagely
   import pandas as pd
   import numpy as np
   import matplotlib.pyplot as plt
   
   # 1. Data loading
   pd.sage.ask("How do I read data from different sources?")
   
   # 2. Data exploration
   df.sage.ask("How do I explore and understand this dataset?")
   
   # 3. Data cleaning
   df.sage.ask("How do I clean and preprocess this data?")
   
   # 4. Analysis
   df.sage.ask("How do I perform statistical analysis on this data?")
   
   # 5. Visualization
   plt.sage.ask("How do I create effective visualizations for this data?")

**Error Handling Pattern**

.. code-block:: python

   try:
       # Your code that might fail
       result = some_operation()
   except Exception as e:
       # Ask for help with the specific error
       module.sage.ask(f"How do I handle this {type(e).__name__} error?")
       module.sage.ask("What are the best practices for error handling?")

**Learning Pattern**

.. code-block:: python

   # Start with concepts
   module.sage.ask("What are the main concepts in this library?")
   
   # Learn basic operations
   module.sage.ask("What are the basic operations I can perform?")
   
   # Learn advanced features
   module.sage.ask("What are the advanced features and when should I use them?")
   
   # Learn best practices
   module.sage.ask("What are the best practices for using this library?")

Next Steps
----------

Now that you understand the module assistant, explore:

* :doc:`ipython_magic` - Using IPython magic commands
* :doc:`configuration` - Customizing Sagely's behavior
* :doc:`web_search` - Using web search for up-to-date information
* :doc:`caching` - Understanding caching behavior
* :doc:`status_updates` - Monitoring agent progress 