#!/usr/bin/env python3
"""
Example demonstrating how to use the separated prompts directly.
"""

from sagely.prompts import (
    INITIAL_RESPONSE_PROMPT,
    ORCHESTRATOR_EVALUATION_PROMPT,
    FINAL_RESPONSE_WITH_WEB_PROMPT,
    FINAL_RESPONSE_WITHOUT_WEB_PROMPT,
    SYSTEM_MESSAGE_TEMPLATE
)

def main():
    print("=== Using Separated Prompts ===\n")
    
    # Example 1: System message template
    print("=== Example 1: System Message Template ===")
    system_msg = SYSTEM_MESSAGE_TEMPLATE.format(module_name="numpy")
    print(system_msg)
    print()
    
    # Example 2: Initial response prompt
    print("=== Example 2: Initial Response Prompt ===")
    initial_prompt = INITIAL_RESPONSE_PROMPT.format(
        traceback="No recent errors",
        context_summary="Working with array data",
        module_info="NumPy module with array operations",
        question="How do I create a 2D array?"
    )
    print(initial_prompt)
    print()
    
    # Example 3: Orchestrator evaluation prompt
    print("=== Example 3: Orchestrator Evaluation Prompt ===")
    evaluation_prompt = ORCHESTRATOR_EVALUATION_PROMPT.format(
        question="How do I create a 2D array?",
        module_name="numpy",
        answer="You can use np.array([[1, 2], [3, 4]]) to create a 2D array."
    )
    print(evaluation_prompt)
    print()
    
    # Example 4: Final response with web search
    print("=== Example 4: Final Response with Web Search ===")
    final_with_web = FINAL_RESPONSE_WITH_WEB_PROMPT.format(
        question="What are the latest NumPy features?",
        initial_answer="NumPy has many features for array operations.",
        web_results="Recent NumPy releases include improved performance and new functions.",
        module_info="NumPy module information",
        traceback="No errors",
        context_summary="Working with scientific computing"
    )
    print(final_with_web)
    print()
    
    # Example 5: Final response without web search
    print("=== Example 5: Final Response without Web Search ===")
    final_without_web = FINAL_RESPONSE_WITHOUT_WEB_PROMPT.format(
        question="What is np.array?",
        initial_answer="np.array is a function that creates NumPy arrays from various input types."
    )
    print(final_without_web)
    print()
    
    # Example 6: Custom prompt modification
    print("=== Example 6: Custom Prompt Modification ===")
    # You can modify prompts for specific use cases
    custom_system_msg = SYSTEM_MESSAGE_TEMPLATE.format(module_name="pandas") + "\nFocus on data analysis and manipulation."
    print("Custom system message:")
    print(custom_system_msg)
    print()
    
    # Example 7: Prompt inspection
    print("=== Example 7: Prompt Inspection ===")
    print(f"Initial response prompt length: {len(INITIAL_RESPONSE_PROMPT)} characters")
    print(f"Orchestrator prompt length: {len(ORCHESTRATOR_EVALUATION_PROMPT)} characters")
    print(f"Final response with web prompt length: {len(FINAL_RESPONSE_WITH_WEB_PROMPT)} characters")
    print(f"Final response without web prompt length: {len(FINAL_RESPONSE_WITHOUT_WEB_PROMPT)} characters")
    print(f"System message template length: {len(SYSTEM_MESSAGE_TEMPLATE)} characters")

if __name__ == "__main__":
    main() 