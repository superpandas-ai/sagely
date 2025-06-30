import pytest
from unittest.mock import patch, MagicMock
from sagely.config import get_config, update_config, reset_config

@pytest.fixture
def mock_tavily_search():
    with patch('sagely.langgraph_agent.TavilySearch') as mock:
        yield mock

@pytest.fixture
def setup_config():
    # Save original config
    original_config = get_config().to_dict()
    
    # Set up test config
    update_config(
        enable_web_search=True,
        tavily_api_key="test_key",
        show_status_updates=False
    )
    
    yield
    
    # Restore original config
    reset_config()
    for key, value in original_config.items():
        update_config(**{key: value})

def test_web_search_disabled():
    """Test that web search returns appropriate message when disabled."""
    update_config(enable_web_search=False)
    
    # Import the function after config change
    from sagely.langgraph_agent import web_search
    result = web_search.invoke({"query": "python unittest"})
    assert "Web search is disabled" in result
    update_config(enable_web_search=True)

def test_web_search_success(mock_tavily_search, setup_config):
    """Test successful web search with mock results."""
    # Mock search results
    mock_results = [
        {
            'title': 'Python Testing Guide',
            'url': 'https://example.com/1',
            'snippet': 'A comprehensive guide to testing in Python'
        },
        {
            'title': 'Best Practices for Unit Testing',
            'url': 'https://example.com/2',
            'snippet': 'Learn about unit testing best practices'
        }
    ]
    
    mock_instance = MagicMock()
    mock_instance.invoke.return_value = {"results": mock_results}
    mock_tavily_search.return_value = mock_instance
    
    # Import the function after mocking
    from sagely.langgraph_agent import web_search
    result = web_search.invoke({"query": "python testing"})
    
    # Verify the search was performed with correct parameters
    mock_tavily_search.assert_called_once_with(api_key="test_key", max_results=5)
    mock_instance.invoke.assert_called_once_with({"query": "python testing"})
    
    # Check that results are formatted correctly
    assert "Python Testing Guide" in result
    assert "Best Practices for Unit Testing" in result
    assert "https://example.com/1" in result
    assert "https://example.com/2" in result
    assert "References:" in result

def test_web_search_empty_results(mock_tavily_search, setup_config):
    """Test web search with empty results."""
    mock_instance = MagicMock()
    mock_instance.invoke.return_value = {"results": []}
    mock_tavily_search.return_value = mock_instance
    
    from sagely.langgraph_agent import web_search
    result = web_search.invoke({"query": "nonexistent topic"})
    assert "**References:**" in result

def test_web_search_error_handling(mock_tavily_search, setup_config):
    """Test web search error handling."""
    mock_instance = MagicMock()
    mock_instance.invoke.side_effect = Exception("API Error")
    mock_tavily_search.return_value = mock_instance
    
    from sagely.langgraph_agent import web_search
    result = web_search.invoke({"query": "python testing"})
    assert "Web search failed" in result
    assert "API Error" in result

def test_web_search_invalid_results(mock_tavily_search, setup_config):
    """Test web search with invalid results structure."""
    mock_instance = MagicMock()
    mock_instance.invoke.return_value = {"results": "invalid result"}  # Not a list
    mock_tavily_search.return_value = mock_instance
    
    from sagely.langgraph_agent import web_search
    result = web_search.invoke({"query": "python testing"})
    assert "**References:**" in result  # Should handle gracefully

def test_web_search_missing_api_key(setup_config):
    """Test web search behavior with missing API key."""
    update_config(tavily_api_key=None)
    
    from sagely.langgraph_agent import web_search
    result = web_search.invoke({"query": "python testing"})
    assert "Web search failed" in result

def test_web_search_tavily_not_available(setup_config):
    """Test web search when TavilySearchResults is not available."""
    with patch('sagely.langgraph_agent.TavilySearch', side_effect=ImportError("Tavily not available")):
        from sagely.langgraph_agent import web_search
        result = web_search.invoke({"query": "python testing"})
        assert "Web search failed" in result

def test_web_search_provider_config():
    """Test web search provider configuration."""
    # Test default provider
    config = get_config()
    assert config.web_search_provider == "openai_websearch"
    
    # Test changing provider
    update_config(web_search_provider="tavily")
    config = get_config()
    assert config.web_search_provider == "tavily"
    
    # Test invalid provider (should keep current value)
    update_config(web_search_provider="invalid_provider")
    config = get_config()
    assert config.web_search_provider == "invalid_provider"  # Should accept any string

def test_langgraph_agent_web_search_provider():
    """Test LangGraphAgent with different web search providers."""
    from sagely.langgraph_agent import LangGraphAgent
    
    # Test with OpenAI web search provider
    update_config(web_search_provider="openai_websearch")
    agent = LangGraphAgent()
    assert agent.web_search_provider == "openai_websearch"
    
    # Test with Tavily web search provider
    update_config(web_search_provider="tavily")
    agent2 = LangGraphAgent()
    assert agent2.web_search_provider == "tavily"
    
    # Test graph rebuild when provider changes
    agent.rebuild_graph_if_needed()
    assert agent.web_search_provider == "tavily"

def test_web_search_provider_environment_variable():
    """Test web search provider configuration via environment variable."""
    import os
    
    # Save original environment
    original_env = os.environ.get('SAGELY_WEB_SEARCH_PROVIDER')
    
    try:
        # Set environment variable
        os.environ['SAGELY_WEB_SEARCH_PROVIDER'] = 'tavily'
        
        # Reset config to load from environment
        reset_config()
        config = get_config()
        config.load_from_env()
        
        assert config.web_search_provider == 'tavily'
        
    finally:
        # Restore original environment
        if original_env is not None:
            os.environ['SAGELY_WEB_SEARCH_PROVIDER'] = original_env
        elif 'SAGELY_WEB_SEARCH_PROVIDER' in os.environ:
            del os.environ['SAGELY_WEB_SEARCH_PROVIDER']

def test_openai_web_search_method():
    """Test the _openai_web_search method."""
    from sagely.langgraph_agent import LangGraphAgent
    
    # Create an agent instance
    agent = LangGraphAgent()
    
    # Test the method exists
    assert hasattr(agent, '_openai_web_search')
    assert callable(agent._openai_web_search) 