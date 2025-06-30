import os
import pytest
from sagely.config import (
    get_config, update_config, clear_caches, clear_module_cache, reset_config, SagelyConfig
)

def test_default_config_values():
    config = get_config()
    assert config.model_name == "gpt-4"
    assert config.show_status_updates is True
    assert config.enable_response_cache is True
    assert config.enable_module_cache is True
    assert config.enable_web_search is True
    assert config.web_search_timeout == 10
    assert config.enable_langsmith_tracing is False
    assert config.langsmith_project is None

def test_update_config_and_reinit():
    config = get_config()
    update_config(model_name="gpt-3.5-turbo", show_status_updates=False)
    assert config.model_name == "gpt-3.5-turbo"
    assert config.show_status_updates is False
    update_config(model_name="gpt-4", show_status_updates=True)  # reset


def test_cache_clearing():
    config = get_config()
    # Fill caches
    if config.response_cache:
        config.response_cache.set("mod", "q", "a")
        assert config.response_cache.get("mod", "q") == "a"
    if config.module_cache:
        config.module_cache.set("mod", "info")
        assert config.module_cache.get("mod") == "info"
    # Clear caches
    clear_caches("response")
    if config.response_cache:
        assert config.response_cache.get("mod", "q") is None
    clear_caches("module")
    if config.module_cache:
        assert config.module_cache.get("mod") is None
    # Fill again and clear all
    if config.response_cache:
        config.response_cache.set("mod", "q", "a")
    if config.module_cache:
        config.module_cache.set("mod", "info")
    clear_caches()
    if config.response_cache:
        assert config.response_cache.get("mod", "q") is None
    if config.module_cache:
        assert config.module_cache.get("mod") is None

def test_clear_module_cache_specific():
    config = get_config()
    if config.module_cache:
        config.module_cache.set("mod1", "info1")
        config.module_cache.set("mod2", "info2")
        clear_module_cache("mod1")
        assert config.module_cache.get("mod1") is None
        assert config.module_cache.get("mod2") == "info2"
        clear_module_cache()
        assert config.module_cache.get("mod2") is None

def test_env_loading(monkeypatch):
    """Test loading configuration from environment variables."""
    # Set environment variables
    monkeypatch.setenv("SAGELY_MODEL", "gpt-3.5-turbo")
    monkeypatch.setenv("SAGELY_SHOW_STATUS", "false")
    monkeypatch.setenv("SAGELY_ENABLE_WEB_SEARCH", "false")
    monkeypatch.setenv("SAGELY_WEB_SEARCH_TIMEOUT", "15")
    monkeypatch.setenv("SAGELY_SHOW_LINE_NUMBERS", "false")
    
    # Reset config to load from environment
    from sagely.config import reset_config
    reset_config()
    
    # Get config and check values
    config = get_config()
    assert config.model_name == "gpt-3.5-turbo"
    assert config.show_status_updates is False
    assert config.enable_web_search is False
    assert config.web_search_timeout == 15
    assert config.show_line_numbers is False
    # Clean up
    reset_config()

def test_display_with_highlight_line_numbers():
    """Test display_with_highlight function respects line numbers configuration."""
    from sagely.widgets import display_with_highlight
    
    # Test with default configuration (should show line numbers)
    config = get_config()
    original_setting = config.show_line_numbers
    
    try:
        # Test with line numbers enabled
        config.show_line_numbers = True
        result = display_with_highlight("test code", show_line_numbers=None)
        assert result == "test code"
        
        # Test with line numbers disabled
        config.show_line_numbers = False
        result = display_with_highlight("test code", show_line_numbers=None)
        assert result == "test code"
        
        # Test explicit override
        result = display_with_highlight("test code", show_line_numbers=True)
        assert result == "test code"
        
    finally:
        # Restore original setting
        config.show_line_numbers = original_setting

def test_direct_config_updates():
    """Test direct configuration updates via attribute assignment."""
    from sagely import config
    
    # Save original values
    original_module_cache = config.enable_module_cache
    original_line_numbers = config.show_line_numbers
    original_model = config.model_name
    
    try:
        # Test direct updates
        config.enable_module_cache = False
        assert config.enable_module_cache is False
        
        config.show_line_numbers = False
        assert config.show_line_numbers is False
        
        config.model_name = "gpt-3.5-turbo"
        assert config.model_name == "gpt-3.5-turbo"
        
        # Test that cache reinitialization happens
        config.enable_response_cache = False
        assert config.enable_response_cache is False
        
    finally:
        # Restore original values
        config.enable_module_cache = original_module_cache
        config.show_line_numbers = original_line_numbers
        config.model_name = original_model
        config.enable_response_cache = True 