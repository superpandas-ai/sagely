#!/usr/bin/env python3
"""
Simple test script to verify the SuperPython package structure works.
"""

import sys
import os

# Add the current directory to the path so we can import our package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from superpython import agent
        print("✓ Successfully imported superpython.agent")
        
        from superpython.cache import ResponseCache
        print("✓ Successfully imported superpython.cache")
        
        from superpython.context import get_recent_traceback, summarize_object
        print("✓ Successfully imported superpython.context")
        
        from superpython.widgets import display_with_highlight
        print("✓ Successfully imported superpython.widgets")
        
        from superpython.import_hook import install_hook
        print("✓ Successfully imported superpython.import_hook")
        
        from superpython.ipython_magics import load_ipython_extension
        print("✓ Successfully imported superpython.ipython_magics")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_agent_creation():
    """Test that the agent can be created."""
    try:
        from superpython.agent import SuperPythonAgent
        agent = SuperPythonAgent()
        print("✓ Successfully created SuperPythonAgent instance")
        return True
    except Exception as e:
        print(f"✗ Error creating agent: {e}")
        return False

def test_cache():
    """Test the cache functionality."""
    try:
        from superpython.cache import ResponseCache
        cache = ResponseCache()
        
        # Test setting and getting
        cache.set("test_module", "test question", "test answer")
        result = cache.get("test_module", "test question")
        
        if result == "test answer":
            print("✓ Cache functionality works")
            return True
        else:
            print("✗ Cache functionality failed")
            return False
    except Exception as e:
        print(f"✗ Cache test error: {e}")
        return False

if __name__ == "__main__":
    print("Testing SuperPython package structure...")
    print()
    
    tests = [
        test_imports,
        test_agent_creation,
        test_cache,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Package structure is working correctly.")
    else:
        print("❌ Some tests failed. Please check the errors above.") 