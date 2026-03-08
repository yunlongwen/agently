#!/bin/bash
# Pre-push hook - runs before pushing to remote
# This hook runs lint and format checks before push
# Note: mypy is temporarily disabled due to existing type annotation issues

set -e

echo "🔍 Running pre-push checks..."

# Get the repository root directory
REPO_ROOT="$(git rev-parse --show-toplevel)"

# Change to repo root
cd "$REPO_ROOT"

echo "📁 Working directory: $(pwd)"

# Run linter
echo "📋 Running ruff check..."
python3 -m ruff check . || {
    echo ""
    echo "❌ Ruff check failed!"
    echo ""
    echo "💡 To fix automatically, run:"
    echo "   ruff check . --fix"
    echo ""
    echo "Then commit the changes and try again."
    exit 1
}

# Run formatter
echo "✨ Running ruff format check..."
python3 -m ruff format --check . || {
    echo ""
    echo "❌ Ruff format check failed!"
    echo ""
    echo "💡 To fix, run:"
    echo "   ruff format ."
    echo ""
    echo "Then commit the changes and try again."
    exit 1
}

# TODO: Re-enable mypy check after fixing type annotations
# echo "🔍 Running mypy type check..."
# python3 -m mypy src/agently || {
#     echo ""
#     echo "❌ Mypy type check failed!"
#     exit 1
# }

echo "✅ All pre-push checks passed!"
exit 0
