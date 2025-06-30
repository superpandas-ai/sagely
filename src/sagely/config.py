"""
Configuration system for Sagely.

This module provides a centralized configuration system that allows users to
customize various aspects of Sagely's behavior and automatically reinitializes
caches when changes are made.
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from .tracing import *
from .cache import ResponseCache, ModuleInfoCache

@dataclass
class SagelyConfig:
    """Configuration class for Sagely settings."""
    
    # Model configuration
    model_name: str = "gpt-4.1-mini"
    
    # Display configuration
    show_status_updates: bool = True
    show_line_numbers: bool = True
    
    # Cache configuration
    enable_response_cache: bool = True
    enable_module_cache: bool = True
    
    # Web search configuration
    enable_web_search: bool = True
    web_search_provider: str = "openai_websearch"  # "openai_websearch" or "tavily"
    web_search_timeout: int = 10
    tavily_api_key: Optional[str] = os.environ.get("TAVILY_API_KEY")
    
    # API Keys
    openai_api_key: Optional[str] = os.environ.get("OPENAI_API_KEY")
    
    # LangSmith configuration
    enable_langsmith_tracing: bool = False
    langsmith_project: Optional[str] = None
    
    # Cache instances
    _response_cache: Optional[ResponseCache] = None
    _module_cache: Optional[ModuleInfoCache] = None
    
    @property
    def config_dir(self) -> Path:
        """Get the configuration directory path."""
        return Path.home() / ".sagely"
    
    @property
    def config_file(self) -> Path:
        """Get the configuration file path."""
        return self.config_dir / "config.json"
    
    def __post_init__(self):
        """Initialize caches after object creation."""
        self._initialize_caches()
    
    def __setattr__(self, name, value):
        """Override setattr to handle configuration updates."""
        # Check if this is an initial setup (before __post_init__)
        if not hasattr(self, '_response_cache'):
            super().__setattr__(name, value)
            return
        
        # Get the old value if it exists
        old_value = getattr(self, name, None) if hasattr(self, name) else None
        
        # Set the new value
        super().__setattr__(name, value)
        
        # Validate API keys if they're being set
        if name == 'openai_api_key':
            self._validate_api_keys()
        
        # Check if reinitialization is needed
        if name in ['enable_response_cache', 'enable_module_cache']:
            self._reinitialize()
        
        # Show status update if values actually changed (but not for internal cache attributes)
        if (self.show_status_updates and old_value != value and 
            not name.startswith('_')):
            print_status(f"Updated {name}: {old_value} → {value}", "info")
    
    def _validate_api_keys(self):
        """Validate that required API keys are present."""
        if self.openai_api_key is None:
            raise ValueError(
                "OpenAI API key is required. Please set it using:\n"
                "1. Environment variable: export OPENAI_API_KEY='your-key'\n"
                "2. Direct assignment: sagely.config.openai_api_key = 'your-key'\n"
                "3. Configuration file: ~/.sagely/config.json"
            )
    
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
    
    def save_config(self) -> bool:
        """
        Save current configuration to file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure config directory exists
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            # Get current configuration as dictionary
            config_data = self.to_dict()
            
            # Save to file
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            if self.show_status_updates:
                print_status(f"Configuration saved to {self.config_file}", "success")
            return True
            
        except Exception as e:
            if self.show_status_updates:
                print_status(f"Failed to save configuration: {e}", "error")
            return False
    
    def load_config(self) -> bool:
        """
        Load configuration from file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.config_file.exists():
                if self.show_status_updates:
                    print_status("No configuration file found", "info")
                self.save_config()  # Create config file with defaults
                return False
            
            with open(self.config_file, 'r') as f:
                config_data = json.load(f)
            
            # Update configuration with loaded data
            self.update(**config_data)
            
            if self.show_status_updates:
                print_status(f"Configuration loaded from {self.config_file}", "success")
            return True
            
        except json.JSONDecodeError as e:
            if self.show_status_updates:
                print_status(f"Invalid configuration file format: {e}", "error")
            return False
        except Exception as e:
            if self.show_status_updates:
                print_status(f"Failed to load configuration: {e}", "error")
            return False
    
    def update(self, **kwargs) -> None:
        """
        Update configuration and reinitialize caches if necessary.
        
        Args:
            **kwargs: Configuration parameters to update
        """
        needs_reinit = False
        needs_validation = False
        
        for key, value in kwargs.items():
            if hasattr(self, key):
                old_value = getattr(self, key)
                setattr(self, key, value)
                
                # Check if reinitialization is needed
                if key in ['enable_response_cache', 'enable_module_cache']:
                    needs_reinit = True
                
                # Check if validation is needed
                if key == 'openai_api_key':
                    needs_validation = True
                
                if self.show_status_updates and old_value != value:
                    print_status(f"Updated {key}: {old_value} → {value}", "info")
            else:
                if self.show_status_updates:
                    print_status(f"Unknown configuration key: {key}", "warning")
        
        if needs_reinit:
            self._reinitialize()
        
        if needs_validation:
            self._validate_api_keys()
    
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
    
    def to_dict(self) -> Dict[str, Any]:
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
            'SAGELY_SHOW_LINE_NUMBERS': 'show_line_numbers',
            'SAGELY_ENABLE_RESPONSE_CACHE': 'enable_response_cache',
            'SAGELY_ENABLE_MODULE_CACHE': 'enable_module_cache',
            'SAGELY_ENABLE_WEB_SEARCH': 'enable_web_search',
            'SAGELY_WEB_SEARCH_PROVIDER': 'web_search_provider',
            'SAGELY_WEB_SEARCH_TIMEOUT': 'web_search_timeout',
            'SAGELY_ENABLE_LANGSMITH': 'enable_langsmith_tracing',
            'SAGELY_LANGSMITH_PROJECT': 'langsmith_project',
            'TAVILY_API_KEY': 'tavily_api_key',
            'OPENAI_API_KEY': 'openai_api_key',
        }
        
        updates = {}
        for env_var, config_key in env_mapping.items():
            if env_var in os.environ:
                value = os.environ[env_var]
                
                # Convert string values to appropriate types
                if config_key == 'show_status_updates':
                    value = value.lower() in ('true', '1', 'yes', 'on')
                elif config_key == 'show_line_numbers':
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
                elif config_key == 'tavily_api_key' and value.lower() in ('none', 'null', ''):
                    value = None
                elif config_key == 'openai_api_key' and value.lower() in ('none', 'null', ''):
                    value = None
                
                updates[config_key] = value
        
        if updates:
            self.update(**updates)
            if self.show_status_updates:
                print_status(f"Loaded {len(updates)} configuration values from environment", "info")
            
            # Validate API keys after loading from environment
            self._validate_api_keys()


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
        # Try to load from file first, then environment
        _config.load_config()
        _config.load_from_env()
        # Validate API keys after loading
        _config._validate_api_keys()
    return _config


# Create a module-level config object for direct access
config = get_config()


def update_config(**kwargs) -> None:
    """
    Update global configuration.
    
    Args:
        **kwargs: Configuration parameters to update
    """
    config = get_config()
    config.update(**kwargs)


def save_config() -> bool:
    """
    Save global configuration to file.
    
    Returns:
        True if successful, False otherwise
    """
    config = get_config()
    return config.save_config()


def load_config() -> bool:
    """
    Load global configuration from file.
    
    Returns:
        True if successful, False otherwise
    """
    config = get_config()
    return config.load_config()


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