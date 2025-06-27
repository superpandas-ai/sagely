import openai
import inspect
import sys
from .cache import ResponseCache
from .context import get_recent_traceback, summarize_object
from .widgets import display_with_highlight

class SuperPythonAgent:
    def __init__(self):
        self.cache = ResponseCache()

    def ask(self, module_name, question, context_obj=None):
        cached = self.cache.get(module_name, question)
        if cached:
            return display_with_highlight(f"📦 Cached Answer:\n{cached}")

        traceback = get_recent_traceback()
        context_summary = summarize_object(context_obj) if context_obj else "None"

        try:
            __import__(module_name)
            mod = sys.modules[module_name]
            doc = inspect.getdoc(mod)
            members = inspect.getmembers(mod)
            functions = [name for name, obj in members if inspect.isfunction(obj)]
            context_info = f"\n\nDocumentation:\n{doc}\n\nFunctions:\n{functions[:20]}"
        except:
            context_info = ""

        prompt = f"""
You are an assistant for the Python library '{module_name}'.

Recent Error (if any):
{traceback}

Context Object:
{context_summary}

Package Info:
{context_info}

User Question:
{question}
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful Python expert."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response['choices'][0]['message']['content']
        self.cache.set(module_name, question, answer)
        return display_with_highlight(answer) 