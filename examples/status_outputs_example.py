#!/usr/bin/env python3
"""
Example demonstrating status outputs in the LangGraph agent.

This example shows how the agent provides real-time feedback about
what it's doing during the workflow execution.
"""

from sagely import LangGraphAgent

def main():
    print("🚀 LangGraph Agent Status Outputs Example")
    print("=" * 50)
    
    # Create an agent instance
    agent = LangGraphAgent(model_name="gpt-4")
    
    print("\n📝 Example 1: Basic question with status tracking")
    print("-" * 40)
    
    # Ask a question - you'll see status messages throughout the process
    agent.ask(
        module_name="json",
        question="How do I parse JSON data in Python?"
    )
    
    print("\n📝 Example 2: Question that might trigger web search")
    print("-" * 40)
    
    # Ask a question that might need web search for latest information
    agent.ask(
        module_name="requests",
        question="What are the latest best practices for handling timeouts in requests?"
    )
    
    print("\n📝 Example 3: Cached response (should be fast)")
    print("-" * 40)
    
    # Ask the same question again - should use cache
    agent.ask(
        module_name="json",
        question="How do I parse JSON data in Python?"
    )
    
    print("\n📝 Example 4: Module cache operations")
    print("-" * 40)
    
    # Check if a module is cached
    is_cached = agent.is_module_cached("json")
    print(f"Module 'json' is cached: {is_cached}")
    
    # Clear module cache for a specific module
    agent.clear_module_cache("json")
    
    # Check again
    is_cached = agent.is_module_cached("json")
    print(f"Module 'json' is cached after clearing: {is_cached}")
    
    print("\n✅ Example completed! Notice how the status messages")
    print("   provided visibility into each step of the workflow.")

if __name__ == "__main__":
    main() 