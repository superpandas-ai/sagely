def load_ipython_extension(ipython):
    """
    Load the SuperPython extension for IPython.
    This registers the %super magic command.
    """
    try:
        from IPython.core.magic import register_line_magic
        
        def super_magic(line):
            """
            Magic command to ask SuperPython about a module.
            Usage:
                %super pandas how to merge dataframes?
                %super numpy generate random numbers
            """
            parts = line.strip().split()
            if len(parts) < 2:
                print("Usage: %super <module> <question>")
                return
            module_name = parts[0]
            question = ' '.join(parts[1:])
            from .agent import SuperPythonAgent
            agent = SuperPythonAgent()
            return agent.ask(module_name, question)
        register_line_magic(super_magic)
        print("SuperPython extension loaded. Use %super <module> <question> to ask questions.")
    except Exception:
        # Not in IPython context or IPython not available
        pass 