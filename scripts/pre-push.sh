#!/bin/bash
# Pre-push hook - runs before pushing to remote
# This hook runs lint and format checks before push

set -e

echo "🔍 Running pre-push checks..."

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to repo root
cd "$REPO_ROOT"

# Run linter using python -m to ensure it works in virtual environments
echo "📋 Running ruff..."
python3 -m ruff check . --fix || {
    echo "❌ Ruff check failed. Please fix linting errors."
    exit 1
}

# Run formatter
echo "✨ Running ruff format..."
python3 -m ruff format . || {
    echo "❌ Ruff format failed. Please fix formatting."
    exit 1
}

echo "✅ All pre-push checks passed!"
echo ""
echo "💡 Tip: Run 'pytest' locally before pushing to catch test failures."
exit 0
