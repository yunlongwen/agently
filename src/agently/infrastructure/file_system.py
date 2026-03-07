"""File system service for file and directory operations"""

from pathlib import Path

from agently.logging import LoggingMixin


class FileSystemService(LoggingMixin):
    """Service for file system operations"""

    def read_file(self, file_path: Path) -> str:
        """Read content from a file

        Args:
            file_path: Path to the file

        Returns:
            File content as string

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        self.logger.info("Reading file", file_path=str(file_path))
        return file_path.read_text()

    def write_file(self, file_path: Path, content: str) -> None:
        """Write content to a file

        Args:
            file_path: Path to the file
            content: Content to write
        """
        self.logger.info("Writing file", file_path=str(file_path))
        file_path.write_text(content)

    def append_file(self, file_path: Path, content: str) -> None:
        """Append content to a file

        Args:
            file_path: Path to the file
            content: Content to append
        """
        self.logger.info("Appending to file", file_path=str(file_path))
        with file_path.open("a") as f:
            f.write(content)

    def delete_file(self, file_path: Path) -> None:
        """Delete a file

        Args:
            file_path: Path to the file

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        self.logger.info("Deleting file", file_path=str(file_path))
        file_path.unlink()

    def file_exists(self, file_path: Path) -> bool:
        """Check if a file exists

        Args:
            file_path: Path to check

        Returns:
            True if file exists, False otherwise
        """
        return file_path.exists()

    def list_directory(self, dir_path: Path) -> list[Path]:
        """List files in a directory

        Args:
            dir_path: Path to the directory

        Returns:
            List of file paths

        Raises:
            FileNotFoundError: If directory doesn't exist
        """
        self.logger.info("Listing directory", dir_path=str(dir_path))
        return [f for f in dir_path.iterdir() if f.is_file()]

    def create_directory(self, dir_path: Path) -> None:
        """Create a directory

        Args:
            dir_path: Path to the directory
        """
        self.logger.info("Creating directory", dir_path=str(dir_path))
        dir_path.mkdir(parents=True, exist_ok=True)
