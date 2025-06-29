def load_ipython_extension(ipython):
    """
    Load the sagely extension for IPython.
    This registers the %sagely magic command.
    """
    try:
        from IPython.core.magic import register_line_magic
        def sage_magic(line):
            """
            Magic command to ask sagely about a module.
            Usage:
                %sagely pandas how to merge dataframes?
                %sagely numpy generate random numbers
            """
            parts = line.strip().split()
            if len(parts) < 2:
                print("Usage: %sagely <module> <question>")
                return
            module_name = parts[0]
            question = ' '.join(parts[1:])
            from sagely.agent import SageAgent
            agent = SageAgent()
            return agent.ask(module_name, question)
        register_line_magic(sage_magic)
        print("sagely extension loaded. Use %sagely <module> <question> to ask questions.")
    except Exception:
        pass 