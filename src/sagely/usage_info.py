"""
Token usage tracking for sagely package.
"""

from typing import Dict, Any, List
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json
import os
from pathlib import Path


@dataclass
class TokenUsage:
    """Track token usage for a single request."""
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    model_name: str = ""
    request_type: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'input_tokens': self.input_tokens,
            'output_tokens': self.output_tokens,
            'total_tokens': self.total_tokens,
            'timestamp': self.timestamp.isoformat(),
            'model_name': self.model_name,
            'request_type': self.request_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TokenUsage':
        """Create from dictionary."""
        return cls(
            input_tokens=data.get('input_tokens', 0),
            output_tokens=data.get('output_tokens', 0),
            total_tokens=data.get('total_tokens', 0),
            timestamp=datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat())),
            model_name=data.get('model_name', ''),
            request_type=data.get('request_type', '')
        )


class UsageTracker:
    """Track token usage across the entire session, separated by model."""
    
    def __init__(self):
        self._usage_history: list[TokenUsage] = []
        self._model_usage: Dict[str, TokenUsage] = {}  # Track usage per model
        self._session_start = datetime.now()
        self._session_id = self._session_start.strftime("%Y%m%d_%H%M%S")
        self._usage_dir = Path.home() / ".sagely" / "usage_data"
        self._usage_file = self._usage_dir / f"usage_{self._session_id}.json"
        
        # Ensure usage directory exists
        self._usage_dir.mkdir(parents=True, exist_ok=True)
    
    def add_usage(self, usage_metadata: Dict[str, Any], model_name: str = "", request_type: str = "") -> None:
        """Add token usage from a response."""
        if not usage_metadata:
            return
            
        usage = TokenUsage(
            input_tokens=usage_metadata.get('input_tokens', 0),
            output_tokens=usage_metadata.get('output_tokens', 0),
            total_tokens=usage_metadata.get('total_tokens', 0),
            model_name=model_name,
            request_type=request_type
        )
        self._usage_history.append(usage)
        
        # Update model-specific usage
        if model_name not in self._model_usage:
            self._model_usage[model_name] = TokenUsage(model_name=model_name)
        
        model_usage = self._model_usage[model_name]
        model_usage.input_tokens += usage.input_tokens
        model_usage.output_tokens += usage.output_tokens
        model_usage.total_tokens += usage.total_tokens
        
        # Save to file after each usage addition
        self._save_to_file()
    
    def get_session_total(self) -> TokenUsage:
        """Get total usage for the current session across all models."""
        total = TokenUsage()
        for usage in self._usage_history:
            total.input_tokens += usage.input_tokens
            total.output_tokens += usage.output_tokens
            total.total_tokens += usage.total_tokens
        return total
    
    def get_model_usage(self, model_name: str) -> TokenUsage:
        """Get usage for a specific model."""
        return self._model_usage.get(model_name, TokenUsage(model_name=model_name))
    
    def get_all_model_usage(self) -> Dict[str, TokenUsage]:
        """Get usage for all models."""
        return self._model_usage.copy()
    
    def get_session_summary(self) -> str:
        """Get a formatted summary of session usage with model breakdown."""
        total = self.get_session_total()
        session_duration = datetime.now() - self._session_start
        
        summary = f"Session Token Usage:\n"
        summary += f"  Total input tokens: {total.input_tokens:,}\n"
        summary += f"  Total output tokens: {total.output_tokens:,}\n"
        summary += f"  Total tokens: {total.total_tokens:,}\n"
        summary += f"  Session duration: {session_duration}\n"
        summary += f"  Total requests: {len(self._usage_history)}"
        
        # Add model breakdown
        if self._model_usage:
            summary += f"\n\nModel Breakdown:"
            for model_name, model_usage in self._model_usage.items():
                summary += f"\n  {model_name}:"
                summary += f"\n    Input tokens: {model_usage.input_tokens:,}"
                summary += f"\n    Output tokens: {model_usage.output_tokens:,}"
                summary += f"\n    Total tokens: {model_usage.total_tokens:,}"
                summary += f"\n    Requests: {self._get_model_request_count(model_name)}"
        
        return summary
    
    def _get_model_request_count(self, model_name: str) -> int:
        """Get the number of requests for a specific model."""
        return sum(1 for usage in self._usage_history if usage.model_name == model_name)
    
    def clear_history(self) -> None:
        """Clear usage history."""
        self._usage_history.clear()
        self._model_usage.clear()
        self._session_start = datetime.now()
    
    def clear_model_history(self, model_name: str) -> None:
        """Clear usage history for a specific model."""
        self._usage_history = [usage for usage in self._usage_history if usage.model_name != model_name]
        if model_name in self._model_usage:
            del self._model_usage[model_name]
    
    def get_recent_usage(self, count: int = 5) -> list[TokenUsage]:
        """Get the most recent usage entries."""
        return self._usage_history[-count:] if self._usage_history else []
    
    def get_model_recent_usage(self, model_name: str, count: int = 5) -> list[TokenUsage]:
        """Get the most recent usage entries for a specific model."""
        model_usage = [usage for usage in self._usage_history if usage.model_name == model_name]
        return model_usage[-count:] if model_usage else []
    
    def _save_to_file(self) -> None:
        """Save current usage data to JSON file."""
        try:
            data = {
                'session_id': self._session_id,
                'session_start': self._session_start.isoformat(),
                'usage_history': [usage.to_dict() for usage in self._usage_history],
                'model_usage': {
                    model_name: usage.to_dict() 
                    for model_name, usage in self._model_usage.items()
                }
            }
            
            with open(self._usage_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            # Silently fail to avoid disrupting the main functionality
            pass
    
    def get_session_file_path(self) -> Path:
        """Get the file path for the current session's usage data."""
        return self._usage_file
    
    def get_session_id(self) -> str:
        """Get the current session ID."""
        return self._session_id
    
    @classmethod
    def load_from_file(cls, file_path: Path) -> 'UsageTracker':
        """Load usage data from a JSON file."""
        tracker = cls()
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Load session info
            tracker._session_id = data.get('session_id', tracker._session_id)
            tracker._session_start = datetime.fromisoformat(data.get('session_start', tracker._session_start.isoformat()))
            tracker._usage_file = file_path
            
            # Load usage history
            tracker._usage_history = [
                TokenUsage.from_dict(usage_data) 
                for usage_data in data.get('usage_history', [])
            ]
            
            # Rebuild model usage from history
            tracker._model_usage.clear()
            for usage in tracker._usage_history:
                if usage.model_name not in tracker._model_usage:
                    tracker._model_usage[usage.model_name] = TokenUsage(model_name=usage.model_name)
                
                model_usage = tracker._model_usage[usage.model_name]
                model_usage.input_tokens += usage.input_tokens
                model_usage.output_tokens += usage.output_tokens
                model_usage.total_tokens += usage.total_tokens
                
        except Exception as e:
            # If loading fails, return a fresh tracker
            pass
        
        return tracker
    
    @classmethod
    def get_all_session_files(cls) -> List[Path]:
        """Get all usage data files."""
        usage_dir = Path.home() / ".sagely" / "usage_data"
        if not usage_dir.exists():
            return []
        
        return sorted(usage_dir.glob("usage_*.json"), reverse=True)
    
    @classmethod
    def load_latest_session(cls) -> 'UsageTracker':
        """Load the most recent session file."""
        session_files = cls.get_all_session_files()
        if not session_files:
            return cls()
        
        return cls.load_from_file(session_files[0])


# Global usage tracker instance
_usage_tracker = UsageTracker()


def get_usage_tracker() -> UsageTracker:
    """Get the global usage tracker instance."""
    return _usage_tracker


def add_usage(usage_metadata: Dict[str, Any], model_name: str = "", request_type: str = "") -> None:
    """Add token usage to the global tracker."""
    _usage_tracker.add_usage(usage_metadata, model_name, request_type)


def get_session_total() -> TokenUsage:
    """Get total usage for the current session."""
    return _usage_tracker.get_session_total()


def get_session_summary() -> str:
    """Get a formatted summary of session usage."""
    return _usage_tracker.get_session_summary()


def clear_usage_history() -> None:
    """Clear usage history."""
    _usage_tracker.clear_history()


def get_model_usage(model_name: str) -> TokenUsage:
    """Get usage for a specific model."""
    return _usage_tracker.get_model_usage(model_name)


def get_all_model_usage() -> Dict[str, TokenUsage]:
    """Get usage for all models."""
    return _usage_tracker.get_all_model_usage()


def clear_model_history(model_name: str) -> None:
    """Clear usage history for a specific model."""
    _usage_tracker.clear_model_history(model_name)


def get_model_recent_usage(model_name: str, count: int = 5) -> list[TokenUsage]:
    """Get the most recent usage entries for a specific model."""
    return _usage_tracker.get_model_recent_usage(model_name, count)


def get_session_file_path() -> Path:
    """Get the file path for the current session's usage data."""
    return _usage_tracker.get_session_file_path()


def get_session_id() -> str:
    """Get the current session ID."""
    return _usage_tracker.get_session_id()


def get_all_session_files() -> List[Path]:
    """Get all usage data files."""
    return UsageTracker.get_all_session_files()


def load_session_from_file(file_path: Path) -> UsageTracker:
    """Load usage data from a specific file."""
    return UsageTracker.load_from_file(file_path)


def load_latest_session() -> UsageTracker:
    """Load the most recent session file."""
    return UsageTracker.load_latest_session() 