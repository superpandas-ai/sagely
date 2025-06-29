from .sage_agent import SageAgent
from .ipython_magics import load_ipython_extension
from .import_hook import install_hook

sage_agent = SageAgent()

install_hook(sage_agent)

__all__ = ["sage_agent", "load_ipython_extension"] 