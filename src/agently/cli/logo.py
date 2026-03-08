"""CLI Logo rendering module

This module provides the LogoRenderer class for generating
ASCII art logos with dynamic version information.
"""

from typing import Optional

from agently import __version__


class LogoRenderer:
    """Renders the Agently CLI logo with dynamic version information.

    This class follows the UI component pattern, separating the logo
    rendering logic from the CLI command handling.

    Attributes:
        version: The version string to display in the logo.
                Defaults to the package version.

    Example:
        >>> renderer = LogoRenderer()
        >>> print(renderer.render())
        >>> # Or with custom version
        >>> renderer = LogoRenderer(version="2.0.0")
        >>> print(renderer.render())
    """

    # ASCII art template using box-drawing characters
    # Each letter is composed of Unicode block elements
    _LOGO_TEMPLATE = """
    ▄▀█ █▀▀ █▀▀ █▄░█ ▀█▀ █░░ █▄█
    █▀█ █▄█ ██▄ █░▀█ ░█░ █▄▄ ░█░

    🤖 Agently v{version} | AI-Driven Programming Assistant
    ────────────────────────────────────────────────────
    Tips: Run 'agently --help' to see available commands
"""

    def __init__(self, version: Optional[str] = None) -> None:
        """Initialize the LogoRenderer.

        Args:
            version: Optional version string. If not provided,
                    uses the package's __version__.
        """
        self.version = version if version is not None else __version__

    def render(self) -> str:
        """Render the logo with the configured version.

        Returns:
            The rendered logo string with version information.
        """
        return self._LOGO_TEMPLATE.format(version=self.version)

    def __str__(self) -> str:
        """Allow direct string conversion of the renderer."""
        return self.render()
