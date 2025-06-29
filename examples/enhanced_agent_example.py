#!/usr/bin/env python3
"""
Example demonstrating the enhanced LangGraph agent with web search functionality.
"""

from sagely.langgraph_agent import LangGraphAgent, create_agent, web_search

def main():
    # Create an enhanced LangGraph agent
    agent = create_agent("gpt-4")
    
    print("=== Enhanced LangGraph Agent with Web Search ===\n")
    
    # Example 1: Simple question that might not need web search
    print("=== Example 1: Basic Python question ===")
    agent.ask("math", "What is the difference between math.floor and math.ceil?")
    print()
    
    # Example 2: More complex question that might benefit from web search
    print("=== Example 2: Complex question about latest features ===")
    agent.ask("pandas", "What are the latest features in pandas 2.0 and how do I use them?")
    print()
    
    # Example 3: Question about best practices that might need web search
    print("=== Example 3: Best practices question ===")
    agent.ask("numpy", "What are the current best practices for memory-efficient array operations in NumPy?")
    print()
    
    # Example 4: Test web search tool directly
    print("=== Example 4: Direct web search ===")
    try:
        web_result = web_search.invoke({"query": "python pandas performance optimization 2024"})
        print("Web search result:")
        print(web_result[:500] + "..." if len(web_result) > 500 else web_result)
    except Exception as e:
        print(f"Web search failed: {e}")
    print()
    
    # Example 5: Show agent workflow information
    print("=== Example 5: Agent Workflow Information ===")
    print(f"Agent type: {type(agent)}")
    print(f"Model: {agent.llm.model_name}")
    print(f"Has cache: {hasattr(agent, 'cache')}")
    print(f"Has graph: {hasattr(agent, 'graph')}")
    
    # Show workflow nodes
    nodes = list(agent.graph.nodes.keys())
    print(f"Workflow nodes: {nodes}")
    
    # Show conditional edges
    print(f"Has conditional edges: {hasattr(agent, '_should_use_web_search')}")
    
    print("\n=== Workflow Description ===")
    print("1. analyze_context: Gathers module info, traceback, and context")
    print("2. generate_response: Creates initial answer from available info")
    print("3. orchestrator: Evaluates if answer is sufficient")
    print("4. web_search_tool: (Conditional) Searches web for additional info")
    print("5. generate_final_response: Creates comprehensive final answer")

if __name__ == "__main__":
    main() 