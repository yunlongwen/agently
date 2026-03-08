"""Concurrency constraint management"""

import threading
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Session:
    """Session information"""

    session_id: str
    created_at: float
    data: dict[str, Any] = field(default_factory=dict)


class ConcurrencyLimiter:
    """Limits concurrent operations"""

    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self._current = 0
        self._lock = threading.Lock()

    def can_acquire(self) -> bool:
        """Check if can acquire a slot

        Returns:
            True if slot available
        """
        with self._lock:
            return self._current < self.max_concurrent

    def acquire(self) -> bool:
        """Acquire a slot

        Returns:
            True if acquired
        """
        with self._lock:
            if self._current < self.max_concurrent:
                self._current += 1
                return True
            return False

    def release(self) -> None:
        """Release a slot"""
        with self._lock:
            if self._current > 0:
                self._current -= 1


class SessionManager:
    """Manages user sessions"""

    def __init__(self, max_sessions: int = 5):
        self.max_sessions = max_sessions
        self.sessions: dict[str, Session] = {}
        self._lock = threading.Lock()

    def create_session(self) -> str:
        """Create a new session

        Returns:
            Session ID
        """
        import time

        with self._lock:
            if len(self.sessions) >= self.max_sessions:
                oldest = min(self.sessions.values(), key=lambda s: s.created_at)
                del self.sessions[oldest.session_id]

            session_id = str(uuid.uuid4())
            session = Session(
                session_id=session_id,
                created_at=time.time(),
            )
            self.sessions[session_id] = session
            return session_id

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID

        Args:
            session_id: Session identifier

        Returns:
            Session or None
        """
        return self.sessions.get(session_id)

    def destroy_session(self, session_id: str) -> None:
        """Destroy a session

        Args:
            session_id: Session identifier
        """
        with self._lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
