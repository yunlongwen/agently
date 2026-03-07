"""Concurrency constraints - Session and concurrency management"""

import threading
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Session:
    """Session information"""
    id: str
    created_at: float = field(default_factory=lambda: __import__('time').time())
    last_active: float = field(default_factory=lambda: __import__('time').time())
    context: Dict[str, Any] = field(default_factory=dict)
    status: str = "active"


class ConcurrencyLimiter:
    """
    Concurrency Limiter - 并发限制器

    限制并发任务数量，支持3-5个并发会话。
    """

    def __init__(self, max_concurrent: int = 5):
        """
        Initialize concurrency limiter

        Args:
            max_concurrent: Maximum concurrent tasks (default: 5)
        """
        self.max_concurrent = max(1, min(max_concurrent, 10))  # Clamp between 1-10
        self._current = 0
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)

    def can_acquire(self) -> bool:
        """Check if a slot is available"""
        with self._lock:
            return self._current < self.max_concurrent

    def acquire(self, blocking: bool = True, timeout: Optional[float] = None) -> bool:
        """
        Acquire a concurrency slot

        Args:
            blocking: Whether to block until available
            timeout: Maximum time to wait (seconds)

        Returns:
            True if acquired, False otherwise
        """
        with self._condition:
            if not blocking:
                if self._current < self.max_concurrent:
                    self._current += 1
                    return True
                return False

            # Wait until a slot is available or timeout
            wait_result = self._condition.wait_for(
                lambda: self._current < self.max_concurrent,
                timeout=timeout
            )

            if wait_result:
                self._current += 1
                return True
            return False

    def release(self) -> None:
        """Release a concurrency slot"""
        with self._condition:
            if self._current > 0:
                self._current -= 1
                self._condition.notify()

    def get_status(self) -> Dict[str, Any]:
        """Get current concurrency status"""
        with self._lock:
            return {
                "current": self._current,
                "max": self.max_concurrent,
                "available": self.max_concurrent - self._current,
                "utilization": self._current / self.max_concurrent * 100,
            }

    def __enter__(self):
        """Context manager entry"""
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.release()
        return False


class SessionManager:
    """
    Session Manager - 会话管理器

    管理并发会话，支持3-5个并发上下文。
    """

    def __init__(self, max_sessions: int = 5):
        """
        Initialize session manager

        Args:
            max_sessions: Maximum concurrent sessions (default: 5)
        """
        self.max_sessions = max(1, min(max_sessions, 10))
        self.sessions: Dict[str, Session] = {}
        self._lock = threading.Lock()
        self._session_limiter = ConcurrencyLimiter(max_sessions)

    def create_session(self, context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Create a new session

        Args:
            context: Initial session context

        Returns:
            Session ID or None if limit reached
        """
        if not self._session_limiter.acquire(blocking=False):
            return None

        session_id = str(uuid.uuid4())[:8]
        session = Session(
            id=session_id,
            context=context or {},
        )

        with self._lock:
            self.sessions[session_id] = session

        return session_id

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID"""
        with self._lock:
            session = self.sessions.get(session_id)
            if session:
                import time
                session.last_active = time.time()
            return session

    def update_session(self, session_id: str, context: Dict[str, Any]) -> bool:
        """Update session context"""
        with self._lock:
            session = self.sessions.get(session_id)
            if session:
                session.context.update(context)
                import time
                session.last_active = time.time()
                return True
            return False

    def destroy_session(self, session_id: str) -> bool:
        """Destroy a session"""
        with self._lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
                self._session_limiter.release()
                return True
            return False

    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all active sessions"""
        with self._lock:
            return [
                {
                    "id": s.id,
                    "created_at": s.created_at,
                    "last_active": s.last_active,
                    "status": s.status,
                }
                for s in self.sessions.values()
            ]

    def get_session_count(self) -> int:
        """Get number of active sessions"""
        with self._lock:
            return len(self.sessions)

    def cleanup_inactive_sessions(self, max_idle_seconds: float = 3600) -> int:
        """
        Clean up inactive sessions

        Args:
            max_idle_seconds: Maximum idle time before cleanup

        Returns:
            Number of sessions cleaned up
        """
        import time
        current_time = time.time()
        to_remove = []

        with self._lock:
            for session_id, session in self.sessions.items():
                if current_time - session.last_active > max_idle_seconds:
                    to_remove.append(session_id)

        for session_id in to_remove:
            self.destroy_session(session_id)

        return len(to_remove)

    def get_status(self) -> Dict[str, Any]:
        """Get session manager status"""
        return {
            "active_sessions": self.get_session_count(),
            "max_sessions": self.max_sessions,
            "available_slots": self.max_sessions - self.get_session_count(),
            "limiter_status": self._session_limiter.get_status(),
        }
