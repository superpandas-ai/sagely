import pytest
from sagely.sage_agent import SageAgent
from sagely.langgraph_agent import LangGraphAgent, create_agent, analyze_module, get_error_context, web_search, extended_module_summary
from unittest.mock import Mock, patch
from langchain_core.messages import AIMessage

def mock_openai_client(monkeypatch):
    # Create a mock response that LangChain expects
    mock_response = Mock()
    mock_response.content = "sqrt is a mathematical function"
    # Provide a real usage_metadata dict
    mock_response.usage_metadata = {
        'input_tokens': 10,
        'output_tokens': 5,
        'total_tokens': 15
    }
    # Mock the ChatOpenAI class
    mock_llm = Mock()
    mock_llm.invoke.return_value = mock_response
    mock_llm.model_name = "gpt-4.1-mini"
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
    with patch("sagely.widgets.display_with_highlight") as mock_display:
        agent.ask("math", "What is sqrt?")
        agent.ask("math", "What is sqrt?")
        # First call should use API, second should use cache
        # Check that display_with_highlight was called with the correct arguments
        calls = [call.args[0] for call in mock_display.call_args_list]
        assert any("sqrt is a mathematical function" in c for c in calls)
        assert any("📦 Cached Answer" in c for c in calls)

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
    with patch("sagely.widgets.display_with_highlight") as mock_display:
        agent.ask("math", "What is the square root function?")
        # Should call display_with_highlight with the mock response
        calls = [call.args[0] for call in mock_display.call_args_list]
        assert any("sqrt is a mathematical function" in c for c in calls)
        # Test with different module and question
        agent.ask("numpy", "How to create an array?")
        calls = [call.args[0] for call in mock_display.call_args_list]
        assert any("sqrt is a mathematical function" in c for c in calls)  # Same mock response 

def test_create_agent():
    """Test that we can create a LangGraph agent."""
    agent = create_agent("gpt-4.1-mini")
    assert isinstance(agent, LangGraphAgent)
    assert agent.llm.model_name == "gpt-4.1-mini"

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
    with patch('sagely.langgraph_agent.TavilySearch') as mock_tavily:
        # Mock Tavily search results
        mock_instance = Mock()
        mock_instance.invoke.return_value = {"results": [
            {
                'title': 'Python Programming Guide',
                'url': 'https://example.com/python',
                'content': 'Python is a programming language'
            }
        ]}
        mock_tavily.return_value = mock_instance
        
        # Set up config for testing
        from sagely.config import update_config
        update_config(tavily_api_key="test_key", enable_web_search=True)
        
        result = web_search.invoke({"query": "python programming"})
        assert isinstance(result, str)
        assert "Python Programming Guide" in result
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

def test_module_name_capture():
    """Test that the module name is correctly captured when using sage helper."""
    from sagely.import_hook import SageHelper, make_sage_function
    from sagely.sage_agent import SageAgent
    from unittest.mock import patch
    
    # Create a mock agent to capture the module name
    mock_agent = Mock()
    mock_agent.ask = Mock()
    
    # Test with a simple module name
    sage_helper = make_sage_function(mock_agent, "test_module")
    sage_helper.ask("test question")
    
    # Verify that the agent.ask was called with the correct module name
    mock_agent.ask.assert_called_once_with("test_module", "test question", None)
    
    # Test with a complex module name (package.submodule)
    mock_agent.reset_mock()
    sage_helper = make_sage_function(mock_agent, "sklearn.linear_model")
    sage_helper.ask("what is linear regression?")
    
    # Verify that the agent.ask was called with the correct module name
    mock_agent.ask.assert_called_once_with("sklearn.linear_model", "what is linear regression?", None)
    
    # Test with context object
    mock_agent.reset_mock()
    context_obj = {"some": "context"}
    sage_helper.ask("test question", context_obj)
    
    # Verify that the agent.ask was called with the correct module name and context
    mock_agent.ask.assert_called_once_with("sklearn.linear_model", "test question", context_obj)

def test_import_hook_module_name():
    """Test that the import hook correctly captures module names."""
    from sagely.import_hook import install_hook, make_sage_function
    from unittest.mock import Mock, patch
    import types
    
    # Create a mock agent
    mock_agent = Mock()
    mock_agent.ask = Mock()
    
    # Test the make_sage_function directly
    sage_helper = make_sage_function(mock_agent, "test_module")
    assert sage_helper.module_name == "test_module"
    
    # Test that the sage helper correctly calls the agent with the module name
    sage_helper.ask("test question")
    mock_agent.ask.assert_called_once_with("test_module", "test question", None)
    
    # Test with a complex module name
    mock_agent.reset_mock()
    sage_helper = make_sage_function(mock_agent, "sklearn.linear_model")
    sage_helper.ask("what is linear regression?")
    mock_agent.ask.assert_called_once_with("sklearn.linear_model", "what is linear regression?", None)
    
    # Test the module name capture logic
    mock_module = Mock(spec=types.ModuleType)
    mock_module.__name__ = "test_package.test_module"
    
    # Test that getattr(module, '__name__', module_name) works correctly
    module_name_actual = getattr(mock_module, '__name__', "wrong_name")
    assert module_name_actual == "test_package.test_module"
    
    # Test fallback when __name__ is not available
    mock_module_no_name = Mock(spec=types.ModuleType)
    del mock_module_no_name.__name__
    module_name_fallback = getattr(mock_module_no_name, '__name__', "fallback_name")
    assert module_name_fallback == "fallback_name"


