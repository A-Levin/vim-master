.PHONY: help install dev test test-unit test-integration lint format check clean run

help:
	@echo "Available commands:"
	@echo "  install         - Install production dependencies"
	@echo "  dev             - Install development dependencies"
	@echo "  test            - Run all tests"
	@echo "  test-unit       - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  lint            - Run linter checks"
	@echo "  format          - Format code"
	@echo "  check           - Run all checks (lint, format, type)"
	@echo "  clean           - Clean cache and temporary files"
	@echo "  run             - Run the application"

install:
	uv sync --no-dev

dev:
	uv sync --dev
	uv run pre-commit install

test:
	uv run pytest

test-unit:
	uv run pytest app/tests/unit/ -v

test-integration:
	uv run pytest app/tests/integration/ -v

lint:
	uv run ruff check .

format:
	uv run ruff format .

check: lint
	uv run ruff format --check .
	uv run mypy app/

clean:
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name ".mypy_cache" -delete
	find . -type d -name ".ruff_cache" -delete

run:
	uv run python app/main.py
