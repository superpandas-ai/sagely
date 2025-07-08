import pytest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

from sagely.usage_info import (
    UsageTracker,
    TokenUsage,
    add_usage,
    get_usage_tracker,
    get_session_total,
    get_session_summary,
    get_model_usage,
    get_all_model_usage,
    get_model_recent_usage,
    clear_usage_history,
    clear_model_history,
    get_session_id,
    get_session_file_path,
    get_all_session_files,
    load_session_from_file,
    load_latest_session
)


class TestTokenUsage:
    """Test the TokenUsage dataclass."""
    
    def test_token_usage_creation(self):
        """Test creating a TokenUsage instance."""
        usage = TokenUsage(
            input_tokens=100,
            output_tokens=50,
            total_tokens=150,
            timestamp=datetime.now(),
            model_name="gpt-4",
            request_type="test_request"
        )
        
        assert usage.input_tokens == 100
        assert usage.output_tokens == 50
        assert usage.total_tokens == 150
        assert usage.model_name == "gpt-4"
        assert usage.request_type == "test_request"
        assert isinstance(usage.timestamp, datetime)
    
    def test_token_usage_from_dict(self):
        """Test creating TokenUsage from dictionary."""
        usage_dict = {
            'input_tokens': 200,
            'output_tokens': 100,
            'total_tokens': 300,
            'model_name': 'gpt-4o',
            'request_type': 'web_search'
        }
        
        usage = TokenUsage.from_dict(usage_dict)
        assert usage.input_tokens == 200
        assert usage.output_tokens == 100
        assert usage.total_tokens == 300
        assert usage.model_name == 'gpt-4o'
        assert usage.request_type == 'web_search'
        assert isinstance(usage.timestamp, datetime)
    
    def test_token_usage_to_dict(self):
        """Test converting TokenUsage to dictionary."""
        timestamp = datetime.now()
        usage = TokenUsage(
            input_tokens=150,
            output_tokens=75,
            total_tokens=225,
            timestamp=timestamp,
            model_name="gpt-3.5-turbo",
            request_type="final_response"
        )
        
        usage_dict = usage.to_dict()
        assert usage_dict['input_tokens'] == 150
        assert usage_dict['output_tokens'] == 75
        assert usage_dict['total_tokens'] == 225
        assert usage_dict['model_name'] == "gpt-3.5-turbo"
        assert usage_dict['request_type'] == "final_response"
        assert 'timestamp' in usage_dict
    
    def test_token_usage_validation(self):
        """Test that TokenUsage validates input correctly."""
        # Test with zero tokens
        usage = TokenUsage(
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
            timestamp=datetime.now(),
            model_name="gpt-4",
            request_type="empty_request"
        )
        assert usage.total_tokens == 0
        
        # Test with large token counts
        usage = TokenUsage(
            input_tokens=1000000,
            output_tokens=500000,
            total_tokens=1500000,
            timestamp=datetime.now(),
            model_name="gpt-4",
            request_type="large_request"
        )
        assert usage.total_tokens == 1500000