def test_usage_tracking():
    """Test that token usage is properly tracked."""
    from sagely.usage_info import (
        get_usage_tracker, 
        add_usage, 
        get_session_total, 
        clear_usage_history,
        get_model_usage,
        get_all_model_usage,
        TokenUsage
    )
    
    # Clear usage history for clean test
    clear_usage_history()
    
    # Test initial state
    total = get_session_total()
    assert total.input_tokens == 0
    assert total.output_tokens == 0
    assert total.total_tokens == 0
    
    # Add some test usage for different models
    test_usage = {
        'input_tokens': 100,
        'output_tokens': 50,
        'total_tokens': 150
    }
    add_usage(test_usage, "gpt-4", "test_request")
    
    # Check that usage was added
    total = get_session_total()
    assert total.input_tokens == 100
    assert total.output_tokens == 50
    assert total.total_tokens == 150
    
    # Add more usage for a different model
    add_usage({
        'input_tokens': 200,
        'output_tokens': 100,
        'total_tokens': 300
    }, "gpt-4o", "another_request")
    
    # Check cumulative usage
    total = get_session_total()
    assert total.input_tokens == 300
    assert total.output_tokens == 150
    assert total.total_tokens == 450
    
    # Test model-specific usage
    gpt4_usage = get_model_usage("gpt-4")
    assert gpt4_usage.input_tokens == 100
    assert gpt4_usage.output_tokens == 50
    assert gpt4_usage.total_tokens == 150
    assert gpt4_usage.model_name == "gpt-4"
    
    gpt4o_usage = get_model_usage("gpt-4o")
    assert gpt4o_usage.input_tokens == 200
    assert gpt4o_usage.output_tokens == 100
    assert gpt4o_usage.total_tokens == 300
    assert gpt4o_usage.model_name == "gpt-4o"
    
    # Test getting all model usage
    all_models = get_all_model_usage()
    assert "gpt-4" in all_models
    assert "gpt-4o" in all_models
    assert len(all_models) == 2
    
    # Test usage tracker
    tracker = get_usage_tracker()
    recent = tracker.get_recent_usage(2)
    assert len(recent) == 2
    assert recent[0].model_name == "gpt-4"
    assert recent[0].request_type == "test_request"
    assert recent[1].model_name == "gpt-4o"
    assert recent[1].request_type == "another_request"


def test_usage_tracking_with_mock_llm(monkeypatch):
    """Test that usage tracking works with mocked LLM responses."""
    from sagely.usage_info import get_session_total, clear_usage_history
    
    # Clear usage history
    clear_usage_history()
    
    # Create a mock response with usage_metadata
    mock_response = Mock()
    mock_response.content = "Test response"
    mock_response.usage_metadata = {
        'input_tokens': 25,
        'output_tokens': 15,
        'total_tokens': 40
    }
    
    # Mock the ChatOpenAI class
    mock_llm = Mock()
    mock_llm.invoke.return_value = mock_response
    mock_llm.model_name = "gpt-4.1-mini"
    
    # Patch the ChatOpenAI import
    monkeypatch.setattr("sagely.langgraph_agent.ChatOpenAI", lambda *args, **kwargs: mock_llm)
    
    # Create agent and make a request
    agent = LangGraphAgent()
    with patch("sagely.widgets.display_with_highlight"):
        agent.ask("math", "What is 2+2?", use_cache=False)
    
    # Check that usage was tracked
    total = get_session_total()
    assert total.total_tokens > 0  # Should have tracked some usage


def test_usage_data_attribute():
    """Test that the usage_data attribute works correctly."""
    import sagely
    from sagely import clear_usage_history, add_usage
    
    # Clear usage history for clean test
    clear_usage_history()
    
    # Test initial state
    assert sagely.usage_data.input_tokens == 0
    assert sagely.usage_data.output_tokens == 0
    assert sagely.usage_data.total_tokens == 0
    assert sagely.usage_data.request_count == 0
    
    # Add some test usage
    add_usage({
        'input_tokens': 100,
        'output_tokens': 50,
        'total_tokens': 150
    }, "gpt-4", "test_request")
    
    # Test updated state
    assert sagely.usage_data.input_tokens == 100
    assert sagely.usage_data.output_tokens == 50
    assert sagely.usage_data.total_tokens == 150
    assert sagely.usage_data.request_count == 1
    
    # Test properties
    assert sagely.usage_data.total.input_tokens == 100
    assert "Session Token Usage" in sagely.usage_data.summary
    assert sagely.usage_data.tracker is not None
    
    # Test string representation
    assert "Input tokens: 100" in str(sagely.usage_data)
    
    # Test repr representation
    assert "UsageData(input_tokens=100" in repr(sagely.usage_data)
    
    # Test model-specific functionality
    assert "gpt-4" in sagely.usage_data.models
    assert sagely.usage_data.get_model_usage("gpt-4").total_tokens == 150
    assert len(sagely.usage_data.models) == 1


