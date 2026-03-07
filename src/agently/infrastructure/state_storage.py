"""State storage service for managing application state"""

import json
from pathlib import Path
from typing import Any, Optional

from agently.logging import LoggingMixin


class StateStorage(LoggingMixin):
    """Service for state storage using SQLite"""

    def __init__(self, db_path: Path) -> None:
        """Initialize state storage

        Args:
            db_path: Path to the database file
        """
        self.db_path = db_path
        self._ensure_db_exists()
        self.logger.info("State storage initialized", db_path=str(db_path))

    def _ensure_db_exists(self) -> None:
        """Ensure database file exists"""
        if not self.db_path.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.db_path.write_text("{}")
            self.logger.debug("Created new state database", db_path=str(self.db_path))

    def _load_state(self) -> dict[str, Any]:
        """Load state from database

        Returns:
            State dictionary
        """
        try:
            content = self.db_path.read_text()
            return json.loads(content)
        except Exception:
            self.logger.warning("Failed to load state, returning empty dict")
            return {}

    def _save_state(self, state: dict[str, Any]) -> None:
        """Save state to database

        Args:
            state: State dictionary to save
        """
        content = json.dumps(state, indent=2)
        self.db_path.write_text(content)

    def store(self, key: str, value: Any) -> None:
        """Store a key-value pair

        Args:
            key: Storage key
            value: Value to store
        """
        self.logger.debug("Storing state", key=key)
        state = self._load_state()
        state[key] = value
        self._save_state(state)

    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve a value by key

        Args:
            key: Storage key

        Returns:
            Value if exists, None otherwise
        """
        self.logger.debug("Retrieving state", key=key)
        state = self._load_state()
        return state.get(key)

    def delete(self, key: str) -> None:
        """Delete a key-value pair

        Args:
            key: Storage key to delete
        """
        self.logger.debug("Deleting state", key=key)
        state = self._load_state()
        if key in state:
            del state[key]
            self._save_state(state)

    def list_keys(self) -> list[str]:
        """List all stored keys

        Returns:
            List of keys
        """
        self.logger.debug("Listing all keys")
        state = self._load_state()
        return list(state.keys())

    def clear_all(self) -> None:
        """Clear all stored state"""
        self.logger.info("Clearing all state")
        self._save_state({})
