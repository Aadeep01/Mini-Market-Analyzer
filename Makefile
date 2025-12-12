.PHONY: install test test-integration lint format type-check check run clean help

# Default target
.DEFAULT_GOAL := help

install: ## Install dependencies using uv
	uv sync

test: ## Run unit tests
	uv run pytest tests/test_data_loader.py tests/test_indicators.py tests/test_strategy.py

test-integration: ## Run integration tests with real data
	uv run pytest tests/test_integration_real.py -v -s

lint: ## Run ruff for linting
	uv run ruff check .

format: ## Run ruff for formatting
	uv run ruff format .

type-check: ## Run mypy for static type checking
	uv run mypy .

check: lint type-check test ## Run all quality checks (lint, type-check, unit tests)

run: ## Run the interactive CLI session
	uv run python -m mini_market_analyzer.main interactive

analyze: ## Run a single analysis (usage: make analyze args="AAPL")
	uv run python -m mini_market_analyzer.main analyze $(args)

clean: ## Clean up cache files
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
