"""
Prompts used by the LangGraph agent for various tasks.
"""

# Prompt for generating initial response
INITIAL_RESPONSE_PROMPT = """
Recent Error (if any):
{traceback}

Context Object:
{context_summary}

Package Info:
{module_info}

User Question:
{question}

Please provide a comprehensive answer based on the available information.
"""

# Prompt for orchestrator to evaluate if answer is sufficient
ORCHESTRATOR_EVALUATION_PROMPT = """
You are evaluating whether an answer to a question about a Python library is sufficient.

Question: {question}
Module: {module_name}
Current Answer: {answer}

Evaluate if this answer is comprehensive and accurate enough to fully address the user's question.
Consider:
1. Does it directly answer the question?
2. Does it provide enough detail and examples?
3. Does it cover edge cases or common issues?
4. Is it up-to-date with current best practices?

Respond with either "SUFFICIENT" or "NEEDS_WEB_SEARCH" followed by a brief explanation.
"""

# Prompt for generating final response with web search results
FINAL_RESPONSE_WITH_WEB_PROMPT = """
You have an initial answer and additional web search results. Create a comprehensive final answer.

User Question: {question}

Initial Answer:
{initial_answer}

Additional Web Information:
{web_results}

Package Info:
{module_info}

Recent Error (if any):
{traceback}

Context Object:
{context_summary}

Please create a comprehensive final answer that:
1. Incorporates the best information from both sources
2. Provides clear, actionable guidance
3. Includes relevant examples and best practices
4. Addresses the user's question completely
"""

# Prompt for generating final response without web search
FINAL_RESPONSE_WITHOUT_WEB_PROMPT = """
The initial answer is sufficient. Please format it nicely for the user.

User Question: {question}

Answer:
{initial_answer}
"""

# System message template for context analysis
SYSTEM_MESSAGE_TEMPLATE = "You are an assistant for the Python library '{module_name}'. Provide helpful, accurate answers about the library." 