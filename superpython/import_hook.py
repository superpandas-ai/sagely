import sys
import types
from typing import Any


class SuperPythonAttribute:
    """Descriptor that provides the superpython.ask functionality."""
    
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
    """Install the SuperPython import hook by adding superpython attribute to modules."""
    
    def add_superpython_to_module(module_name, module):
        """Add superpython attribute to a module."""
        if not isinstance(module, types.ModuleType):
            return
        
        # Don't modify our own modules
        if module_name.startswith('superpython'):
            return
        
        # Don't modify built-in modules
        if module_name in sys.builtin_module_names:
            return
        
        # Add superpython attribute if it doesn't exist
        if not hasattr(module, 'superpython'):
            module.superpython = SuperPythonAttribute(agent)
    
    # Add superpython to existing modules
    for module_name, module in sys.modules.items():
        add_superpython_to_module(module_name, module)
    
    # Store the original __import__ function
    original_import = __builtins__['__import__']
    
    def superpython_import(name, *args, **kwargs):
        """Wrapped __import__ that adds superpython attribute to imported modules."""
        module = original_import(name, *args, **kwargs)
        add_superpython_to_module(name, module)
        return module
    
    # Replace __import__ with our wrapped version
    __builtins__['__import__'] = superpython_import
    
    return original_import


def uninstall_hook():
    """Uninstall the SuperPython import hook."""
    # This would need to restore the original __import__ and remove superpython attributes
    # For now, just a placeholder
    pass 