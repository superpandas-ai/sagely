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
    monkeypatch.setenv("SAGELY_MODEL", "gpt-3.5-turbo")
    monkeypatch.setenv("SAGELY_SHOW_STATUS", "false")
    monkeypatch.setenv("SAGELY_ENABLE_WEB_SEARCH", "0")
    monkeypatch.setenv("SAGELY_WEB_SEARCH_TIMEOUT", "7")
    reset_config()  # force reload
    config = get_config()
    assert config.model_name == "gpt-3.5-turbo"
    assert config.show_status_updates is False
    assert config.enable_web_search is False
    assert config.web_search_timeout == 7
    # Clean up
    reset_config() 