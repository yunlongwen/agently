"""Git service for Git operations"""

from pathlib import Path

from agently.logging import LoggingMixin


class GitService(LoggingMixin):
    """Service for Git operations"""

    def init_repository(self, repo_path: Path) -> None:
        """Initialize a Git repository

        Args:
            repo_path: Path to the repository
        """
        try:
            from git import Repo

            self.logger.info("Initializing Git repository", repo_path=str(repo_path))
            Repo.init(repo_path)
        except ImportError as e:
            self.logger.error("GitPython not installed")
            raise ImportError("GitPython is required. Install with: pip install GitPython") from e

    def get_current_branch(self, repo_path: Path) -> str:
        """Get current branch name

        Args:
            repo_path: Path to the repository

        Returns:
            Branch name
        """
        from git import Repo

        self.logger.debug("Getting current branch", repo_path=str(repo_path))
        repo = Repo(repo_path)
        return repo.active_branch.name

    def add_file(self, repo_path: Path, file_path: Path) -> None:
        """Add a file to Git

        Args:
            repo_path: Path to the repository
            file_path: Path to the file
        """
        from git import Repo

        self.logger.info("Adding file to Git", file_path=str(file_path))
        repo = Repo(repo_path)
        repo.index.add([str(file_path)])

    def commit_changes(self, repo_path: Path, message: str) -> None:
        """Commit changes

        Args:
            repo_path: Path to the repository
            message: Commit message
        """
        from git import Repo

        self.logger.info("Committing changes", message=message)
        repo = Repo(repo_path)
        repo.index.commit(message)

    def get_status(self, repo_path: Path) -> str:
        """Get repository status

        Args:
            repo_path: Path to the repository

        Returns:
            Status string
        """
        from git import Repo

        self.logger.debug("Getting repository status", repo_path=str(repo_path))
        repo = Repo(repo_path)
        return str(repo.git.status())

    def is_repository(self, repo_path: Path) -> bool:
        """Check if directory is a Git repository

        Args:
            repo_path: Path to check

        Returns:
            True if it's a repository, False otherwise
        """
        try:
            from git import Repo

            Repo(repo_path)
            return True
        except Exception:
            return False
