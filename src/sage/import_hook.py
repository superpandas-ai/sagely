import sys
import types
from typing import Any


class SageAttribute:
    """Descriptor that provides the sage.ask functionality."""
    
    def __init__(self, agent):
        self.agent = agent
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        
        # Get the module name from the object
        module_name = getattr(obj, '__name__', None)
        if module_name is None:
            return self
        
        # Return a callable that can ask questions
        def ask(question, context_obj=None):
            return self.agent.ask(module_name, question, context_obj)
        
        return ask


def install_hook(agent):
    """Install the Sage import hook by adding sage attribute to modules."""
    
    def add_sage_to_module(module_name, module):
        """Add sage attribute to a module."""
        if not isinstance(module, types.ModuleType):
            return
        
        # Don't modify our own modules
        if module_name.startswith('sage'):
            return
        
        # Don't modify built-in modules
        if module_name in sys.builtin_module_names:
            return
        
        # Add sage attribute if it doesn't exist
        if not hasattr(module, 'sage'):
            module.sage = SageAttribute(agent)
    
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
    """Uninstall the Sage import hook."""
    # This would need to restore the original __import__ and remove sage attributes
    # For now, just a placeholder
    pass 