"""Tests for CLI main module"""

from click.testing import CliRunner

from agently.cli.main import cli


class TestCLI:
    """Test CLI commands"""

    def test_cli_group_exists(self):
        """Test that CLI group is available"""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Agently" in result.output

    def test_version_command(self):
        """Test version command"""
        runner = CliRunner()
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_ask_command(self):
        """Test ask command"""
        runner = CliRunner()
        result = runner.invoke(cli, ["ask", "test question"])
        assert result.exit_code == 0
        assert "Question: test question" in result.output

    def test_chat_command(self):
        """Test chat command"""
        runner = CliRunner()
        result = runner.invoke(cli, ["chat"])
        assert result.exit_code == 0
        assert "Interactive chat coming soon" in result.output
