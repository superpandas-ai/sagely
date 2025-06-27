from superpython.agent import SuperPythonAgent

def test_caching():
    agent = SuperPythonAgent()
    response1 = agent.ask("math", "What is sqrt?")
    response2 = agent.ask("math", "What is sqrt?")
    assert "📦 Cached Answer" in response2
    assert response1 == response2


def test_display():
    from superpython.widgets import display_with_highlight
    text = "def hello():\n    return 'hi'"
    result = display_with_highlight(text)
    assert "hello" in result 