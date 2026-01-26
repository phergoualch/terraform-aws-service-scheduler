.PHONY: help lint lint-unsafe format check test clean pre-commit install-hooks fix ci

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

lint: ## Run Ruff linter with safe auto-fixes only
	@echo "Running Ruff linter with safe fixes..."
	@uvx ruff check lambda/src --fix || true
	@echo "✓ Linting complete (some issues may require manual fixes)"

lint-unsafe: ## Run Ruff linter with unsafe auto-fixes (use with caution)
	@echo "Running Ruff linter with unsafe fixes..."
	@uvx ruff check lambda/src --fix --unsafe-fixes || true
	@echo "✓ Linting complete with unsafe fixes"

format: ## Run Ruff formatter
	@echo "Running Ruff formatter..."
	@uvx ruff format lambda/src
	@echo "✓ Formatting complete"

check: ## Run Ruff linter without auto-fix (CI mode)
	@echo "Running Ruff checks (no auto-fix)..."
	uvx ruff check lambda/src
	uvx ruff format lambda/src --check

test: ## Run pytest tests
	@echo "Running tests..."
	@cd lambda/src && python -m pytest tests/ -v

clean: ## Remove Python cache files and build artifacts
	@echo "Cleaning cache files and build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf lambda/lambda.zip 2>/dev/null || true
	@echo "✓ Cleanup complete"

pre-commit: ## Run all pre-commit hooks on all files
	@echo "Running pre-commit hooks..."
	@pre-commit run --all-files || true

install-hooks: ## Install pre-commit hooks
	@echo "Installing pre-commit hooks..."
	@pre-commit install
	@echo "✓ Pre-commit hooks installed"

# Combined targets
fix: lint format ## Run linter and formatter (full fix)
	@echo "✓ All fixes applied"

ci: check test ## Run all CI checks (linting + tests)
