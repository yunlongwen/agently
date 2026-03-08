"""Tests for state storage service"""

from pathlib import Path

from agently.infrastructure.state_storage import StateStorage


class TestStateStorage:
    """Test StateStorage class"""

    def test_store_and_retrieve(self, tmp_path: Path):
        """Test storing and retrieving state"""
        db_path = tmp_path / "test.db"
        storage = StateStorage(db_path)

        # Store
        storage.store("test_key", {"value": 42})

        # Retrieve
        result = storage.retrieve("test_key")
        assert result == {"value": 42}

    def test_retrieve_nonexistent_key(self, tmp_path: Path):
        """Test retrieving nonexistent key"""
        db_path = tmp_path / "test.db"
        storage = StateStorage(db_path)

        result = storage.retrieve("nonexistent")
        assert result is None

    def test_delete_key(self, tmp_path: Path):
        """Test deleting a key"""
        db_path = tmp_path / "test.db"
        storage = StateStorage(db_path)

        # Store then delete
        storage.store("test_key", {"value": 42})
        storage.delete("test_key")

        # Verify deleted
        result = storage.retrieve("test_key")
        assert result is None

    def test_list_keys(self, tmp_path: Path):
        """Test listing all keys"""
        db_path = tmp_path / "test.db"
        storage = StateStorage(db_path)

        # Store multiple keys
        storage.store("key1", {"value": 1})
        storage.store("key2", {"value": 2})
        storage.store("key3", {"value": 3})

        # List keys
        keys = storage.list_keys()
        assert set(keys) == {"key1", "key2", "key3"}

    def test_clear_all(self, tmp_path: Path):
        """Test clearing all state"""
        db_path = tmp_path / "test.db"
        storage = StateStorage(db_path)

        # Store data
        storage.store("key1", {"value": 1})
        storage.store("key2", {"value": 2})

        # Clear all
        storage.clear_all()

        # Verify cleared
        keys = storage.list_keys()
        assert len(keys) == 0
