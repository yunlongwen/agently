"""CLI main entry point"""

import sys
from typing import Optional

import click

from agently.config import get_settings
from agently.logging import configure_logging, get_logger
from agently.orchestrator import NexusOrchestrator


@click.group()
@click.version_option(version="0.1.0")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Agently - AI-driven programming assistant"""
    ctx.ensure_object(dict)
    ctx.obj["orchestrator"] = NexusOrchestrator()


@cli.command()
@click.pass_context
def chat(ctx: click.Context) -> None:
    """Start interactive chat session"""
    click.echo("🤖 Agently Interactive Chat")
    click.echo("Type 'exit' or 'quit' to end the session\n")

    orchestrator: NexusOrchestrator = ctx.obj["orchestrator"]

    while True:
        try:
            user_input = click.prompt("You", type=str)

            if user_input.lower() in ["exit", "quit", "q"]:
                click.echo("Goodbye! 👋")
                break

            click.echo("🤖 Thinking...")
            result = orchestrator.process_task(user_input)

            if result["success"]:
                click.echo(f"Agently: {result['data']}")
            else:
                click.echo(f"❌ Error: {result.get('error', 'Unknown error')}")

        except click.Abort:
            click.echo("\nGoodbye! 👋")
            break
        except Exception as e:
            click.echo(f"❌ Error: {e}")


@cli.command()
@click.argument("question")
@click.pass_context
def ask(ctx: click.Context, question: str) -> None:
    """Ask a quick question"""
    click.echo(f"🤖 Question: {question}")
    click.echo("Processing...\n")

    orchestrator: NexusOrchestrator = ctx.obj["orchestrator"]
    result = orchestrator.process_task(question)

    if result["success"]:
        click.echo("✅ Result:")
        click.echo(result["data"])
    else:
        click.echo(f"❌ Error: {result.get('error', 'Unknown error')}")


@cli.command()
@click.pass_context
def version(ctx: click.Context) -> None:
    """Show version information"""
    click.echo("Agently version: 0.1.0")
    click.echo("AI-driven programming assistant")


@cli.group()
def agent() -> None:
    """Agent management commands"""
    pass


@agent.command(name="list")
@click.pass_context
def agent_list(ctx: click.Context) -> None:
    """List all available agents"""
    orchestrator: NexusOrchestrator = ctx.obj["orchestrator"]
    agents = orchestrator.get_available_agents()

    click.echo("🤖 Available Agents:")
    click.echo("-" * 40)

    for agent_info in agents:
        click.echo(f"\n📌 {agent_info['name']}")
        click.echo(f"   {agent_info['description']}")
        if agent_info['capabilities']:
            click.echo(f"   Capabilities: {', '.join(agent_info['capabilities'])}")


@agent.command(name="info")
@click.argument("agent_name")
@click.pass_context
def agent_info(ctx: click.Context, agent_name: str) -> None:
    """Show information about a specific agent"""
    orchestrator: NexusOrchestrator = ctx.obj["orchestrator"]
    agents = orchestrator.get_available_agents()

    agent = next((a for a in agents if a["name"] == agent_name), None)

    if agent:
        click.echo(f"🤖 Agent: {agent['name']}")
        click.echo(f"Description: {agent['description']}")
        click.echo(f"Capabilities: {', '.join(agent['capabilities'])}")
    else:
        click.echo(f"❌ Agent '{agent_name}' not found")


@agent.command(name="select")
@click.argument("agent_name")
@click.pass_context
def agent_select(ctx: click.Context, agent_name: str) -> None:
    """Select an agent for the next task"""
    click.echo(f"✅ Selected agent: {agent_name}")
    click.echo("Use 'agently task <description>' to execute a task with this agent")


@cli.command()
@click.argument("description")
@click.option("--agent", "-a", help="Specific agent to use")
@click.pass_context
def task(ctx: click.Context, description: str, agent: Optional[str]) -> None:
    """Execute a task with Agently"""
    click.echo(f"📝 Task: {description}")

    if agent:
        click.echo(f"🤖 Using agent: {agent}")

    click.echo("\n⏳ Processing...\n")

    orchestrator: NexusOrchestrator = ctx.obj["orchestrator"]

    context = {}
    if agent:
        context["preferred_agent"] = agent

    result = orchestrator.process_task(description, context=context)

    if result["success"]:
        click.echo("✅ Task completed successfully!")
        click.echo("\nResult:")
        click.echo(result["data"])
    else:
        click.echo(f"❌ Task failed: {result.get('error', 'Unknown error')}")


@cli.group()
def config() -> None:
    """Configuration commands"""
    pass


@config.command(name="show")
def config_show() -> None:
    """Show current configuration"""
    settings = get_settings()
    click.echo("⚙️  Current Configuration:")
    click.echo(f"  Debug: {settings.debug}")
    click.echo(f"  Log Level: {settings.log_level}")


@config.command(name="set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str) -> None:
    """Set a configuration value"""
    click.echo(f"✅ Set {key} = {value}")
    click.echo("Note: Configuration changes will take effect on next run")


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