class TestUsageTracker:
    """Test the UsageTracker class."""
    
    def setup_method(self):
        """Set up test environment."""
        clear_usage_history()
    
    def test_usage_tracker_initialization(self):
        """Test UsageTracker initialization."""
        tracker = UsageTracker()
        assert tracker.get_session_id() is not None
        assert len(tracker.get_session_id()) > 0
        assert len(tracker._usage_history) == 0
        assert len(tracker._model_usage) == 0
    
    def test_add_usage_basic(self):
        """Test basic usage addition."""
        tracker = UsageTracker()
        
        usage_data = {
            'input_tokens': 100,
            'output_tokens': 50,
            'total_tokens': 150
        }
        
        tracker.add_usage(usage_data, "gpt-4", "test_request")
        
        assert len(tracker._usage_history) == 1
        assert tracker._usage_history[0].input_tokens == 100
        assert tracker._usage_history[0].model_name == "gpt-4"
        assert tracker._usage_history[0].request_type == "test_request"
        
        # Check model-specific usage
        assert "gpt-4" in tracker._model_usage
        assert tracker._model_usage["gpt-4"].total_tokens == 150
    
    def test_add_usage_multiple_models(self):
        """Test adding usage for multiple models."""
        tracker = UsageTracker()
        
        # Add usage for different models
        tracker.add_usage({'input_tokens': 100, 'output_tokens': 50, 'total_tokens': 150}, "gpt-4", "request1")
        tracker.add_usage({'input_tokens': 200, 'output_tokens': 100, 'total_tokens': 300}, "gpt-4o", "request2")
        tracker.add_usage({'input_tokens': 150, 'output_tokens': 75, 'total_tokens': 225}, "gpt-4", "request3")
        
        assert len(tracker._usage_history) == 3
        assert len(tracker._model_usage) == 2
        
        # Check cumulative usage for gpt-4
        gpt4_usage = tracker._model_usage["gpt-4"]
        assert gpt4_usage.input_tokens == 250  # 100 + 150
        assert gpt4_usage.output_tokens == 125  # 50 + 75
        assert gpt4_usage.total_tokens == 375  # 150 + 225
        
        # Check usage for gpt-4o
        gpt4o_usage = tracker._model_usage["gpt-4o"]
        assert gpt4o_usage.total_tokens == 300
    
    def test_get_session_total(self):
        """Test getting total session usage."""
        tracker = UsageTracker()
        
        tracker.add_usage({'input_tokens': 100, 'output_tokens': 50, 'total_tokens': 150}, "gpt-4", "request1")
        tracker.add_usage({'input_tokens': 200, 'output_tokens': 100, 'total_tokens': 300}, "gpt-4o", "request2")
        
        total = tracker.get_session_total()
        assert total.input_tokens == 300
        assert total.output_tokens == 150
        assert total.total_tokens == 450
    
    def test_get_model_usage(self):
        """Test getting model-specific usage."""
        tracker = UsageTracker()
        
        tracker.add_usage({'input_tokens': 100, 'output_tokens': 50, 'total_tokens': 150}, "gpt-4", "request1")
        tracker.add_usage({'input_tokens': 200, 'output_tokens': 100, 'total_tokens': 300}, "gpt-4o", "request2")
        
        gpt4_usage = tracker.get_model_usage("gpt-4")
        assert gpt4_usage.total_tokens == 150
        assert gpt4_usage.model_name == "gpt-4"
        
        # Test non-existent model
        non_existent = tracker.get_model_usage("non-existent")
        assert non_existent.total_tokens == 0
        assert non_existent.model_name == "non-existent"
    
    def test_get_recent_usage(self):
        """Test getting recent usage entries."""
        tracker = UsageTracker()
        
        # Add multiple usage entries
        for i in range(5):
            tracker.add_usage(
                {'input_tokens': 100 + i, 'output_tokens': 50 + i, 'total_tokens': 150 + 2*i},
                "gpt-4",
                f"request{i}"
            )
        
        # Get recent 3 entries (returns last 3, in order they were added)
        recent = tracker.get_recent_usage(3)
        assert len(recent) == 3
        assert recent[0].request_type == "request2"  # Third entry
        assert recent[1].request_type == "request3"  # Fourth entry
        assert recent[2].request_type == "request4"  # Fifth entry (most recent)
        
        # Get more than available
        recent = tracker.get_recent_usage(10)
        assert len(recent) == 5
    
    def test_get_model_recent_usage(self):
        """Test getting recent usage for specific model."""
        tracker = UsageTracker()
        
        # Add usage for different models
        tracker.add_usage({'input_tokens': 100, 'output_tokens': 50, 'total_tokens': 150}, "gpt-4", "gpt4_request1")
        tracker.add_usage({'input_tokens': 200, 'output_tokens': 100, 'total_tokens': 300}, "gpt-4o", "gpt4o_request1")
        tracker.add_usage({'input_tokens': 150, 'output_tokens': 75, 'total_tokens': 225}, "gpt-4", "gpt4_request2")
        tracker.add_usage({'input_tokens': 250, 'output_tokens': 125, 'total_tokens': 375}, "gpt-4o", "gpt4o_request2")
        
        # Get recent gpt-4 usage (returns in order added, most recent last)
        gpt4_recent = tracker.get_model_recent_usage("gpt-4", 2)
        assert len(gpt4_recent) == 2
        assert all(usage.model_name == "gpt-4" for usage in gpt4_recent)
        assert gpt4_recent[0].request_type == "gpt4_request1"  # First gpt-4 request
        assert gpt4_recent[1].request_type == "gpt4_request2"  # Second gpt-4 request (most recent)
        
        # Get recent gpt-4o usage
        gpt4o_recent = tracker.get_model_recent_usage("gpt-4o", 1)
        assert len(gpt4o_recent) == 1
        assert gpt4o_recent[0].model_name == "gpt-4o"
    
    def test_clear_usage_history(self):
        """Test clearing usage history."""
        tracker = UsageTracker()
        
        tracker.add_usage({'input_tokens': 100, 'output_tokens': 50, 'total_tokens': 150}, "gpt-4", "request1")
        tracker.add_usage({'input_tokens': 200, 'output_tokens': 100, 'total_tokens': 300}, "gpt-4o", "request2")
        
        assert len(tracker._usage_history) == 2
        assert len(tracker._model_usage) == 2
        
        tracker.clear_history()
        
        assert len(tracker._usage_history) == 0
        assert len(tracker._model_usage) == 0
    
    def test_clear_model_history(self):
        """Test clearing history for specific model."""
        tracker = UsageTracker()
        
        tracker.add_usage({'input_tokens': 100, 'output_tokens': 50, 'total_tokens': 150}, "gpt-4", "request1")
        tracker.add_usage({'input_tokens': 200, 'output_tokens': 100, 'total_tokens': 300}, "gpt-4o", "request2")
        
        assert len(tracker._model_usage) == 2
        
        tracker.clear_model_history("gpt-4")
        
        assert "gpt-4" not in tracker._model_usage
        assert "gpt-4o" in tracker._model_usage
        assert len(tracker._model_usage) == 1


