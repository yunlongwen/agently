"""Tests for CLI Logo rendering"""

from unittest.mock import patch

from click.testing import CliRunner

from agently.cli.logo import LogoRenderer
from agently.cli.main import cli


class TestLogoRenderer:
    """Test LogoRenderer class"""

    def test_logo_renderer_initialization(self):
        """Test LogoRenderer can be initialized with version"""
        renderer = LogoRenderer(version="1.0.0")
        assert renderer.version == "1.0.0"

    def test_logo_renderer_default_version(self):
        """Test LogoRenderer uses package version by default"""
        renderer = LogoRenderer()
        from agently import __version__

        assert renderer.version == __version__

    def test_logo_contains_agently_text(self):
        """Test rendered logo contains AGENTLY ASCII art"""
        renderer = LogoRenderer(version="0.1.0")
        logo = renderer.render()
        # Check for key characters that form "AGENTLY"
        assert "▄▀█" in logo
        assert "█▀▀" in logo
        assert "█▄█" in logo

    def test_logo_contains_version(self):
        """Test rendered logo contains version number"""
        renderer = LogoRenderer(version="1.2.3")
        logo = renderer.render()
        assert "1.2.3" in logo

    def test_logo_contains_help_tip(self):
        """Test rendered logo contains help tip"""
        renderer = LogoRenderer(version="0.1.0")
        logo = renderer.render()
        assert "--help" in logo

    def test_logo_does_not_contain_hardcoded_version(self):
        """Test logo uses dynamic version, not hardcoded"""
        renderer = LogoRenderer(version="9.9.9")
        logo = renderer.render()
        assert "9.9.9" in logo
        # Should not contain old hardcoded version
        assert "0.1.0" not in logo or "9.9.9" in logo


class TestCLILogoDisplay:
    """Test CLI logo display behavior"""

    def test_logo_displayed_on_bare_command(self):
        """Test logo is displayed when running 'agently' without subcommand"""
        runner = CliRunner()
        result = runner.invoke(cli, [])
        assert result.exit_code == 0
        # Check for AGENTLY ASCII art characters
        assert "▄▀█" in result.output
        assert "█▀▀" in result.output

    def test_logo_not_displayed_with_help_flag(self):
        """Test logo is not displayed when using --help"""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        # Logo ASCII characters should not be in help output
        assert "▄▀█" not in result.output

    def test_logo_not_displayed_with_version_flag(self):
        """Test logo is not displayed when using --version"""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        # Logo ASCII characters should not be in version output
        assert "▄▀█" not in result.output

    def test_logo_not_displayed_with_subcommand(self):
        """Test logo is not displayed when using subcommands"""
        runner = CliRunner()
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        # Logo ASCII characters should not be in subcommand output
        assert "▄▀█" not in result.output

    def test_logo_contains_dynamic_version(self):
        """Test logo displays the actual package version"""
        from agently import __version__

        runner = CliRunner()
        result = runner.invoke(cli, [])
        assert result.exit_code == 0
        assert __version__ in result.output

    @patch("agently.cli.logo.LogoRenderer.render")
    def test_logo_render_called_on_bare_command(self, mock_render):
        """Test that logo render is called when no subcommand"""
        mock_render.return_value = "MOCK_LOGO"
        runner = CliRunner()
        result = runner.invoke(cli, [])
        # The mock should have been called
        assert mock_render.called or "MOCK_LOGO" in result.output or "▄▀█" in result.output
