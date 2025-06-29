#!/usr/bin/env python3
"""
Example demonstrating the Sagely configuration system.

This example shows how to configure various aspects of Sagely's behavior
and how the system automatically reinitializes when changes are made.
"""

from sagely import (
    get_config, 
    update_config, 
    clear_caches, 
    clear_module_cache, 
    reset_config,
    agent,  # This is the default agent instance
    SageAgent
)

def main():
    print("🔧 Sagely Configuration System Example")
    print("=" * 50)
    
    # Get current configuration
    config = get_config()
    print(f"\n📋 Current Configuration:")
    for key, value in config.get_config().items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*50)
    print("1. Testing with default configuration")
    print("-" * 30)
    
    # Test with default settings
    agent.ask("json", "How do I parse JSON?")
    
    print("\n" + "="*50)
    print("2. Changing model and disabling status updates")
    print("-" * 30)
    
    # Update configuration
    update_config(
        model_name="gpt-3.5-turbo",
        show_status_updates=False
    )
    
    print("Configuration updated! Notice the reduced status output...")
    # Create a new agent with the new model (since config no longer instantiates agents)
    new_agent = SageAgent(model_name=get_config().model_name)
    new_agent.ask("json", "How do I serialize JSON?")
    
    print("\n" + "="*50)
    print("3. Re-enabling status updates and changing web search timeout")
    print("-" * 30)
    
    # Update configuration again
    update_config(
        show_status_updates=True,
        web_search_timeout=5
    )
    print("Configuration updated! Status updates are back...")
    new_agent = SageAgent(model_name=get_config().model_name)
    new_agent.ask("requests", "How do I make HTTP requests?")
    
    print("\n" + "="*50)
    print("4. Disabling web search")
    print("-" * 30)
    
    # Disable web search
    update_config(enable_web_search=False)
    print("Web search disabled! The agent will only use local knowledge...")
    new_agent = SageAgent(model_name=get_config().model_name)
    new_agent.ask("pandas", "What are the latest features?")
    
    print("\n" + "="*50)
    print("5. Cache management")
    print("-" * 30)
    
    # Show cache operations
    print("Clearing response cache...")
    clear_caches("response")
    
    print("Clearing module cache for 'json'...")
    clear_module_cache("json")
    
    print("Clearing all caches...")
    clear_caches()
    
    print("\n" + "="*50)
    print("6. Environment variable configuration")
    print("-" * 30)
    
    print("You can also configure Sagely using environment variables:")
    print("  export SAGELY_MODEL=gpt-4")
    print("  export SAGELY_SHOW_STATUS=false")
    print("  export SAGELY_ENABLE_WEB_SEARCH=false")
    print("  export SAGELY_WEB_SEARCH_TIMEOUT=15")
    
    print("\n" + "="*50)
    print("7. Resetting to defaults")
    print("-" * 30)
    
    # Reset configuration
    reset_config()
    
    print("Configuration reset to defaults!")
    config = get_config()
    print(f"Model: {config.model_name}")
    print(f"Status updates: {config.show_status_updates}")
    print(f"Web search: {config.enable_web_search}")
    
    print("\n✅ Configuration example completed!")
    print("The configuration system allows you to customize Sagely's behavior")
    print("and automatically reinitializes the system when changes are made.")

if __name__ == "__main__":
    main() 