def test_model_specific_usage_tracking():
    """Test that usage is properly tracked per model."""
    from sagely.usage_info import (
        clear_usage_history, 
        add_usage, 
        get_model_usage, 
        get_all_model_usage,
        clear_model_history,
        get_model_recent_usage
    )
    
    # Clear usage history for clean test
    clear_usage_history()
    
    # Add usage for multiple models
    add_usage({'input_tokens': 100, 'output_tokens': 50, 'total_tokens': 150}, "gpt-4", "request1")
    add_usage({'input_tokens': 200, 'output_tokens': 100, 'total_tokens': 300}, "gpt-4o", "request2")
    add_usage({'input_tokens': 150, 'output_tokens': 75, 'total_tokens': 225}, "gpt-4", "request3")
    
    # Test model-specific usage
    gpt4_usage = get_model_usage("gpt-4")
    assert gpt4_usage.input_tokens == 250  # 100 + 150
    assert gpt4_usage.output_tokens == 125  # 50 + 75
    assert gpt4_usage.total_tokens == 375  # 150 + 225
    assert gpt4_usage.model_name == "gpt-4"
    
    gpt4o_usage = get_model_usage("gpt-4o")
    assert gpt4o_usage.input_tokens == 200
    assert gpt4o_usage.output_tokens == 100
    assert gpt4o_usage.total_tokens == 300
    assert gpt4o_usage.model_name == "gpt-4o"
    
    # Test getting all models
    all_models = get_all_model_usage()
    assert len(all_models) == 2
    assert "gpt-4" in all_models
    assert "gpt-4o" in all_models
    
    # Test model-specific recent usage
    gpt4_recent = get_model_recent_usage("gpt-4", 2)
    assert len(gpt4_recent) == 2
    assert all(usage.model_name == "gpt-4" for usage in gpt4_recent)
    
    gpt4o_recent = get_model_recent_usage("gpt-4o", 2)
    assert len(gpt4o_recent) == 1
    assert gpt4o_recent[0].model_name == "gpt-4o"
    
    # Test clearing specific model history
    clear_model_history("gpt-4")
    gpt4_usage_after_clear = get_model_usage("gpt-4")
    assert gpt4_usage_after_clear.input_tokens == 0
    assert gpt4_usage_after_clear.output_tokens == 0
    assert gpt4_usage_after_clear.total_tokens == 0
    
    # gpt-4o should still have its usage
    gpt4o_usage_after_clear = get_model_usage("gpt-4o")
    assert gpt4o_usage_after_clear.total_tokens == 300


def test_file_based_usage_tracking():
    """Test that usage data is properly saved to and loaded from files."""
    from sagely.usage_info import (
        clear_usage_history, 
        add_usage, 
        get_session_file_path,
        get_session_id,
        get_all_session_files,
        load_session_from_file,
        load_latest_session
    )
    import tempfile
    import shutil
    from pathlib import Path
    
    # Clear usage history for clean test
    clear_usage_history()
    
    # Add some test usage
    add_usage({'input_tokens': 100, 'output_tokens': 50, 'total_tokens': 150}, "gpt-4", "test_request")
    add_usage({'input_tokens': 200, 'output_tokens': 100, 'total_tokens': 300}, "gpt-4o", "another_request")
    
    # Check that file was created
    session_file = get_session_file_path()
    assert session_file.exists()
    assert session_file.name.startswith("usage_")
    assert session_file.name.endswith(".json")
    
    # Check session ID
    session_id = get_session_id()
    assert session_id is not None
    assert len(session_id) > 0
    
    # Load the session from file
    loaded_tracker = load_session_from_file(session_file)
    
    # Check that loaded data matches
    assert loaded_tracker.get_session_total().total_tokens == 450
    assert loaded_tracker.get_model_usage("gpt-4").total_tokens == 150
    assert loaded_tracker.get_model_usage("gpt-4o").total_tokens == 300
    
    # Check that we can get all session files
    session_files = get_all_session_files()
    assert len(session_files) > 0
    assert session_file in session_files
    
    # Test loading latest session
    latest_tracker = load_latest_session()
    assert latest_tracker.get_session_total().total_tokens == 450


def test_usage_data_file_properties():
    """Test that usage_data provides access to file-based properties."""
    import sagely
    from sagely import clear_usage_history, add_usage
    
    # Clear usage history for clean test
    clear_usage_history()
    
    # Add some test usage
    add_usage({'input_tokens': 100, 'output_tokens': 50, 'total_tokens': 150}, "gpt-4", "test_request")
    
    # Test file properties
    assert sagely.usage_data.session_id is not None
    assert len(sagely.usage_data.session_id) > 0
    
    session_file = sagely.usage_data.session_file_path
    assert session_file.exists()
    assert session_file.name.startswith("usage_")
    assert session_file.name.endswith(".json")
    
    # Test that repr includes session_id
    repr_str = repr(sagely.usage_data)
    assert "session_id=" in repr_str 