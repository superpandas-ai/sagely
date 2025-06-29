import sys
import types
from typing import Any


class SageHelper:
    """Helper class that provides the .ask() method for modules."""
    def __init__(self, agent, module_name):
        self.agent = agent
        self.module_name = module_name
    
    def ask(self, question, context_obj=None):
        return self.agent.ask(self.module_name, question, context_obj)


def make_sage_function(agent, module_name):
    """Create a SageHelper object for a module."""
    return SageHelper(agent, module_name)


def install_hook(agent):
    """Install the sage import hook by adding sage attribute to modules."""
    
    def add_sage_to_module(module_name, module):
        """Add sage attribute to a module."""
        if not isinstance(module, types.ModuleType):
            return
        
        # Don't modify our own modules
        if module_name.startswith('sagely'):
            return
        
        # Don't modify built-in modules
        if module_name in sys.builtin_module_names:
            return
        
        # Skip private or deprecated modules (e.g., numpy.core, numpy.fft.helper, numpy.linalg.linalg)
        private_suffixes = ('.core', '.helper', '.linalg')
        if '._' in module_name or module_name.endswith(private_suffixes):
            return
        
        # Add sage attribute if it doesn't exist
        if not hasattr(module, 'sage'):
            module.sage = make_sage_function(agent, module_name)
    
    # Add sage to existing modules
    for module_name, module in sys.modules.items():
        add_sage_to_module(module_name, module)
    
    # Store the original __import__ function
    original_import = __builtins__['__import__']
    
    def sage_import(name, *args, **kwargs):
        """Wrapped __import__ that adds sage attribute to imported modules."""
        module = original_import(name, *args, **kwargs)
        add_sage_to_module(name, module)
        return module
    
    # Replace __import__ with our wrapped version
    __builtins__['__import__'] = sage_import
    
    return original_import


def uninstall_hook():
    """Uninstall the sage import hook."""
    # This would need to restore the original __import__ and remove sage attributes
    # For now, just a placeholder
    pass 