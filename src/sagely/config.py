"""
Configuration system for Sagely.

This module provides a centralized configuration system that allows users to
customize various aspects of Sagely's behavior and automatically reinitializes
caches when changes are made.
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from .tracing import *
from .cache import ResponseCache, ModuleInfoCache

@dataclass
class SagelyConfig:
    """Configuration class for Sagely settings."""
    
    # Model configuration
    model_name: str = "gpt-4"
    
    # Display configuration
    show_status_updates: bool = True
    
    # Cache configuration
    enable_response_cache: bool = True
    enable_module_cache: bool = True
    
    # Web search configuration
    enable_web_search: bool = True
    web_search_timeout: int = 10
    
    # LangSmith configuration
    enable_langsmith_tracing: bool = False
    langsmith_project: Optional[str] = None
    
    # Cache instances
    _response_cache: Optional[ResponseCache] = None
    _module_cache: Optional[ModuleInfoCache] = None
    
    def __post_init__(self):
        """Initialize caches after object creation."""
        self._initialize_caches()
    
    def _initialize_caches(self):
        """Initialize cache instances."""
        if self.enable_response_cache:
            self._response_cache = ResponseCache()
        if self.enable_module_cache:
            self._module_cache = ModuleInfoCache()
    
    @property
    def response_cache(self) -> Optional[ResponseCache]:
        """Get the response cache instance."""
        return self._response_cache
    
    @property
    def module_cache(self) -> Optional[ModuleInfoCache]:
        """Get the module cache instance."""
        return self._module_cache
    
    def update(self, **kwargs) -> None:
        """
        Update configuration and reinitialize caches if necessary.
        
        Args:
            **kwargs: Configuration parameters to update
        """
        needs_reinit = False
        
        for key, value in kwargs.items():
            if hasattr(self, key):
                old_value = getattr(self, key)
                setattr(self, key, value)
                
                # Check if reinitialization is needed
                if key in ['enable_response_cache', 'enable_module_cache']:
                    needs_reinit = True
                
                if self.show_status_updates:
                    print_status(f"Updated {key}: {old_value} → {value}", "info")
            else:
                if self.show_status_updates:
                    print_status(f"Unknown configuration key: {key}", "warning")
        
        if needs_reinit:
            self._reinitialize()
    
    def _reinitialize(self):
        """Reinitialize caches with new configuration."""
        if self.show_status_updates:
            print_status("Reinitializing Sagely caches with new configuration...", "info")
        # Reinitialize caches
        self._initialize_caches()
        if self.show_status_updates:
            print_status("Sagely caches reinitialized successfully", "success")
    
    def clear_caches(self, cache_type: Optional[str] = None) -> None:
        """
        Clear caches.
        
        Args:
            cache_type: Type of cache to clear ('response', 'module', or None for all)
        """
        if cache_type is None or cache_type == "response":
            if self._response_cache:
                self._response_cache.clear()
                if self.show_status_updates:
                    print_status("Response cache cleared", "cache")
            elif self.show_status_updates:
                print_status("Response cache is disabled", "warning")
        
        if cache_type is None or cache_type == "module":
            if self._module_cache:
                self._module_cache.clear()
                if self.show_status_updates:
                    print_status("Module cache cleared", "cache")
            elif self.show_status_updates:
                print_status("Module cache is disabled", "warning")
    
    def clear_module_cache(self, module_name: Optional[str] = None) -> None:
        """
        Clear module cache for specific module or all modules.
        
        Args:
            module_name: If provided, clear cache for this specific module only.
                        If None, clear all module cache.
        """
        if self._module_cache:
            if module_name:
                self._module_cache.clear_module(module_name)
                if self.show_status_updates:
                    print_status(f"Module cache cleared for '{module_name}'", "cache")
            else:
                self._module_cache.clear()
                if self.show_status_updates:
                    print_status("All module cache cleared", "cache")
        elif self.show_status_updates:
            print_status("Module cache is disabled", "warning")
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get current configuration as a dictionary.
        
        Returns:
            Dictionary containing current configuration
        """
        config = {}
        for field in self.__dataclass_fields__:
            if not field.startswith('_'):
                config[field] = getattr(self, field)
        return config
    
    def load_from_env(self) -> None:
        """Load configuration from environment variables."""
        env_mapping = {
            'SAGELY_MODEL': 'model_name',
            'SAGELY_SHOW_STATUS': 'show_status_updates',
            'SAGELY_ENABLE_RESPONSE_CACHE': 'enable_response_cache',
            'SAGELY_ENABLE_MODULE_CACHE': 'enable_module_cache',
            'SAGELY_ENABLE_WEB_SEARCH': 'enable_web_search',
            'SAGELY_WEB_SEARCH_TIMEOUT': 'web_search_timeout',
            'SAGELY_ENABLE_LANGSMITH': 'enable_langsmith_tracing',
            'SAGELY_LANGSMITH_PROJECT': 'langsmith_project',
        }
        
        updates = {}
        for env_var, config_key in env_mapping.items():
            if env_var in os.environ:
                value = os.environ[env_var]
                
                # Convert string values to appropriate types
                if config_key == 'show_status_updates':
                    value = value.lower() in ('true', '1', 'yes', 'on')
                elif config_key == 'enable_response_cache':
                    value = value.lower() in ('true', '1', 'yes', 'on')
                elif config_key == 'enable_module_cache':
                    value = value.lower() in ('true', '1', 'yes', 'on')
                elif config_key == 'enable_web_search':
                    value = value.lower() in ('true', '1', 'yes', 'on')
                elif config_key == 'web_search_timeout':
                    value = int(value)
                elif config_key == 'enable_langsmith_tracing':
                    value = value.lower() in ('true', '1', 'yes', 'on')
                elif config_key == 'langsmith_project' and value.lower() in ('none', 'null', ''):
                    value = None
                
                updates[config_key] = value
        
        if updates:
            self.update(**updates)
            if self.show_status_updates:
                print_status(f"Loaded {len(updates)} configuration values from environment", "info")


def print_status(message: str, status_type: str = "info"):
    """Print a status message with appropriate formatting."""
    status_symbols = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "search": "🔍",
        "thinking": "🤔",
        "cache": "📦"
    }
    symbol = status_symbols.get(status_type, "ℹ️")
    print(f"{symbol} {message}")


# Global configuration instance
_config: Optional[SagelyConfig] = None


def get_config() -> SagelyConfig:
    """
    Get the global configuration instance.
    
    Returns:
        Global SagelyConfig instance
    """
    global _config
    if _config is None:
        _config = SagelyConfig()
        _config.load_from_env()
    return _config


def update_config(**kwargs) -> None:
    """
    Update global configuration.
    
    Args:
        **kwargs: Configuration parameters to update
    """
    config = get_config()
    config.update(**kwargs)


def clear_caches(cache_type: Optional[str] = None) -> None:
    """
    Clear caches using global configuration.
    
    Args:
        cache_type: Type of cache to clear ('response', 'module', or None for all)
    """
    config = get_config()
    config.clear_caches(cache_type)


def clear_module_cache(module_name: Optional[str] = None) -> None:
    """
    Clear module cache using global configuration.
    
    Args:
        module_name: If provided, clear cache for this specific module only.
                    If None, clear all module cache.
    """
    config = get_config()
    config.clear_module_cache(module_name)


def reset_config() -> None:
    """Reset global configuration to defaults."""
    global _config
    _config = None
    if get_config().show_status_updates:
        print_status("Configuration reset to defaults", "info") 