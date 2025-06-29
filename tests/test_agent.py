import pytest
from sagely.sage_agent import SageAgent
from sagely.langgraph_agent import LangGraphAgent, create_agent, analyze_module, get_error_context, web_search, extended_module_summary
from unittest.mock import Mock, patch
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

def test_extended_module_summary():
    """Test the extended_module_summary function."""
    import sys
    summary = extended_module_summary(sys)
    
    # Check that summary has the expected structure
    assert "functions" in summary
    assert "classes" in summary
    assert "submodules" in summary
    
    # Check that all values are lists
    assert isinstance(summary["functions"], list)
    assert isinstance(summary["classes"], list)
    assert isinstance(summary["submodules"], list)
    
    # Check that functions and classes have tuples with name and docstring
    if summary["functions"]:
        assert isinstance(summary["functions"][0], tuple)
        assert len(summary["functions"][0]) == 2
        assert isinstance(summary["functions"][0][0], str)  # name
        assert isinstance(summary["functions"][0][1], (str, type(None)))  # docstring or None
    
    if summary["classes"]:
        assert isinstance(summary["classes"][0], tuple)
        assert len(summary["classes"][0]) == 2
        assert isinstance(summary["classes"][0][0], str)  # name
        assert isinstance(summary["classes"][0][1], (str, type(None)))  # docstring or None

def test_get_error_context_tool():
    """Test the get_error_context tool."""
    result = get_error_context.invoke({})
    assert isinstance(result, str)

def test_web_search_tool():
    """Test the web_search tool."""
    with patch('requests.get') as mock_get:
        # Mock a successful response
        mock_response = Mock()
        mock_response.json.return_value = {
            "Abstract": "Python is a programming language",
            "Answer": "Python is great for data science",
            "RelatedTopics": [{"Text": "Python programming"}]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = web_search.invoke({"query": "python programming"})
        assert isinstance(result, str)
        assert "Python is a programming language" in result

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

def test_enhanced_workflow_nodes():
    """Test that the enhanced workflow has all the expected nodes."""
    agent = LangGraphAgent()
    # Check that the graph has the expected nodes
    nodes = agent.graph.nodes
    expected_nodes = ["analyze_context", "generate_response", "orchestrator", 
                     "web_search_tool", "generate_final_response"]
    for node in expected_nodes:
        assert node in nodes

def test_conditional_edges():
    """Test that the conditional edges are properly set up."""
    agent = LangGraphAgent()
    # The orchestrator should have conditional edges
    assert hasattr(agent, '_should_use_web_search') 