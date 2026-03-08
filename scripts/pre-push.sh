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

# Run linter - DON'T use --fix, fail if there are issues
echo "📋 Running ruff..."
python3 -m ruff check . || {
    echo ""
    echo "❌ Ruff check failed!"
    echo ""
    echo "💡 To fix automatically, run:"
    echo "   ruff check . --fix"
    echo "   ruff format ."
    echo ""
    echo "Then commit the changes and try again."
    exit 1
}

# Run formatter - check mode, don't modify
echo "✨ Running ruff format check..."
python3 -m ruff format --check . || {
    echo ""
    echo "❌ Ruff format check failed!"
    echo ""
    echo "💡 To fix automatically, run:"
    echo "   ruff format ."
    echo ""
    echo "Then commit the changes and try again."
    exit 1
}

echo "✅ All pre-push checks passed!"
exit 0
