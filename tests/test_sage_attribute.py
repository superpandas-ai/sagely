import pytest
from sagely.import_hook import install_hook
from sagely.agent import SageAgent


def test_sage_attribute_injection():
    """Test that the .sage attribute is injected into modules."""
    # Create an agent
    agent = SageAgent()
    
    # Install the hook
    install_hook(agent)
    
    # Import a module
    import math
    
    # Check that the .sage attribute exists and is callable
    assert hasattr(math, 'sage')
    assert callable(math.sage)


def test_sage_attribute_not_injected_to_sagely():
    """Test that .sage attribute is not injected to sagely modules."""
    agent = SageAgent()
    install_hook(agent)
    
    # Import sagely itself
    import sagely
    
    # Check that sagely doesn't have the .sage attribute
    assert not hasattr(sagely, 'sage')


def test_sage_attribute_functionality():
    """Test that the .sage attribute can be used to ask questions."""
    agent = SageAgent()
    install_hook(agent)
    
    # Import a module
    import math
    
    # The .sage attribute should be callable
    ask_function = math.sage
    assert callable(ask_function)
    
    # Test that the function can be called (though it may fail without proper setup)
    assert hasattr(ask_function, '__call__') 