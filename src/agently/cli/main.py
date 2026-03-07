"""CLI main entry point"""

import sys

import click

from agently.config import get_settings
from agently.logging import configure_logging, get_logger


@click.group()
@click.version_option(version="0.1.0")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Agently - AI-driven programming assistant"""
    ctx.ensure_object(dict)


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