class TestFileBasedStorage:
    """Test file-based storage functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        clear_usage_history()
    
    def test_session_file_creation(self):
        """Test that session files are created correctly."""
        tracker = UsageTracker()
        
        # Add some usage to trigger file creation
        tracker.add_usage({'input_tokens': 100, 'output_tokens': 50, 'total_tokens': 150}, "gpt-4", "test_request")
        
        session_file = tracker.get_session_file_path()
        assert session_file.exists()
        assert session_file.name.startswith("usage_")
        assert session_file.name.endswith(".json")
        
        # Check file content
        with open(session_file, 'r') as f:
            data = json.load(f)
        
        assert 'session_id' in data
        assert 'session_start' in data
        assert 'usage_history' in data
        assert 'model_usage' in data
        assert data['session_id'] == tracker.get_session_id()
    
    def test_session_file_naming(self):
        """Test that session files have correct naming convention."""
        tracker = UsageTracker()
        tracker.add_usage({'input_tokens': 100, 'output_tokens': 50, 'total_tokens': 150}, "gpt-4", "test_request")
        
        session_file = tracker.get_session_file_path()
        filename = session_file.name
        
        # Check format: usage_YYYYMMDD_HHMMSS.json
        assert filename.startswith("usage_")
        assert filename.endswith(".json")
        
        # Extract timestamp part
        timestamp_part = filename[6:-5]  # Remove "usage_" and ".json"
        assert len(timestamp_part) == 15  # YYYYMMDD_HHMMSS
        
        # Check that it's a valid timestamp
        try:
            datetime.strptime(timestamp_part, "%Y%m%d_%H%M%S")
        except ValueError:
            pytest.fail("Invalid timestamp format in filename")
    
    def test_load_session_from_file(self):
        """Test loading session data from file."""
        tracker = UsageTracker()
        
        # Add usage data
        tracker.add_usage({'input_tokens': 100, 'output_tokens': 50, 'total_tokens': 150}, "gpt-4", "request1")
        tracker.add_usage({'input_tokens': 200, 'output_tokens': 100, 'total_tokens': 300}, "gpt-4o", "request2")
        
        session_file = tracker.get_session_file_path()
        
        # Load the session
        loaded_tracker = load_session_from_file(session_file)
        
        # Check that data matches
        assert loaded_tracker.get_session_id() == tracker.get_session_id()
        assert loaded_tracker.get_session_total().total_tokens == 450
        assert loaded_tracker.get_model_usage("gpt-4").total_tokens == 150
        assert loaded_tracker.get_model_usage("gpt-4o").total_tokens == 300
    
    def test_load_nonexistent_file(self):
        """Test loading a non-existent file."""
        # The load_from_file method handles exceptions gracefully
        tracker = load_session_from_file(Path("/nonexistent/file.json"))
        # Should return a fresh tracker with no data
        assert tracker.get_session_total().total_tokens == 0
    
    def test_load_invalid_json_file(self):
        """Test loading a file with invalid JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            temp_file = Path(f.name)
        
        try:
            # The load_from_file method handles exceptions gracefully
            tracker = load_session_from_file(temp_file)
            # Should return a fresh tracker with no data
            assert tracker.get_session_total().total_tokens == 0
        finally:
            temp_file.unlink()
    
    def test_get_all_session_files(self):
        """Test getting all session files."""
        # Create multiple sessions
        for i in range(3):
            tracker = UsageTracker()
            tracker.add_usage({'input_tokens': 100 + i, 'output_tokens': 50 + i, 'total_tokens': 150 + 2*i}, "gpt-4", f"request{i}")
        
        session_files = get_all_session_files()
        assert len(session_files) >= 3
        
        # Check that files are sorted by date (newest first)
        for i in range(len(session_files) - 1):
            assert session_files[i].name > session_files[i + 1].name
    
    def test_load_latest_session(self):
        """Test loading the latest session."""
        # Create multiple sessions
        for i in range(3):
            tracker = UsageTracker()
            tracker.add_usage({'input_tokens': 100 + i, 'output_tokens': 50 + i, 'total_tokens': 150 + 2*i}, "gpt-4", f"request{i}")
        
        latest_tracker = load_latest_session()
        assert latest_tracker is not None
        assert latest_tracker.get_session_total().total_tokens > 0


