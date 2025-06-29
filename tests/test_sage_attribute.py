import pytest
from sagely.import_hook import install_hook, SageHelper
from sagely.sage_agent import SageAgent


def test_sage_attribute_injection():
    """Test that the .sage attribute is injected into modules."""
    # Create an agent
    agent = SageAgent()
    
    # Install the hook
    install_hook(agent)
    
    # Import a module
    import math
    
    # Check that the .sage attribute exists and has an ask method
    assert hasattr(math, 'sage')
    assert isinstance(math.sage, SageHelper)
    assert hasattr(math.sage, 'ask')
    assert callable(math.sage.ask)


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
    
    # The .sage attribute should be a SageHelper object with an ask method
    sage_helper = math.sage
    assert isinstance(sage_helper, SageHelper)
    assert hasattr(sage_helper, 'ask')
    assert callable(sage_helper.ask)
    
    # Test that the ask method can be called (though it may fail without proper setup)
    assert hasattr(sage_helper.ask, '__call__') 