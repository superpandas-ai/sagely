Your First Example
=================

Let's walk through a complete example to get you familiar with Sagely. We'll work with pandas to demonstrate the key features.

Step 1: Setup
-------------

First, make sure you have Sagely installed and your API key configured:

.. code-block:: python

   import sagely
   import pandas as pd
   
   # Verify everything is working
   print("Sagely is ready!")

Step 2: Basic Question
---------------------

Let's start with a simple question about pandas:

.. code-block:: python

   pd.sage.ask("What is a DataFrame and how do I create one?")

You should see:
1. Status updates showing what Sagely is doing
2. A comprehensive answer with code examples
3. Syntax-highlighted output

Step 3: Working with Data
------------------------

Now let's create some data and ask questions about it:

.. code-block:: python

   # Create a sample DataFrame
   data = {
       'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
       'Age': [25, 30, 35, 28],
       'City': ['New York', 'London', 'Paris', 'Tokyo'],
       'Salary': [50000, 60000, 70000, 55000]
   }
   df = pd.DataFrame(data)
   
   # Ask about the DataFrame
   df.sage.ask("What are the basic operations I can perform on this DataFrame?")

Step 4: Error Context
--------------------

Let's see how Sagely handles errors:

.. code-block:: python

   try:
       # This will cause an error
       result = df['Age'] + "years"
   except TypeError:
       # Now ask about the error
       df.sage.ask("How do I convert the Age column to string and add 'years'?")

Step 5: Data Analysis
--------------------

Let's perform some analysis and ask for help:

.. code-block:: python

   # Calculate some statistics
   mean_age = df['Age'].mean()
   print(f"Average age: {mean_age}")
   
   # Ask about more advanced analysis
   df.sage.ask("How do I group by City and calculate average salary?")

Step 6: Visualization
--------------------

Let's add visualization and ask for help:

.. code-block:: python

   import matplotlib.pyplot as plt
   
   # Create a simple plot
   plt.figure(figsize=(8, 6))
   df.plot(x='Name', y='Salary', kind='bar')
   plt.title('Salary by Name')
   plt.show()
   
   # Ask about improving the visualization
   plt.sage.ask("How do I make this bar chart more professional looking?")

Step 7: Advanced Operations
--------------------------

Let's explore more advanced pandas operations:

.. code-block:: python

   # Ask about data manipulation
   df.sage.ask("How do I create a new column that categorizes ages into groups?")
   
   # Ask about data filtering
   df.sage.ask("How do I filter this DataFrame to show only people over 30?")

Step 8: Best Practices
---------------------

Let's learn about best practices:

.. code-block:: python

   pd.sage.ask("What are the best practices for working with pandas DataFrames?")
   pd.sage.ask("How do I handle missing data effectively?")

Complete Example
---------------

Here's the complete example in one block:

.. code-block:: python

   import sagely
   import pandas as pd
   import matplotlib.pyplot as plt
   
   # Create sample data
   data = {
       'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
       'Age': [25, 30, 35, 28],
       'City': ['New York', 'London', 'Paris', 'Tokyo'],
       'Salary': [50000, 60000, 70000, 55000]
   }
   df = pd.DataFrame(data)
   
   # Basic operations
   df.sage.ask("What are the basic operations I can perform on this DataFrame?")
   
   # Data analysis
   df.sage.ask("How do I group by City and calculate average salary?")
   
   # Visualization
   plt.figure(figsize=(8, 6))
   df.plot(x='Name', y='Salary', kind='bar')
   plt.title('Salary by Name')
   plt.show()
   
   plt.sage.ask("How do I make this bar chart more professional looking?")
   
   # Best practices
   pd.sage.ask("What are the best practices for working with pandas DataFrames?")

What You've Learned
-------------------

In this example, you've experienced:

1. **Basic Usage**: How to ask questions about modules
2. **Context Awareness**: How Sagely understands your data and errors
3. **Status Updates**: Real-time feedback about what's happening
4. **Caching**: Responses are cached for future use
5. **Integration**: How Sagely works with multiple libraries
6. **Best Practices**: Learning recommended approaches

Key Takeaways
-------------

* **Simple Interface**: Just add `.sage.ask()` to any module
* **Contextual Help**: Sagely understands your specific situation
* **Progressive Learning**: Build on previous questions
* **Error Handling**: Get help when things go wrong
* **Best Practices**: Learn recommended approaches

Next Steps
----------

Now that you've completed your first example, try:

1. **Explore Other Libraries**: Try `numpy.sage.ask()`, `requests.sage.ask()`, etc.
2. **Ask Complex Questions**: Combine multiple concepts in one question
3. **Use IPython Magic**: Try `%sagely` commands in Jupyter
4. **Customize Settings**: Explore the configuration options
5. **Check the Examples**: Look at more advanced examples in the documentation

Remember, Sagely is designed to be your coding companion. Don't hesitate to ask questions about any aspect of the libraries you're using! 