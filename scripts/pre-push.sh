#!/bin/bash
# Pre-push hook - runs before pushing to remote
# This hook runs tests to catch issues before they reach CI

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

# Run tests (only if test files exist)
if python3 -m pytest --collect-only -q 2>&1 | grep -q "test session starts"; then
    echo "🧪 Running tests..."
    python3 -m pytest --no-cov -q || {
        echo "❌ Tests failed. Please fix failing tests."
        exit 1
    }
else
    echo "⚠️  No tests found, skipping..."
fi

echo "✅ All pre-push checks passed!"
exit 0
