import os

try:
    from langsmith import Client
    from langchain_core.tracers import LangChainTracerV2
    from langchain_core.tracers import tracing_v2_enabled, enable_tracing_v2
except ImportError:
    Client = None
    tracing_v2_enabled = lambda: False
    enable_tracing_v2 = lambda: None

# Enable LangSmith tracing if environment variable is set
if os.environ.get("LANGCHAIN_TRACING_V2", "false").lower() in ("1", "true", "yes"):  # pragma: no cover
    enable_tracing_v2()
    # Optionally, you can set the project name via LANGCHAIN_PROJECT
    # and the API key via LANGCHAIN_API_KEY
    # See: https://docs.smith.langchain.com/docs/tracing/ for more info 