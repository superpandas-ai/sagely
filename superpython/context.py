import sys
import traceback
import inspect
from typing import Any, Optional


def get_recent_traceback() -> str:
    """Get the most recent traceback as a string."""
    try:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_traceback is not None:
            return ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    except:
        pass
    return "No recent errors"


def summarize_object(obj: Any) -> str:
    """Create a summary of an object for context."""
    if obj is None:
        return "None"
    
    try:
        obj_type = type(obj).__name__
        
        # Handle different types of objects
        if hasattr(obj, '__dict__'):
            # Class instance
            attrs = list(obj.__dict__.keys())[:10]  # Limit to first 10 attributes
            return f"{obj_type} with attributes: {attrs}"
        elif hasattr(obj, '__len__'):
            # Container-like object
            try:
                length = len(obj)
                if length > 0:
                    first_item = str(obj[0])[:100]  # First 100 chars of first item
                    return f"{obj_type} with {length} items, first: {first_item}"
                else:
                    return f"{obj_type} (empty)"
            except (IndexError, TypeError):
                return f"{obj_type} (length: {length})"
        else:
            # Simple object
            return f"{obj_type}: {str(obj)[:200]}"  # First 200 chars
            
    except Exception as e:
        return f"Error summarizing object: {str(e)}"


def get_module_info(module_name: str) -> str:
    """Get information about a module."""
    try:
        module = sys.modules.get(module_name)
        if module is None:
            return f"Module '{module_name}' not found"
        
        doc = inspect.getdoc(module) or "No documentation available"
        members = inspect.getmembers(module)
        functions = [name for name, obj in members if inspect.isfunction(obj)]
        classes = [name for name, obj in members if inspect.isclass(obj)]
        
        info = f"Documentation: {doc[:500]}...\n"
        info += f"Functions: {functions[:10]}\n"
        info += f"Classes: {classes[:10]}"
        
        return info
    except Exception as e:
        return f"Error getting module info: {str(e)}" 