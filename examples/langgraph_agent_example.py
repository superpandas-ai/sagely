#!/usr/bin/env python3
"""
Example demonstrating the use of the LangGraph agent in Sagely.
"""

from sagely.langgraph_agent import LangGraphAgent, create_agent

def main():
    # Create a LangGraph agent
    agent = create_agent("gpt-4")
    
    # Example 1: Ask about a standard library module
    print("=== Example 1: Asking about 'math' module ===")
    agent.ask("math", "What is the difference between math.floor and math.ceil?")
    print()
    
    # Example 2: Ask about a third-party module (if available)
    try:
        print("=== Example 2: Asking about 'numpy' module ===")
        agent.ask("numpy", "How do I create a 2D array?")
        print()
    except ImportError:
        print("numpy not available, skipping example 2")
    
    # Example 3: Create agent with different model
    print("=== Example 3: Using different model ===")
    try:
        agent_gpt35 = create_agent("gpt-3.5-turbo")
        agent_gpt35.ask("json", "How do I parse JSON in Python?")
    except Exception as e:
        print(f"Error with gpt-3.5-turbo: {e}")
    
    print("\n=== Agent Features ===")
    print(f"Agent type: {type(agent)}")
    print(f"Model: {agent.llm.model_name}")
    print(f"Has cache: {hasattr(agent, 'cache')}")
    print(f"Has graph: {hasattr(agent, 'graph')}")

if __name__ == "__main__":
    main() 