from IPython.display import display, HTML
from rich.console import Console
from rich.syntax import Syntax
from rich.text import Text


def display_with_highlight(text, lexer=None):
    """
    Display text with syntax highlighting using Rich library.
    
    Args:
        text (str): The text to display with highlighting
        lexer (str, optional): The lexer to use for syntax highlighting. 
                              Defaults to "text" if None.
    
    Returns:
        str: The original text that was displayed
    """
    # Use Rich console for IPython display
    console = Console(force_terminal=True)
    
    # Determine lexer - map common lexers to Rich syntax names
    if lexer is None:
        syntax_lexer = "text"
    elif hasattr(lexer, '__name__'):
        # Handle pygments lexer objects
        lexer_name = lexer.__name__.lower()
        if 'python' in lexer_name:
            syntax_lexer = "python"
        elif 'json' in lexer_name:
            syntax_lexer = "json"
        elif 'yaml' in lexer_name or 'yml' in lexer_name:
            syntax_lexer = "yaml"
        elif 'markdown' in lexer_name or 'md' in lexer_name:
            syntax_lexer = "markdown"
        elif 'html' in lexer_name:
            syntax_lexer = "html"
        elif 'css' in lexer_name:
            syntax_lexer = "css"
        elif 'javascript' in lexer_name or 'js' in lexer_name:
            syntax_lexer = "javascript"
        else:
            syntax_lexer = "text"
    else:
        # Handle string lexer names
        syntax_lexer = str(lexer).lower()
    
    # Create Rich syntax object with highlighting
    syntax = Syntax(text, syntax_lexer, theme="monokai", line_numbers=True)
    
    # Display using Rich console
    console.print(syntax)
    
    # Return the original text
    return text 