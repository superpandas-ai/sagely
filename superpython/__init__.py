from .agent import SuperPythonAgent
from .ipython_magics import load_ipython_extension
from .import_hook import install_hook

agent = SuperPythonAgent()

install_hook(agent)

__all__ = ["agent", "load_ipython_extension"] 