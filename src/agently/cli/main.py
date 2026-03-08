"""CLI main entry point"""

import sys

import click

from agently.cli.logo import LogoRenderer
from agently.config import get_settings
from agently.logging import configure_logging, get_logger


@click.group(invoke_without_command=True)
@click.version_option(version="0.1.0")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Agently - AI-driven programming assistant"""
    ctx.ensure_object(dict)

    # 只在不带子命令时显示 logo
    if ctx.invoked_subcommand is None:
        logo_renderer = LogoRenderer()
        click.echo(logo_renderer.render())
        click.echo(ctx.get_help())


@cli.command()
@click.pass_context
def chat(ctx: click.Context) -> None:
    """Start interactive chat session"""
    click.echo("Interactive chat coming soon!")


@cli.command()
@click.argument("question")
@click.pass_context
def ask(ctx: click.Context, question: str) -> None:
    """Ask a quick question"""
    click.echo(f"Question: {question}")
    click.echo("AI processing coming soon!")


@cli.command()
@click.pass_context
def version(ctx: click.Context) -> None:
    """Show version information"""
    click.echo("Agently version: 0.1.0")


@cli.group()
@click.pass_context
def agent(ctx: click.Context) -> None:
    """Agent management commands"""
    pass


@agent.command()
@click.pass_context
def list(ctx: click.Context) -> None:
    """List all available agents"""
    click.echo("Available agents:")
    click.echo("  - nexus: Orchestrator agent")
    click.echo("  - code-generator: Code generation agent")
    click.echo("  - requirements-analyzer: Requirements analysis agent")


@agent.command()
@click.argument("name")
@click.pass_context
def info(ctx: click.Context, name: str) -> None:
    """Show agent information"""
    click.echo(f"Agent: {name}")
    click.echo(f"Description: Agent {name} information")


@agent.command()
@click.argument("name")
@click.pass_context
def select(ctx: click.Context, name: str) -> None:
    """Select an agent for interaction"""
    click.echo(f"Selected agent: {name}")


@cli.group()
@click.pass_context
def config(ctx: click.Context) -> None:
    """Configuration management commands"""
    pass


@config.command()
@click.pass_context
def show(ctx: click.Context) -> None:
    """Show current configuration"""
    settings = get_settings()
    click.echo("Current configuration:")
    click.echo(f"  Model: {settings.openai_model}")
    click.echo(f"  Log level: {settings.log_level}")


@config.command()
@click.argument("key")
@click.argument("value")
@click.pass_context
def set(ctx: click.Context, key: str, value: str) -> None:
    """Set configuration value"""
    click.echo(f"Set {key} = {value}")


@cli.group()
@click.pass_context
def task(ctx: click.Context) -> None:
    """Task management commands"""
    pass


@task.command()
@click.argument("description")
@click.pass_context
def execute(ctx: click.Context, description: str) -> None:
    """Execute a task"""
    click.echo(f"Executing task: {description}")


def main() -> None:
    """Main CLI entry point"""
    settings = get_settings()
    configure_logging(settings)
    logger = get_logger(__name__)

    logger.info("Agently starting", version="0.1.0")

    try:
        cli()
    except Exception as e:
        logger.error("CLI error", error=str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
