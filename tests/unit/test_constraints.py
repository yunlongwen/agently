"""Tests for constraints module"""

import pytest
from unittest.mock import Mock, patch

from agently.constraints.memory import MemoryLimiter, MemoryTracker
from agently.constraints.timing import ResponseTimeMonitor, TimeoutManager
from agently.constraints.concurrency import ConcurrencyLimiter, SessionManager
from agently.constraints.security import SecurityManager, ResourceLimiter


class TestMemoryLimiter:
    """Test MemoryLimiter"""

    def test_init(self):
        """Test initializing memory limiter"""
        limiter = MemoryLimiter(max_mb=1024)
        assert limiter.max_mb == 1024

    def test_check_memory(self):
        """Test checking memory usage"""
        limiter = MemoryLimiter(max_mb=4096)
        result = limiter.check_memory()
        assert isinstance(result, dict)
        assert "current_mb" in result

    def test_is_within_limit(self):
        """Test checking if within limit"""
        limiter = MemoryLimiter(max_mb=4096)
        with patch.object(limiter, 'get_current_memory_mb', return_value=100):
            assert limiter.is_within_limit() is True

    def test_exceeds_limit(self):
        """Test when memory exceeds limit"""
        limiter = MemoryLimiter(max_mb=100)
        with patch.object(limiter, 'get_current_memory_mb', return_value=150):
            assert limiter.is_within_limit() is False


class TestMemoryTracker:
    """Test MemoryTracker"""

    def test_init(self):
        """Test initializing memory tracker"""
        tracker = MemoryTracker()
        assert tracker.snapshots == []

    def test_take_snapshot(self):
        """Test taking memory snapshot"""
        tracker = MemoryTracker()
        tracker.take_snapshot("test")
        assert len(tracker.snapshots) == 1

    def test_get_usage_trend(self):
        """Test getting usage trend"""
        tracker = MemoryTracker()
        tracker.take_snapshot("start")
        tracker.take_snapshot("end")
        trend = tracker.get_usage_trend()
        assert isinstance(trend, dict)


class TestResponseTimeMonitor:
    """Test ResponseTimeMonitor"""

    def test_init(self):
        """Test initializing response time monitor"""
        monitor = ResponseTimeMonitor()
        assert monitor.measurements == []

    def test_start_timer(self):
        """Test starting timer"""
        monitor = ResponseTimeMonitor()
        monitor.start_timer("test_task")
        assert "test_task" in monitor.timers

    def test_stop_timer(self):
        """Test stopping timer"""
        monitor = ResponseTimeMonitor()
        monitor.start_timer("test_task")
        result = monitor.stop_timer("test_task")
        assert isinstance(result, float)
        assert result >= 0

    def test_get_average_response_time(self):
        """Test getting average response time"""
        from agently.constraints.timing import TimingMeasurement
        monitor = ResponseTimeMonitor()
        monitor.measurements = [
            TimingMeasurement(task="t1", duration_seconds=1.0),
            TimingMeasurement(task="t2", duration_seconds=2.0),
            TimingMeasurement(task="t3", duration_seconds=3.0),
        ]
        avg = monitor.get_average_response_time()
        assert avg == 2.0


class TestTimeoutManager:
    """Test TimeoutManager"""

    def test_init(self):
        """Test initializing timeout manager"""
        manager = TimeoutManager()
        assert "simple" in manager.timeouts
        assert manager.timeouts["simple"] == 30

    def test_set_timeout(self):
        """Test setting timeout"""
        manager = TimeoutManager()
        manager.set_timeout("simple", 30)
        assert manager.timeouts["simple"] == 30

    def test_get_timeout_for_task(self):
        """Test getting timeout for task"""
        manager = TimeoutManager()
        # Short task should use simple timeout
        timeout = manager.get_timeout_for_task("simple")
        assert timeout == 30

        # Long task (>50 words) should use complex timeout
        long_task = " ".join(["word"] * 60)
        timeout = manager.get_timeout_for_task(long_task)
        assert timeout == 120


class TestConcurrencyLimiter:
    """Test ConcurrencyLimiter"""

    def test_init(self):
        """Test initializing concurrency limiter"""
        limiter = ConcurrencyLimiter(max_concurrent=5)
        assert limiter.max_concurrent == 5

    def test_can_acquire(self):
        """Test checking if can acquire slot"""
        limiter = ConcurrencyLimiter(max_concurrent=2)
        assert limiter.can_acquire() is True

    def test_acquire_and_release(self):
        """Test acquiring and releasing slot"""
        limiter = ConcurrencyLimiter(max_concurrent=1)
        assert limiter.acquire() is True
        assert limiter.can_acquire() is False
        limiter.release()
        assert limiter.can_acquire() is True


class TestSessionManager:
    """Test SessionManager"""

    def test_init(self):
        """Test initializing session manager"""
        manager = SessionManager(max_sessions=5)
        assert manager.max_sessions == 5

    def test_create_session(self):
        """Test creating session"""
        manager = SessionManager()
        session_id = manager.create_session()
        assert session_id is not None
        assert session_id in manager.sessions

    def test_get_session(self):
        """Test getting session"""
        manager = SessionManager()
        session_id = manager.create_session()
        session = manager.get_session(session_id)
        assert session is not None

    def test_destroy_session(self):
        """Test destroying session"""
        manager = SessionManager()
        session_id = manager.create_session()
        manager.destroy_session(session_id)
        assert session_id not in manager.sessions


class TestSecurityManager:
    """Test SecurityManager"""

    def test_init(self):
        """Test initializing security manager"""
        manager = SecurityManager()
        assert manager is not None

    def test_validate_command_allowed(self):
        """Test validating allowed command"""
        manager = SecurityManager()
        result = manager.validate_command("ls -la")
        assert result["allowed"] is True

    def test_validate_command_blocked(self):
        """Test validating blocked command"""
        manager = SecurityManager()
        result = manager.validate_command("rm -rf /")
        assert result["allowed"] is False


class TestResourceLimiter:
    """Test ResourceLimiter"""

    def test_init(self):
        """Test initializing resource limiter"""
        limiter = ResourceLimiter()
        assert "cpu_percent" in limiter.limits
        assert limiter.limits["cpu_percent"] == 80.0

    def test_set_limit(self):
        """Test setting resource limit"""
        limiter = ResourceLimiter()
        limiter.set_limit("cpu_percent", 80)
        assert limiter.limits["cpu_percent"] == 80

    def test_check_resource(self):
        """Test checking resource"""
        limiter = ResourceLimiter()
        limiter.set_limit("memory_mb", 1024)
        result = limiter.check_resource("memory_mb", 512)
        assert result["within_limit"] is True
