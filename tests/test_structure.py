#!/usr/bin/env python3
"""
Simple test script to verify the Sage package structure works.
"""

import sys
import os

# Add the current directory to the path so we can import our package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    from sage import agent
    from sage.cache import ResponseCache
    from sage.context import get_recent_traceback, summarize_object
    from sage.widgets import display_with_highlight
    from sage.import_hook import install_hook
    from sage.ipython_magics import load_ipython_extension
    # If any import fails, the test will error

def test_agent_creation():
    """Test that the agent can be created."""
    from sage.agent import SageAgent
    agent = SageAgent()
    assert agent is not None
    assert hasattr(agent, 'ask')

def test_cache():
    """Test the cache functionality."""
    from sage.cache import ResponseCache
    cache = ResponseCache()
    cache.set("test_module", "test question", "test answer")
    result = cache.get("test_module", "test question")
    assert result == "test answer"

if __name__ == "__main__":
    print("Testing Sage package structure...")
    print()
    try:
        test_imports()
        print("✓ All imports successful")
    except Exception as e:
        print(f"✗ Import error: {e}")
    try:
        test_agent_creation()
        print("✓ Agent creation successful")
    except Exception as e:
        print(f"✗ Agent creation error: {e}")
    try:
        test_cache()
        print("✓ Cache functionality successful")
    except Exception as e:
        print(f"✗ Cache test error: {e}")
    print("\n🎉 All tests completed!") 