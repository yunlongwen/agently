"""Interactive CLI shell for Agently"""

import sys
from typing import Optional

import click
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style

from agently.cli.logo import LogoRenderer
from agently.logging import get_logger

logger = get_logger(__name__)

# Custom style for the prompt
style = Style.from_dict(
    {
        "prompt": "#00aa00 bold",
        "command": "#00aaaa",
        "info": "#888888",
    }
)

# Available commands for auto-completion
COMMANDS = [
    "help",
    "exit",
    "quit",
    "agent",
    "agents",
    "clear",
    "version",
]


class InteractiveShell:
    """Interactive CLI shell for Agently"""

    def __init__(self) -> None:
        self.session: Optional[PromptSession] = None
        self.completer = WordCompleter(COMMANDS, ignore_case=True)
        self.kb = KeyBindings()
        self._setup_key_bindings()

    def _setup_key_bindings(self) -> None:
        """Setup custom key bindings"""

        @self.kb.add("c-c")
        def _(event):
            """Ctrl+C to exit"""
            event.app.exit()

        @self.kb.add("c-d")
        def _(event):
            """Ctrl+D to exit"""
            event.app.exit()

    def _get_prompt_message(self) -> list:
        """Get the prompt message with styling"""
        return [
            ("class:prompt", "🤖 "),
            ("class:command", "agently"),
            ("class:info", " > "),
        ]

    def _print_welcome(self) -> None:
        """Print welcome message"""
        logo_renderer = LogoRenderer()
        click.echo(logo_renderer.render())
        click.echo()
        click.echo("👋 Welcome to Agently Interactive Shell!")
        click.echo()
        click.echo("Available commands:")
        click.echo("  • Type your question or task to chat with AI")
        click.echo("  • 'help' - Show this help message")
        click.echo("  • 'agents' - List available agents")
        click.echo("  • 'clear' - Clear the screen")
        click.echo("  • 'version' - Show version information")
        click.echo("  • 'exit' or 'quit' - Exit the shell")
        click.echo()
        click.echo("💡 Tip: Just type naturally to start a conversation!")
        click.echo()

    def _print_help(self) -> None:
        """Print help message"""
        click.echo()
        click.echo("📖 Agently Interactive Shell Help")
        click.echo("=" * 50)
        click.echo()
        click.echo("You can:")
        click.echo("  1. Type any question or task to chat with AI")
        click.echo("  2. Use special commands:")
        click.echo()
        click.echo("Commands:")
        click.echo("  help       Show this help message")
        click.echo("  agents     List all available agents")
        click.echo("  clear      Clear the screen")
        click.echo("  version    Show version information")
        click.echo("  exit       Exit the interactive shell")
        click.echo("  quit       Same as exit")
        click.echo()
        click.echo("Keyboard shortcuts:")
        click.echo("  Ctrl+C     Exit the shell")
        click.echo("  Ctrl+D     Exit the shell")
        click.echo()

    def _list_agents(self) -> None:
        """List available agents"""
        click.echo()
        click.echo("🤖 Available Agents:")
        click.echo("=" * 30)
        click.echo("  • nexus          - Orchestrator agent (default)")
        click.echo("  • code-generator - Code generation specialist")
        click.echo("  • requirements   - Requirements analysis agent")
        click.echo("  • debugger       - Debugging assistant")
        click.echo("  • reviewer       - Code review specialist")
        click.echo()

    def _clear_screen(self) -> None:
        """Clear the screen"""
        click.clear()
        self._print_welcome()

    def _process_command(self, text: str) -> bool:
        """Process user input, return False to exit"""
        text = text.strip()

        if not text:
            return True

        # Handle special commands
        if text.lower() in ("exit", "quit"):
            click.echo("👋 Goodbye!")
            return False

        if text.lower() == "help":
            self._print_help()
            return True

        if text.lower() == "agents":
            self._list_agents()
            return True

        if text.lower() == "clear":
            self._clear_screen()
            return True

        if text.lower() == "version":
            from agently import __version__

            click.echo(f"Agently version: {__version__}")
            return True

        # Process as AI conversation
        self._process_ai_input(text)
        return True

    def _process_ai_input(self, text: str) -> None:
        """Process AI conversation input"""
        click.echo()
        click.echo("🤖 AI: ", nl=False)
        click.echo("I'm thinking... (AI integration coming soon!)")
        click.echo()
        click.echo(f"You asked: {text}")
        click.echo()
        click.echo("💡 To get real AI responses, please configure your OpenAI API key:")
        click.echo("   export OPENAI_API_KEY='your-api-key'")
        click.echo()

    def run(self) -> None:
        """Run the interactive shell"""
        try:
            # Create prompt session with history
            self.session = PromptSession(
                completer=self.completer,
                auto_suggest=AutoSuggestFromHistory(),
                key_bindings=self.kb,
                style=style,
            )

            # Print welcome message
            self._print_welcome()

            # Main loop
            while True:
                try:
                    # Get user input
                    text = self.session.prompt(
                        self._get_prompt_message(),
                        multiline=False,
                    )

                    # Process the input
                    if not self._process_command(text):
                        break

                except KeyboardInterrupt:
                    click.echo("\n👋 Goodbye!")
                    break
                except EOFError:
                    click.echo("\n👋 Goodbye!")
                    break

        except Exception as e:
            logger.error("Interactive shell error", error=str(e), exc_info=True)
            click.echo(f"❌ Error: {e}")
            sys.exit(1)


def start_interactive_shell() -> None:
    """Start the interactive shell"""
    shell = InteractiveShell()
    shell.run()
