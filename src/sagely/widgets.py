from IPython.display import display, HTML
from rich.console import Console
from rich.syntax import Syntax
from rich.text import Text
from .config import get_config


def display_with_highlight(text, lexer=None, show_line_numbers=None):
    """
    Display text with syntax highlighting using Rich library.
    
    Args:
        text (str): The text to display with highlighting
        lexer (str, optional): The lexer to use for syntax highlighting. 
                              Defaults to "text" if None.
        show_line_numbers (bool, optional): Whether to show line numbers.
                                           If None, uses configuration setting.
    
    Returns:
        str: The original text that was displayed
    """
    # Use Rich console for IPython display
    console = Console(force_terminal=True)
    
    # Get configuration for line numbers if not specified
    if show_line_numbers is None:
        config = get_config()
        show_line_numbers = config.show_line_numbers
    
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
    syntax = Syntax(text, syntax_lexer, theme="monokai", line_numbers=show_line_numbers)
    
    # Display using Rich console
    console.print(syntax)
    
    # Return the original text
    return text 