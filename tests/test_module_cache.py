import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add the src directory to the path so we can import sagely
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sagely.cache import ModuleInfoCache
from sagely.langgraph_agent import analyze_module


class TestModuleCache(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment with temporary cache directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache = ModuleInfoCache(cache_dir=self.temp_dir)
        
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_cache_set_and_get(self):
        """Test that module info can be set and retrieved from cache."""
        module_name = "test_module"
        module_info = "Test module information"
        
        # Initially, cache should be empty
        self.assertIsNone(self.cache.get(module_name))
        
        # Set cache
        self.cache.set(module_name, module_info)
        
        # Retrieve from cache
        cached_info = self.cache.get(module_name)
        self.assertEqual(cached_info, module_info)
    
    def test_cache_clear(self):
        """Test that cache can be cleared."""
        module_name = "test_module"
        module_info = "Test module information"
        
        # Set cache
        self.cache.set(module_name, module_info)
        self.assertIsNotNone(self.cache.get(module_name))
        
        # Clear cache
        self.cache.clear()
        self.assertIsNone(self.cache.get(module_name))
    
    def test_cache_clear_specific_module(self):
        """Test that cache for a specific module can be cleared."""
        module1 = "test_module_1"
        module2 = "test_module_2"
        info1 = "Info for module 1"
        info2 = "Info for module 2"
        
        # Set cache for both modules
        self.cache.set(module1, info1)
        self.cache.set(module2, info2)
        
        # Clear only module1
        self.cache.clear_module(module1)
        
        # Check that module1 is cleared but module2 remains
        self.assertIsNone(self.cache.get(module1))
        self.assertEqual(self.cache.get(module2), info2)
    
    def test_analyze_module_caching(self):
        """Test that analyze_module function uses caching."""
        # This test requires a real module to analyze
        # We'll use 'os' module which should be available
        module_name = "os"
        
        # First call should analyze and cache
        result1 = analyze_module.invoke({"module_name": module_name})
        self.assertIsNotNone(result1)
        self.assertIn("Module: os", result1)
        
        # Second call should return cached result
        result2 = analyze_module.invoke({"module_name": module_name})
        self.assertEqual(result1, result2)


if __name__ == '__main__':
    unittest.main() 