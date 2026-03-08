"""Tests for CLI"""

from agently.cli.main import cli
from click.testing import CliRunner


class TestCLI:
    """Test CLI commands"""

    def test_cli_version(self):
        """Test CLI version command"""
        runner = CliRunner()
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_cli_ask(self):
        """Test CLI ask command"""
        runner = CliRunner()
        result = runner.invoke(cli, ["ask", "What is Python?"])
        assert result.exit_code == 0
        assert "What is Python?" in result.output

    def test_cli_chat(self):
        """Test CLI chat command"""
        runner = CliRunner()
        result = runner.invoke(cli, ["chat"])
        assert result.exit_code == 0

    def test_cli_agent_list(self):
        """Test CLI agent list command"""
        runner = CliRunner()
        result = runner.invoke(cli, ["agent", "list"])
        assert result.exit_code == 0

    def test_cli_agent_info(self):
        """Test CLI agent info command"""
        runner = CliRunner()
        result = runner.invoke(cli, ["agent", "info", "nexus"])
        assert result.exit_code == 0

    def test_cli_agent_select(self):
        """Test CLI agent select command"""
        runner = CliRunner()
        result = runner.invoke(cli, ["agent", "select", "code-generator"])
        assert result.exit_code == 0

    def test_cli_config_show(self):
        """Test CLI config show command"""
        runner = CliRunner()
        result = runner.invoke(cli, ["config", "show"])
        assert result.exit_code == 0

    def test_cli_config_set(self):
        """Test CLI config set command"""
        runner = CliRunner()
        result = runner.invoke(cli, ["config", "set", "model", "openai"])
        assert result.exit_code == 0

    def test_cli_task_execute(self):
        """Test CLI task execute command"""
        runner = CliRunner()
        result = runner.invoke(cli, ["task", "execute", "generate a function"])
        assert result.exit_code == 0
        result = runner.invoke(cli, ["task", "generate a function"])
