.PHONY: help install install-dev test lint format type-check clean build docs docs-serve docs-run run pre-commit-install pre-commit-run

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
install: ## Install package
	pip install -e .

install-dev: ## Install package with development dependencies
	pip install -e ".[dev]"

test: ## Run tests
	pytest -v

test-cov: ## Run tests with coverage
	pytest --cov=agently --cov-report=html --cov-report=term-missing

lint: ## Run linter (ruff)
	ruff check .

lint-fix: ## Auto-fix linting issues
	ruff check . --fix

format: ## Format code with ruff
	ruff format .

format-check: ## Check code formatting
	ruff format --check .

type-check: ## Run type checker (mypy)
	mypy src/

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: ## Build package
	python -m build

docs-serve: ## Serve documentation locally
	mkdocs serve

docs-build: ## Build documentation
	mkdocs build

run: ## Run Agently CLI
	python -m agently.cli

check: pre-commit-run ## Run all git hooks before commit

pre-commit-install: ## Install pre-commit hooks
	pre-commit install

pre-commit-run: ## Run pre-commit hooks manually
	pre-commit run --all-files
