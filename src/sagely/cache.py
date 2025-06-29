import hashlib
import json
import os
from pathlib import Path


class ResponseCache:
    def __init__(self, cache_dir=None):
        if cache_dir is None:
            cache_dir = Path.home() / ".sage" / "cache"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, module_name, question):
        """Generate a cache key from module name and question."""
        content = f"{module_name}:{question}"
        return hashlib.md5(content.encode()).hexdigest()

    def _get_cache_path(self, cache_key):
        """Get the file path for a cache key."""
        return self.cache_dir / f"{cache_key}.json"

    def get(self, module_name, question):
        """Retrieve a cached response."""
        cache_key = self._get_cache_key(module_name, question)
        cache_path = self._get_cache_path(cache_key)
        
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                    return data.get('response')
            except (json.JSONDecodeError, IOError):
                return None
        return None

    def set(self, module_name, question, response):
        """Cache a response."""
        cache_key = self._get_cache_key(module_name, question)
        cache_path = self._get_cache_path(cache_key)
        
        data = {
            'module_name': module_name,
            'question': question,
            'response': response
        }
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f)
        except IOError:
            pass  # Silently fail if we can't write to cache


class ModuleInfoCache:
    def __init__(self, cache_dir=None):
        if cache_dir is None:
            cache_dir = Path.home() / ".sage" / "module_cache"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, module_name):
        """Generate a cache key from module name."""
        return hashlib.md5(module_name.encode()).hexdigest()

    def _get_cache_path(self, cache_key):
        """Get the file path for a cache key."""
        return self.cache_dir / f"{cache_key}.json"

    def get(self, module_name):
        """Retrieve cached module info."""
        cache_key = self._get_cache_key(module_name)
        cache_path = self._get_cache_path(cache_key)
        
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                    return data.get('module_info')
            except (json.JSONDecodeError, IOError):
                return None
        return None

    def set(self, module_name, module_info):
        """Cache module info."""
        cache_key = self._get_cache_key(module_name)
        cache_path = self._get_cache_path(cache_key)
        
        data = {
            'module_name': module_name,
            'module_info': module_info
        }
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f)
        except IOError:
            pass  # Silently fail if we can't write to cache

    def clear(self):
        """Clear all cached module info."""
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
        except IOError:
            pass  # Silently fail if we can't clear cache

    def clear_module(self, module_name):
        """Clear cache for a specific module."""
        cache_key = self._get_cache_key(module_name)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            if cache_path.exists():
                cache_path.unlink()
        except IOError:
            pass  # Silently fail if we can't clear cache 