import pytest
from sage.agent import SageAgent

def mock_openai_client(monkeypatch):
    class MockChoices:
        def __init__(self, content):
            self.message = type('msg', (), {'content': content})
    class MockCompletions:
        def __init__(self):
            self.create_call_count = 0
        def create(self, **kwargs):
            self.create_call_count += 1
            return type('resp', (), {'choices': [MockChoices("sqrt is a mathematical function")]})()
    class MockChat:
        def __init__(self):
            self.completions = MockCompletions()
    class MockClient:
        def __init__(self):
            self.chat = MockChat()
    monkeypatch.setattr("openai.OpenAI", lambda *args, **kwargs: MockClient())
    return MockClient

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
    from sage.widgets import display_with_highlight
    text = "def hello():\n    return 'hi'"
    result = display_with_highlight(text)
    assert "hello" in result

def test_agent_creation():
    agent = SageAgent()
    assert agent is not None
    assert hasattr(agent, 'ask')
    assert hasattr(agent, 'cache')

def test_cache_functionality():
    from sage.cache import ResponseCache
    cache = ResponseCache()
    # Test setting and getting
    cache.set("test_module", "test question", "test answer")
    result = cache.get("test_module", "test question")
    assert result == "test answer"
    # Test non-existent cache entry
    result = cache.get("test_module", "non-existent question")
    assert result is None 