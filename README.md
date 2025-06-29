<p align="center">
  <img src="https://raw.githubusercontent.com/superpandas-ai/sagely/main/assets/banner.png" alt="sagely Agent Banner" width="100%" />
</p>

<p align="center">
  <b>LLM-powered assistant for every Python package you import.</b><br/>
  Just add <code>.sage.ask("your question")</code> to any module.
</p>

<p align="center">
  <a href="https://pypi.org/project/sagely/">
    <img src="https://img.shields.io/pypi/v/sagely.svg?color=blue" alt="PyPI version">
  </a>
  <a href="https://github.com/superpandas-ai/sagely/actions">
    <img src="https://github.com/superpandas-ai/sagely/workflows/Tests/badge.svg" alt="CI Status">
  </a>
  <a href="https://github.com/superpandas-ai/sagely">
    <img src="https://img.shields.io/github/stars/superpandas-ai/sagely?style=social" alt="GitHub stars">
  </a>
</p>

---

# 🧠 sagely Agent

sagely Agent automatically injects a `.sage` assistant into every package you import. Ask questions about the library you're using, get help with errors, and explore code with syntax-highlighted answers — all powered by an LLM.

---

## 🎥 Demo

> _(Click to view full video)_

https://github.com/superpandas-ai/sagely/assets/demo.gif  
_or_  
https://loom.com/share/sagely-demo-link

---

## ❓ Why sagely?

There are thousands of Python libraries, but their docs aren't always intuitive. sagely fills that gap:

- You don't need to search Stack Overflow every time you forget a method.
- You get context-aware help, including recent exceptions and object summaries.
- It's built for exploration — whether you're using a notebook, REPL, or script.

---

## ✨ Features

- �� Ask any module `.sage.ask("How do I do X?")`
- 💡 Smart context: recent errors + object summaries
- 🧩 Auto-attaches to every import
- 💾 Caches answers to avoid repeated API calls
- 🎨 Syntax-highlighted output with `pygments`
- 🧠 IPython magic: `%sagely pandas how to merge?`

---

## 🚀 Getting Started

### 1. Install

```bash
pip install sagely
```

### 2. Import It
```python
import sagely
```
It hooks into all future imports.

## 🧪 Usage Examples
### Inline Python
```python
import matplotlib

matplotlib.sage.ask("how to make a scatter plot?")
```

### In Jupyter / IPython
```python
%load_ext sagely

%sagely numpy how to generate random numbers?
```

### Programmatic
```python
from sagely import agent

agent.ask("requests", "how do I send a POST request?")
```

## 🔧 Requirements
- openai
- ipywidgets
- pygments
- ipython

(Installed automatically.)

## 🧠 Project Structure
```text
sagely/
├── src/sagely/
│   ├── agent.py
│   ├── cache.py
│   ├── context.py
│   ├── import_hook.py
│   ├── ipython_magics.py
│   ├── widgets.py
│   └── __init__.py
├── tests/
├── pyproject.toml
├── MANIFEST.in
└── README.md
```

## 🤝 Contributing
sagely is early-stage — PRs and ideas welcome!

- Want to support other LLMs?
- Want advanced caching or error tracing?
- Want to auto-annotate cells with answers?

Open an issue or submit a PR. 💥

## 🧷 License
MIT © 2025 SuperPandas Ltd 