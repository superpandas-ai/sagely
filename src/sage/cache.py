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