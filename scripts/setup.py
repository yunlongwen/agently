#!/usr/bin/env python3
"""
Agently Setup Script

This script helps you set up Agently for the first time.
"""

import os
import sys
from pathlib import Path


def print_header(text: str) -> None:
    """Print formatted header"""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def print_step(step: int, text: str) -> None:
    """Print formatted step"""
    print(f"[{step}] {text}")


def confirm(prompt: str, default: bool = True) -> bool:
    """Ask for user confirmation"""
    suffix = " [Y/n]" if default else " [y/N]"
    while True:
        response = input(f"{prompt}{suffix}: ").strip().lower()
        if not response:
            return default
        if response in ("y", "yes"):
            return True
        if response in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'")


def main() -> int:
    """Main setup function"""
    print_header("Agently Setup")

    print("Welcome to Agently! This script will help you set up Agently.\n")

    # Step 1: Check Python version
    print_step(1, "Checking Python version...")
    if sys.version_info < (3, 9):
        print(f"  ❌ Python 3.9+ required, found {sys.version_info.major}.{sys.version_info.minor}")
        return 1
    print(f"  ✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")

    # Step 2: Check if installed
    print_step(2, "Checking installation...")
    try:
        import agently

        print(f"  ✅ Agently {agently.__version__} is installed")
    except ImportError:
        print("  ❌ Agently is not installed")
        print("  💡 Run: pip install agently")
        return 1

    # Step 3: Create config directory
    print_step(3, "Creating configuration directory...")
    config_dir = Path.home() / ".config" / "agently"
    config_dir.mkdir(parents=True, exist_ok=True)
    print(f"  ✅ Configuration directory: {config_dir}")

    # Step 4: Create cache directory
    print_step(4, "Creating cache directory...")
    cache_dir = Path.home() / ".cache" / "agently"
    cache_dir.mkdir(parents=True, exist_ok=True)
    print(f"  ✅ Cache directory: {cache_dir}")

    # Step 5: Setup API keys
    print_step(5, "Setting up API keys...")

    openai_key = os.getenv("OPENAI_API_KEY", "")
    if not openai_key:
        print("  💡 Set your OpenAI API key:")
        print("     export OPENAI_API_KEY='your_api_key'")
    else:
        print("  ✅ OpenAI API key is set")

    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not anthropic_key:
        print("  💡 Optionally, set your Anthropic API key:")
        print("     export ANTHROPIC_API_KEY='your_api_key'")
    else:
        print("  ✅ Anthropic API key is set")

    # Step 6: Test CLI
    print_step(6, "Testing CLI...")
    result = os.system("agently version > /dev/null 2>&1")
    if result == 0:
        print("  ✅ CLI is working correctly")
    else:
        print("  ❌ CLI test failed")
        print("  💡 Try running: agently version")

    # Step 7: Summary
    print_header("Setup Complete!")
    print("Agently is ready to use!")
    print("\nQuick start:")
    print("  agently chat        # Start interactive chat")
    print("  agently ask '...'   # Ask a question")
    print("\nDocumentation:")
    print("  https://yunlongwen.github.io/agently")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
