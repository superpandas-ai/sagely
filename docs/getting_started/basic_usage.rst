Basic Usage
==========

This guide covers the fundamental concepts and patterns for using Sagely effectively.

Core Concepts
------------

**Module Assistant**
Every Python module you import automatically gets a `.sage` assistant attached to it. This assistant can answer questions about the module's functionality, usage patterns, and help with errors.

**Context Awareness**
Sagely automatically captures:
- Recent exceptions and tracebacks
- Object summaries and types
- Module documentation and structure
- Import history

**Caching**
Sagely uses two types of caching:
- **Response Cache**: Stores answers to avoid repeated API calls
- **Module Cache**: Stores analyzed module information for faster subsequent queries

Basic Patterns
-------------

**1. Module Questions**

The most common pattern is asking questions about imported modules:

.. code-block:: python

   import sagely
   import pandas as pd
   
   # Ask about functionality
   pd.sage.ask("How do I read a CSV file?")
   
   # Ask about specific methods
   pd.sage.ask("What does the groupby method do?")
   
   # Ask about errors
   pd.sage.ask("Why do I get SettingWithCopyWarning?")

**2. Error Context**

Sagely automatically includes recent errors in its responses:

.. code-block:: python

   import numpy as np
   
   try:
       result = np.array([1, 2, 3]) + "string"
   except TypeError:
       # Sagely will include the TypeError context
       np.sage.ask("How do I handle type errors in NumPy?")

**3. Object-Specific Questions**

You can ask questions about specific objects:

.. code-block:: python

   import pandas as pd
   
   df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
   
   # Ask about the specific DataFrame
   df.sage.ask("How do I get the shape of this DataFrame?")
   df.sage.ask("What are the data types of the columns?")

**4. Comparative Questions**

Ask about differences between modules or methods:

.. code-block:: python

   import pandas as pd
   import numpy as np
   
   pd.sage.ask("What's the difference between pandas and numpy for data analysis?")
   pd.sage.ask("When should I use merge vs join vs concat?")

Advanced Patterns
----------------

**1. Chaining Questions**

Build on previous answers:

.. code-block:: python

   import pandas as pd
   
   # First, learn about reading data
   pd.sage.ask("How do I read different file formats?")
   
   # Then, ask about processing
   pd.sage.ask("How do I clean and preprocess the data?")
   
   # Finally, ask about analysis
   pd.sage.ask("How do I perform statistical analysis on the data?")

**2. Workflow Questions**

Ask about complete workflows:

.. code-block:: python

   import matplotlib.pyplot as plt
   import pandas as pd
   
   plt.sage.ask("How do I create a complete data visualization workflow from data loading to saving?")

**3. Best Practices**

Ask about recommended approaches:

.. code-block:: python

   import requests
   
   requests.sage.ask("What are the best practices for making HTTP requests?")
   requests.sage.ask("How do I handle rate limiting and retries?")

**4. Performance Questions**

Ask about optimization:

.. code-block:: python

   import pandas as pd
   
   pd.sage.ask("How do I optimize pandas operations for large datasets?")
   pd.sage.ask("What are the most efficient ways to filter and group data?")

IPython Magic Commands
---------------------

For Jupyter notebooks and IPython, you can use magic commands:

.. code-block:: python

   %load_ext sagely
   
   # Ask about any module (even if not imported)
   %sagely numpy how to create arrays?
   %sagely pandas how to handle missing data?
   %sagely matplotlib how to customize plots?

Programmatic Usage
-----------------

For more control, use the programmatic interface:

.. code-block:: python

   from sagely import agent
   
   # Ask about any module by name
   response = agent.ask("requests", "How do I handle authentication?")
   
   # The response is returned as a string
   print(response)

Configuration
-------------

You can customize Sagely's behavior:

.. code-block:: python

   import sagely
   
   # Disable status updates
   sagely.config.show_status_updates = False
   
   # Change the model
   sagely.config.model_name = "gpt-3.5-turbo"
   
   # Disable caching
   sagely.config.enable_response_cache = False

Best Practices
-------------

**1. Be Specific**
Instead of asking "How do I use pandas?", ask "How do I merge two DataFrames on a specific column?"

**2. Include Context**
When asking about errors, let the error occur first, then ask the question.

**3. Use Progressive Questions**
Start with basic concepts, then build up to more complex workflows.

**4. Leverage Caching**
Don't worry about asking the same question multiple times - Sagely caches responses.

**5. Check Status Updates**
Enable status updates to understand what Sagely is doing behind the scenes.

Common Use Cases
----------------

**Data Analysis Workflow:**

.. code-block:: python

   import sagely
   import pandas as pd
   import numpy as np
   import matplotlib.pyplot as plt
   
   # 1. Data loading
   pd.sage.ask("How do I read data from different sources?")
   
   # 2. Data exploration
   pd.sage.ask("How do I explore and understand my dataset?")
   
   # 3. Data cleaning
   pd.sage.ask("How do I handle missing values and outliers?")
   
   # 4. Analysis
   np.sage.ask("How do I perform statistical analysis?")
   
   # 5. Visualization
   plt.sage.ask("How do I create effective visualizations?")

**Web Development:**

.. code-block:: python

   import sagely
   import requests
   import json
   
   # API interactions
   requests.sage.ask("How do I build a robust API client?")
   
   # Data handling
   json.sage.ask("How do I handle complex JSON structures?")

**Machine Learning:**

.. code-block:: python

   import sagely
   import sklearn
   import pandas as pd
   
   # Data preparation
   pd.sage.ask("How do I prepare data for machine learning?")
   
   # Model training
   sklearn.sage.ask("How do I train and evaluate models?")

Next Steps
----------

Now that you understand the basics, explore:

* :doc:`../user_guide/index` - Advanced usage patterns
* :doc:`../configuration/index` - Customizing Sagely
* :doc:`../examples/index` - Real-world examples 