#!/usr/bin/env python3
"""
Example demonstrating the module info caching functionality in sagely.

This example shows how module analysis results are cached to improve performance
for subsequent queries about the same module.
"""

import time
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sagely.langgraph_agent import create_agent, analyze_module
from sagely.cache import ModuleInfoCache


def demonstrate_caching():
    """Demonstrate the module info caching functionality."""
    
    print("🧠 sagely Module Info Caching Demo")
    print("=" * 50)
    
    # Create an agent instance
    agent = create_agent()
    
    # Test module to analyze
    test_module = "json"
    
    print(f"\n1. First analysis of '{test_module}' module:")
    print("-" * 40)
    
    # Time the first analysis (should be slower)
    start_time = time.time()
    result1 = analyze_module.invoke({"module_name": test_module})
    first_analysis_time = time.time() - start_time
    
    print(f"Analysis completed in {first_analysis_time:.3f} seconds")
    print(f"Result length: {len(result1)} characters")
    print(f"First 200 chars: {result1[:200]}...")
    
    print(f"\n2. Second analysis of '{test_module}' module (should use cache):")
    print("-" * 40)
    
    # Time the second analysis (should be much faster)
    start_time = time.time()
    result2 = analyze_module.invoke({"module_name": test_module})
    second_analysis_time = time.time() - start_time
    
    print(f"Analysis completed in {second_analysis_time:.3f} seconds")
    print(f"Speed improvement: {first_analysis_time/second_analysis_time:.1f}x faster")
    print(f"Results identical: {result1 == result2}")
    
    print(f"\n3. Check if module is cached:")
    print("-" * 40)
    
    is_cached = agent.is_module_cached(test_module)
    print(f"Is '{test_module}' cached? {is_cached}")
    
    print(f"\n4. Clear cache for specific module:")
    print("-" * 40)
    
    agent.clear_module_cache(test_module)
    is_cached_after_clear = agent.is_module_cached(test_module)
    print(f"Is '{test_module}' cached after clearing? {is_cached_after_clear}")
    
    print(f"\n5. Test with another module:")
    print("-" * 40)
    
    another_module = "os"
    
    # First analysis
    start_time = time.time()
    result3 = analyze_module.invoke({"module_name": another_module})
    first_time = time.time() - start_time
    
    # Second analysis (cached)
    start_time = time.time()
    result4 = analyze_module.invoke({"module_name": another_module})
    second_time = time.time() - start_time
    
    print(f"'{another_module}' first analysis: {first_time:.3f}s")
    print(f"'{another_module}' second analysis: {second_time:.3f}s")
    print(f"Speed improvement: {first_time/second_time:.1f}x faster")
    
    print(f"\n6. Clear all module cache:")
    print("-" * 40)
    
    agent.clear_module_cache()  # Clear all
    print("All module cache cleared")
    
    # Verify cache is cleared
    is_json_cached = agent.is_module_cached(test_module)
    is_os_cached = agent.is_module_cached(another_module)
    print(f"Is '{test_module}' cached? {is_json_cached}")
    print(f"Is '{another_module}' cached? {is_os_cached}")


def demonstrate_cache_persistence():
    """Demonstrate that cache persists between sessions."""
    
    print(f"\n\n🔄 Cache Persistence Demo")
    print("=" * 50)
    
    # Create a cache instance
    cache = ModuleInfoCache()
    
    test_module = "math"
    
    print(f"1. Analyzing '{test_module}' module...")
    result = analyze_module.invoke({"module_name": test_module})
    print(f"Analysis completed, result length: {len(result)} characters")
    
    print(f"2. Creating new cache instance...")
    new_cache = ModuleInfoCache()
    
    print(f"3. Checking if '{test_module}' is cached in new instance...")
    cached_result = new_cache.get(test_module)
    
    if cached_result:
        print(f"✅ Cache persists! Result length: {len(cached_result)} characters")
        print(f"Results identical: {result == cached_result}")
    else:
        print("❌ Cache does not persist (this shouldn't happen)")


if __name__ == "__main__":
    demonstrate_caching()
    demonstrate_cache_persistence()
    
    print(f"\n\n✅ Demo completed!")
    print("The module info caching system is working correctly.")
    print("This significantly improves performance for repeated queries about the same modules.") 