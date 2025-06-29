import pytest
from sagely.prompts import (
    INITIAL_RESPONSE_PROMPT,
    ORCHESTRATOR_EVALUATION_PROMPT,
    FINAL_RESPONSE_WITH_WEB_PROMPT,
    FINAL_RESPONSE_WITHOUT_WEB_PROMPT,
    SYSTEM_MESSAGE_TEMPLATE
)


def test_initial_response_prompt():
    """Test that the initial response prompt can be formatted correctly."""
    formatted = INITIAL_RESPONSE_PROMPT.format(
        traceback="No error",
        context_summary="Test context",
        module_info="Test module info",
        question="Test question"
    )
    
    assert "No error" in formatted
    assert "Test context" in formatted
    assert "Test module info" in formatted
    assert "Test question" in formatted
    assert "Please provide a comprehensive answer" in formatted


def test_orchestrator_evaluation_prompt():
    """Test that the orchestrator evaluation prompt can be formatted correctly."""
    formatted = ORCHESTRATOR_EVALUATION_PROMPT.format(
        question="Test question",
        module_name="test_module",
        answer="Test answer"
    )
    
    assert "Test question" in formatted
    assert "test_module" in formatted
    assert "Test answer" in formatted
    assert "SUFFICIENT" in formatted
    assert "NEEDS_WEB_SEARCH" in formatted


def test_final_response_with_web_prompt():
    """Test that the final response with web prompt can be formatted correctly."""
    formatted = FINAL_RESPONSE_WITH_WEB_PROMPT.format(
        question="Test question",
        initial_answer="Test initial answer",
        web_results="Test web results",
        module_info="Test module info",
        traceback="No error",
        context_summary="Test context"
    )
    
    assert "Test question" in formatted
    assert "Test initial answer" in formatted
    assert "Test web results" in formatted
    assert "Test module info" in formatted
    assert "No error" in formatted
    assert "Test context" in formatted
    assert "comprehensive final answer" in formatted


def test_final_response_without_web_prompt():
    """Test that the final response without web prompt can be formatted correctly."""
    formatted = FINAL_RESPONSE_WITHOUT_WEB_PROMPT.format(
        question="Test question",
        initial_answer="Test initial answer"
    )
    
    assert "Test question" in formatted
    assert "Test initial answer" in formatted
    assert "format it nicely" in formatted


def test_system_message_template():
    """Test that the system message template can be formatted correctly."""
    formatted = SYSTEM_MESSAGE_TEMPLATE.format(module_name="test_module")
    
    assert "test_module" in formatted
    assert "assistant for the Python library" in formatted
    assert "helpful, accurate answers" in formatted


def test_prompt_imports():
    """Test that all prompts can be imported from the main package."""
    from sagely import (
        INITIAL_RESPONSE_PROMPT,
        ORCHESTRATOR_EVALUATION_PROMPT,
        FINAL_RESPONSE_WITH_WEB_PROMPT,
        FINAL_RESPONSE_WITHOUT_WEB_PROMPT,
        SYSTEM_MESSAGE_TEMPLATE
    )
    
    assert INITIAL_RESPONSE_PROMPT is not None
    assert ORCHESTRATOR_EVALUATION_PROMPT is not None
    assert FINAL_RESPONSE_WITH_WEB_PROMPT is not None
    assert FINAL_RESPONSE_WITHOUT_WEB_PROMPT is not None
    assert SYSTEM_MESSAGE_TEMPLATE is not None 