from IPython.display import display, HTML
from pygments import highlight
from pygments.lexers import PythonLexer, TextLexer
from pygments.formatters import HtmlFormatter


def display_with_highlight(text, lexer=None):
    lexer = lexer or TextLexer()
    formatter = HtmlFormatter(style="friendly", full=False, noclasses=True)
    highlighted = highlight(text, lexer, formatter)
    display(HTML(highlighted))
    return text 