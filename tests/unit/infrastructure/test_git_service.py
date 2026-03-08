"""Tests for Git service"""

from pathlib import Path

from agently.infrastructure.git_service import GitService


class TestGitService:
    """Test GitService class"""

    def test_init_service(self, tmp_path: Path):
        """Test initializing a Git repository"""
        service = GitService()

        service.init_repository(tmp_path)

        # Assert .git directory exists
        git_dir = tmp_path / ".git"
        assert git_dir.exists()
        assert git_dir.is_dir()

    def test_get_current_branch(self, tmp_path: Path):
        """Test getting current branch name"""
        service = GitService()
        service.init_repository(tmp_path)

        branch = service.get_current_branch(tmp_path)
        assert branch == "master" or branch == "main"

    def test_add_file(self, tmp_path: Path):
        """Test adding a file to Git"""
        # Setup
        service = GitService()
        service.init_repository(tmp_path)

        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello")

        # Test
        service.add_file(tmp_path, test_file)

    def test_commit_changes(self, tmp_path: Path):
        """Test committing changes"""
        # Setup
        service = GitService()
        service.init_repository(tmp_path)

        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello")
        service.add_file(tmp_path, test_file)

        # Test
        service.commit_changes(tmp_path, "Initial commit")

    def test_get_status(self, tmp_path: Path):
        """Test getting repository status"""
        # Setup
        service = GitService()
        service.init_repository(tmp_path)

        # Test
        status = service.get_status(tmp_path)
        # Status should be a string
        assert isinstance(status, str)

    def test_is_repository_true(self, tmp_path: Path):
        """Test checking if directory is a repository (True)"""
        service = GitService()
        service.init_repository(tmp_path)

        assert service.is_repository(tmp_path) is True
