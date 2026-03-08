"""State manager for orchestrator"""

from typing import Any


class StateManager:
    """Manages global and session state"""

    def __init__(self):
        self.global_state: dict[str, Any] = {}

    def set_state(self, key: str, value: Any) -> None:
        """Set state value

        Args:
            key: State key
            value: State value
        """
        self.global_state[key] = value

    def get_state(self, key: str) -> Any:
        """Get state value

        Args:
            key: State key

        Returns:
            State value or None
        """
        return self.global_state.get(key)

    def update_state(self, key: str, value: dict[str, Any]) -> None:
        """Update nested state

        Args:
            key: State key
            value: Values to merge
        """
        if key not in self.global_state:
            self.global_state[key] = {}
        if isinstance(self.global_state[key], dict):
            self.global_state[key].update(value)
