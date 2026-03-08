#!/bin/bash
# Pre-push hook - runs before pushing to remote
# This hook runs tests to catch issues before they reach CI

set -e

echo "🔍 Running pre-push checks..."

# Run linter
echo "📋 Running ruff..."
ruff check . --fix || {
    echo "❌ Ruff check failed. Please fix linting errors."
    exit 1
}

# Run formatter
echo "✨ Running ruff format..."
ruff format . || {
    echo "❌ Ruff format failed. Please fix formatting."
    exit 1
}

# Run tests
echo "🧪 Running tests..."
pytest --no-cov -q || {
    echo "❌ Tests failed. Please fix failing tests."
    exit 1
}

echo "✅ All pre-push checks passed!"
exit 0
