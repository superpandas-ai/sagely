import pytest
from sagely.sage_agent import SageAgent
from sagely.langgraph_agent import LangGraphAgent, create_agent, analyze_module, get_error_context
from unittest.mock import Mock
from langchain_core.messages import AIMessage

def mock_openai_client(monkeypatch):
    # Create a mock response that LangChain expects
    mock_response = Mock()
    mock_response.content = "sqrt is a mathematical function"
    
    # Mock the ChatOpenAI class
    mock_llm = Mock()
    mock_llm.invoke.return_value = mock_response
    mock_llm.model_name = "gpt-4"
    
    # Patch the ChatOpenAI import in the agent module
    monkeypatch.setattr("sagely.langgraph_agent.ChatOpenAI", lambda *args, **kwargs: mock_llm)
    
    return mock_llm

def test_caching(monkeypatch):
    mock_client = mock_openai_client(monkeypatch)()
    # Clear the cache to ensure we start fresh
    import shutil
    import os
    cache_dir = os.path.expanduser("~/.sage/cache")
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
    agent = SageAgent()
    response1 = agent.ask("math", "What is sqrt?")
    response2 = agent.ask("math", "What is sqrt?")
    print(f"response1: {response1}")
    print(f"response2: {response2}")
    # First call should use API, second should use cache
    assert "sqrt is a mathematical function" in response1
    assert "📦 Cached Answer" in response2

def test_display():
    from sagely.widgets import display_with_highlight
    text = "def hello():\n    return 'hi'"
    result = display_with_highlight(text)
    assert "hello" in result

def test_agent_creation():
    agent = SageAgent()
    assert agent is not None
    assert hasattr(agent, 'ask')
    assert hasattr(agent, 'cache')

def test_cache_functionality():
    from sagely.cache import ResponseCache
    cache = ResponseCache()
    # Test setting and getting
    cache.set("test_module", "test question", "test answer")
    result = cache.get("test_module", "test question")
    assert result == "test answer"
    # Test non-existent cache entry
    result = cache.get("test_module", "non-existent question")
    assert result is None

def test_ask_function_call(monkeypatch):
    """Test that the ask function call works correctly with mocked OpenAI client."""
    mock_openai_client(monkeypatch)()
    
    # Clear the cache to ensure we start fresh
    import shutil
    import os
    cache_dir = os.path.expanduser("~/.sage/cache")
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
    
    # Create agent and test ask function
    agent = SageAgent()
    
    # Test the ask method with a simple question
    response = agent.ask("math", "What is the square root function?")
    
    # Verify the response contains the expected content from mock
    assert "sqrt is a mathematical function" in response
    
    # Test with different module and question
    response2 = agent.ask("numpy", "How to create an array?")
    assert "sqrt is a mathematical function" in response2  # Same mock response 

def test_create_agent():
    """Test that we can create a LangGraph agent."""
    agent = create_agent("gpt-4")
    assert isinstance(agent, LangGraphAgent)
    assert agent.llm.model_name == "gpt-4"

def test_analyze_module_tool():
    """Test the analyze_module tool."""
    result = analyze_module.invoke({"module_name": "sys"})
    assert isinstance(result, str)
    assert "Functions:" in result

def test_get_error_context_tool():
    """Test the get_error_context tool."""
    result = get_error_context.invoke({})
    assert isinstance(result, str)

def test_langgraph_agent_initialization():
    """Test LangGraph agent initialization."""
    agent = LangGraphAgent()
    assert hasattr(agent, 'llm')
    assert hasattr(agent, 'cache')
    assert hasattr(agent, 'graph')

def test_agent_state_structure():
    """Test that the agent has the expected state structure."""
    agent = LangGraphAgent()
    # The graph should be compiled and ready to use
    assert hasattr(agent.graph, 'invoke') 