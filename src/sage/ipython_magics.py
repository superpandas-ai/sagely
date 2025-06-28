def load_ipython_extension(ipython):
    """
    Load the Sage extension for IPython.
    This registers the %sage magic command.
    """
    try:
        from IPython.core.magic import register_line_magic
        def sage_magic(line):
            """
            Magic command to ask Sage about a module.
            Usage:
                %sage pandas how to merge dataframes?
                %sage numpy generate random numbers
            """
            parts = line.strip().split()
            if len(parts) < 2:
                print("Usage: %sage <module> <question>")
                return
            module_name = parts[0]
            question = ' '.join(parts[1:])
            from sage.agent import SageAgent
            agent = SageAgent()
            return agent.ask(module_name, question)
        register_line_magic(sage_magic)
        print("Sage extension loaded. Use %sage <module> <question> to ask questions.")
    except Exception:
        pass 