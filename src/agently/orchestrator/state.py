"""State Manager - Manages execution state"""

from typing import Any, Dict, List, Optional


class StateManager:
    """
    State Manager - 状态管理器

    管理全局状态、会话状态和上下文传递。
    """

    def __init__(self):
        self.global_state: Dict[str, Any] = {}
        self.session_states: Dict[str, Dict[str, Any]] = {}
        self.context_history: Dict[str, List[Dict[str, Any]]] = {}

    def set_state(self, key: str, value: Any) -> None:
        """Set global state value"""
        self.global_state[key] = value

    def get_state(self, key: str, default: Any = None) -> Any:
        """Get global state value"""
        return self.global_state.get(key, default)

    def update_state(self, key: str, value: Dict[str, Any]) -> None:
        """Update global state (merge dictionaries)"""
        if key in self.global_state and isinstance(self.global_state[key], dict):
            if isinstance(value, dict):
                self.global_state[key].update(value)
            else:
                self.global_state[key] = value
        else:
            self.global_state[key] = value

    def delete_state(self, key: str) -> None:
        """Delete global state value"""
        if key in self.global_state:
            del self.global_state[key]

    def create_session(self, session_id: str) -> None:
        """Create a new session"""
        self.session_states[session_id] = {}
        self.context_history[session_id] = []

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session state"""
        return self.session_states.get(session_id)

    def update_session(self, session_id: str, data: Dict[str, Any]) -> None:
        """Update session state"""
        if session_id not in self.session_states:
            self.create_session(session_id)

        self.session_states[session_id].update(data)

    def delete_session(self, session_id: str) -> None:
        """Delete a session"""
        if session_id in self.session_states:
            del self.session_states[session_id]
        if session_id in self.context_history:
            del self.context_history[session_id]

    def add_to_history(self, session_id: str, entry: Dict[str, Any]) -> None:
        """Add entry to session history"""
        if session_id not in self.context_history:
            self.context_history[session_id] = []

        self.context_history[session_id].append(entry)

    def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get session history"""
        return self.context_history.get(session_id, [])

    def clear_history(self, session_id: str) -> None:
        """Clear session history"""
        if session_id in self.context_history:
            self.context_history[session_id] = []

    def get_all_sessions(self) -> Dict[str, Dict[str, Any]]:
        """Get all session states"""
        return self.session_states.copy()

    def clear_all(self) -> None:
        """Clear all state"""
        self.global_state.clear()
        self.session_states.clear()
        self.context_history.clear()
