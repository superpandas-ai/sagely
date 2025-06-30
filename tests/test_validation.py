#!/usr/bin/env python3

import sagely

print("Testing OpenAI API key validation...")

# Test 1: Setting to None should raise ValueError
try:
    sagely.config.openai_api_key = None
    print("ERROR: Should have raised ValueError")
except ValueError as e:
    print(f"SUCCESS: Caught expected error: {e}")

# Test 2: Setting to a valid key should work
try:
    sagely.config.openai_api_key = "sk-test123"
    print("SUCCESS: Valid API key accepted")
except ValueError as e:
    print(f"ERROR: Should not have raised error: {e}")

# Test 3: Setting back to None should raise ValueError again
try:
    sagely.config.openai_api_key = None
    print("ERROR: Should have raised ValueError")
except ValueError as e:
    print(f"SUCCESS: Caught expected error: {e}")

print("Validation tests completed!") 