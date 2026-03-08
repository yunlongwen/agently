"""Tests for file system service"""

from pathlib import Path

import pytest

from agently.infrastructure.file_system import FileSystemService


class TestFileSystemService:
    """Test FileSystemService class"""

    def test_read_file_success(self, tmp_path: Path):
        """Test reading a file successfully"""
        # Setup
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!")

        # Test
        service = FileSystemService()
        content = service.read_file(test_file)

        # Assert
        assert content == "Hello, World!"

    def test_read_file_not_found(self, tmp_path: Path):
        """Test reading a file that doesn't exist"""
        test_file = tmp_path / "nonexistent.txt"

        service = FileSystemService()
        with pytest.raises(FileNotFoundError):
            service.read_file(test_file)

    def test_write_file_success(self, tmp_path: Path):
        """Test writing a file successfully"""
        test_file = tmp_path / "test.txt"

        service = FileSystemService()
        service.write_file(test_file, "Hello, World!")

        # Assert
        assert test_file.read_text() == "Hello, World!"

    def test_append_file_success(self, tmp_path: Path):
        """Test appending to a file"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello")

        service = FileSystemService()
        service.append_file(test_file, ", World!")

        # Assert
        assert test_file.read_text() == "Hello, World!"

    def test_delete_file_success(self, tmp_path: Path):
        """Test deleting a file"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello")

        service = FileSystemService()
        service.delete_file(test_file)

        # Assert
        assert not test_file.exists()

    def test_file_exists_true(self, tmp_path: Path):
        """Test checking if file exists (True)"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello")

        service = FileSystemService()
        assert service.file_exists(test_file) is True

    def test_file_exists_false(self, tmp_path: Path):
        """Test checking if file exists (False)"""
        test_file = tmp_path / "nonexistent.txt"

        service = FileSystemService()
        assert service.file_exists(test_file) is False

    def test_list_directory(self, tmp_path: Path):
        """Test listing directory contents"""
        # Setup
        (tmp_path / "file1.txt").write_text("File 1")
        (tmp_path / "file2.txt").write_text("File 2")
        (tmp_path / "subdir").mkdir()

        service = FileSystemService()
        files = service.list_directory(tmp_path)

        # Assert
        assert len(files) == 2
        assert any(f.name == "file1.txt" for f in files)
        assert any(f.name == "file2.txt" for f in files)

    def test_create_directory(self, tmp_path: Path):
        """Test creating a directory"""
        new_dir = tmp_path / "new_dir"

        service = FileSystemService()
        service.create_directory(new_dir)

        # Assert
        assert new_dir.exists()
        assert new_dir.is_dir()