class TestIntegrationTests:
    """Integration tests for usage tracking."""
    
    def setup_method(self):
        """Set up test environment."""
        clear_usage_history()
    
    def test_end_to_end_usage_tracking(self):
        """Test complete end-to-end usage tracking workflow."""
        # Start with clean state
        assert get_session_total().total_tokens == 0
        
        # Add usage through the public API
        add_usage({'input_tokens': 100, 'output_tokens': 50, 'total_tokens': 150}, "gpt-4", "initial_response")
        add_usage({'input_tokens': 200, 'output_tokens': 100, 'total_tokens': 300}, "gpt-4o", "web_search")
        add_usage({'input_tokens': 150, 'output_tokens': 75, 'total_tokens': 225}, "gpt-4", "final_response")
        
        # Check total usage
        total = get_session_total()
        assert total.input_tokens == 450
        assert total.output_tokens == 225
        assert total.total_tokens == 675
        
        # Check model-specific usage
        gpt4_usage = get_model_usage("gpt-4")
        assert gpt4_usage.total_tokens == 375  # 150 + 225
        
        gpt4o_usage = get_model_usage("gpt-4o")
        assert gpt4o_usage.total_tokens == 300
        
        # Check recent usage (returns in order added, most recent last)
        recent = get_model_recent_usage("gpt-4", 2)
        assert len(recent) == 2
        assert recent[0].request_type == "initial_response"  # First gpt-4 request
        assert recent[1].request_type == "final_response"    # Second gpt-4 request (most recent)
        
        # Check session summary
        summary = get_session_summary()
        assert "Session Token Usage" in summary
        assert "gpt-4" in summary
        assert "gpt-4o" in summary
        
        # Check file persistence
        session_file = get_session_file_path()
        assert session_file.exists()
        
        # Load from file and verify
        loaded_tracker = load_session_from_file(session_file)
        assert loaded_tracker.get_session_total().total_tokens == 675
    
    def test_concurrent_session_handling(self):
        """Test handling of multiple concurrent sessions."""
        # Create first session
        tracker1 = UsageTracker()
        tracker1.add_usage({'input_tokens': 100, 'output_tokens': 50, 'total_tokens': 150}, "gpt-4", "request1")
        
        # Create second session
        tracker2 = UsageTracker()
        tracker2.add_usage({'input_tokens': 200, 'output_tokens': 100, 'total_tokens': 300}, "gpt-4o", "request2")
        
        # Verify sessions have independent data
        assert tracker1.get_session_total().total_tokens == 150
        assert tracker2.get_session_total().total_tokens == 300
        
        # The file path may be the same if created within the same second, so we only check in-memory data
        assert len(tracker1._usage_history) == 1
        assert len(tracker2._usage_history) == 1
        assert tracker1._usage_history[0].request_type == "request1"
        assert tracker2._usage_history[0].request_type == "request2"
        
        # Verify that each tracker has its own data
        assert len(tracker1._usage_history) == 1
        assert len(tracker2._usage_history) == 1
        assert tracker1._usage_history[0].request_type == "request1"
        assert tracker2._usage_history[0].request_type == "request2"
    
    def test_error_handling(self):
        """Test error handling in usage tracking."""
        tracker = UsageTracker()
        
        # Test with invalid usage data (should handle gracefully)
        tracker.add_usage({'invalid_key': 100}, "gpt-4", "test_request")
        # Should use default values (0) for missing keys
        assert tracker.get_session_total().total_tokens == 0
        
        # Test with missing required fields (should handle gracefully)
        tracker.add_usage({'input_tokens': 100}, "gpt-4", "test_request")
        # Should use default values for missing output_tokens and total_tokens
        total = tracker.get_session_total()
        assert total.input_tokens == 100
        assert total.output_tokens == 0
        assert total.total_tokens == 0
        
        # Test with negative token counts
        tracker.add_usage({'input_tokens': -10, 'output_tokens': -5, 'total_tokens': -15}, "gpt-4", "negative_request")
        # Should not raise error, but should handle gracefully
        assert tracker.get_session_total().total_tokens == -15
    
    def test_large_usage_scenarios(self):
        """Test handling of large usage scenarios."""
        tracker = UsageTracker()
        
        # Add many small requests
        for i in range(1000):
            tracker.add_usage(
                {'input_tokens': 10, 'output_tokens': 5, 'total_tokens': 15},
                "gpt-4",
                f"request_{i}"
            )
        
        assert len(tracker._usage_history) == 1000
        assert tracker.get_session_total().total_tokens == 15000
        
        # Test with very large token counts
        tracker.add_usage(
            {'input_tokens': 1000000, 'output_tokens': 500000, 'total_tokens': 1500000},
            "gpt-4",
            "large_request"
        )
        
        assert tracker.get_session_total().total_tokens == 1515000
    
    def test_model_name_variations(self):
        """Test handling of different model name formats."""
        tracker = UsageTracker()
        
        # Test various model name formats
        model_names = [
            "gpt-4",
            "gpt-4o",
            "gpt-3.5-turbo",
            "claude-3-opus",
            "claude-3-sonnet",
            "gemini-pro",
            "llama-2-70b",
            "custom-model-v1"
        ]
        
        for i, model_name in enumerate(model_names):
            tracker.add_usage(
                {'input_tokens': 100 + i, 'output_tokens': 50 + i, 'total_tokens': 150 + 2*i},
                model_name,
                f"request_{i}"
            )
        
        assert len(tracker._model_usage) == len(model_names)
        
        # Check each model
        for model_name in model_names:
            usage = tracker.get_model_usage(model_name)
            assert usage.model_name == model_name
            assert usage.total_tokens > 0


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def setup_method(self):
        """Set up test environment."""
        clear_usage_history()
    
    def test_zero_tokens(self):
        """Test handling of zero token usage."""
        tracker = UsageTracker()
        
        tracker.add_usage({'input_tokens': 0, 'output_tokens': 0, 'total_tokens': 0}, "gpt-4", "empty_request")
        
        total = tracker.get_session_total()
        assert total.input_tokens == 0
        assert total.output_tokens == 0
        assert total.total_tokens == 0
        
        # Should still create a history entry
        assert len(tracker._usage_history) == 1
        assert tracker._usage_history[0].request_type == "empty_request"
    
    def test_very_large_numbers(self):
        """Test handling of very large token numbers."""
        tracker = UsageTracker()
        
        large_usage = {
            'input_tokens': 999999999,
            'output_tokens': 999999999,
            'total_tokens': 1999999998
        }
        
        tracker.add_usage(large_usage, "gpt-4", "huge_request")
        
        total = tracker.get_session_total()
        assert total.input_tokens == 999999999
        assert total.output_tokens == 999999999
        assert total.total_tokens == 1999999998
    
    def test_special_characters_in_request_type(self):
        """Test handling of special characters in request types."""
        tracker = UsageTracker()
        
        special_request_types = [
            "request with spaces",
            "request-with-dashes",
            "request_with_underscores",
            "request.with.dots",
            "request!with!exclamation",
            "request@with@at",
            "request#with#hash",
            "request$with$dollar",
            "request%with%percent",
            "request^with^caret",
            "request&with&ampersand",
            "request*with*asterisk",
            "request(with)parentheses",
            "request[with]brackets",
            "request{with}braces",
            "request|with|pipe",
            "request\\with\\backslash",
            "request/with/forward/slash",
            "request:with:colon",
            "request;with;semicolon",
            "request\"with\"quotes",
            "request'with'apostrophe",
            "request<with>angle>brackets",
            "request,with,commas",
            "request.with.multiple.dots",
            "request_with_very_long_name_that_goes_on_and_on_and_on",
            "request with unicode: 🚀✨🎉",
            "request with emoji: 😀😃😄😁😆😅😂🤣",
            "request with numbers: 1234567890",
            "request with mixed: AaBbCc123!@#$%^&*()",
            "",  # Empty string
            "   ",  # Whitespace only
            "\n\t\r",  # Control characters
        ]
        
        for i, request_type in enumerate(special_request_types):
            tracker.add_usage(
                {'input_tokens': 10 + i, 'output_tokens': 5 + i, 'total_tokens': 15 + 2*i},
                "gpt-4",
                request_type
            )
        
        # Verify all were added
        assert len(tracker._usage_history) == len(special_request_types)
        
        # Check that we can retrieve them
        for i, request_type in enumerate(special_request_types):
            assert tracker._usage_history[i].request_type == request_type
    
    def test_unicode_model_names(self):
        """Test handling of unicode model names."""
        tracker = UsageTracker()
        
        unicode_model_names = [
            "gpt-4-🚀",
            "claude-3-✨",
            "gemini-🎉",
            "llama-2-😀",
            "custom-model-🌟",
            "model-with-emoji-🎯",
            "model_with_unicode_测试",
            "model_with_unicode_тест",
            "model_with_unicode_テスト",
            "model_with_unicode_اختبار",
            "model_with_unicode_בדיקה",
            "model_with_unicode_परीक्षण",
            "model_with_unicode_ทดสอบ",
            "model_with_unicode_kiểm_tra",
            "model_with_unicode_테스트",
        ]
        
        for i, model_name in enumerate(unicode_model_names):
            tracker.add_usage(
                {'input_tokens': 10 + i, 'output_tokens': 5 + i, 'total_tokens': 15 + 2*i},
                model_name,
                f"request_{i}"
            )
        
        # Verify all were added
        assert len(tracker._model_usage) == len(unicode_model_names)
        
        # Check that we can retrieve them
        for model_name in unicode_model_names:
            usage = tracker.get_model_usage(model_name)
            assert usage.model_name == model_name
            assert usage.total_tokens > 0
    
    def test_file_system_edge_cases(self):
        """Test file system edge cases."""
        tracker = UsageTracker()
        
        # Test with very long session ID
        # This would be handled by the session ID generation, but we can test the file path
        session_file = tracker.get_session_file_path()
        
        # Test that file path is reasonable length
        assert len(str(session_file)) < 500  # Reasonable path length
        
        # Test that we can write and read the file
        tracker.add_usage({'input_tokens': 100, 'output_tokens': 50, 'total_tokens': 150}, "gpt-4", "test_request")
        
        assert session_file.exists()
        assert session_file.stat().st_size > 0
        
        # Test loading the file
        loaded_tracker = load_session_from_file(session_file)
        assert loaded_tracker.get_session_total().total_tokens == 150
    
    # def test_memory_usage_with_large_history(self):
    #     """Test memory usage with large history."""
    #     tracker = UsageTracker()
        
    #     # Add many entries to test memory usage
    #     for i in range(10000):
    #         tracker.add_usage(
    #             {'input_tokens': 10, 'output_tokens': 5, 'total_tokens': 15},
    #             "gpt-4",
    #             f"request_{i}"
    #         )
        
    #     # Verify we can still access data
    #     assert len(tracker.usage_history) == 10000
    #     assert tracker.get_session_total().total_tokens == 150000
        
    #     # Test getting recent usage
    #     recent = tracker.get_recent_usage(100)
    #     assert len(recent) == 100
        
    #     # Test model-specific recent usage
    #     model_recent = tracker.get_model_recent_usage("gpt-4", 50)
    #     assert len(model_recent) == 50
        
    #     # Test summary generation
    #     summary = tracker.get_session_summary()
    #     assert "Session Token Usage" in summary
    #     assert "gpt-4" in summary


if __name__ == "__main__":
    pytest.main([__file__]) 