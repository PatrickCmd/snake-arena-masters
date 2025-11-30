# Backend Makefile

.PHONY: help install run test test-cov test-integration test-all clean setup lint format format-check seed-info verify-api db-migrate db-seed db-reset

# Default target - show help
help:
	@echo "Snake Arena Masters - Backend Makefile"
	@echo ""
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make run           - Run development server"
	@echo "  make test          - Run unit tests"
	@echo "  make test-cov      - Run tests with coverage"
	@echo "  make test-integration - Run integration tests"
	@echo "  make test-all      - Run all tests (unit + integration)"
	@echo "  make lint          - Run linting (ruff check)"
	@echo "  make format        - Format code (ruff format)"
	@echo "  make format-check  - Check formatting without changes"
	@echo "  make seed-info     - Display mock database info"
	@echo "  make verify-api    - Verify API endpoints (requires running server)"
	@echo "  make db-migrate    - Run database migrations"
	@echo "  make db-seed       - Seed database with demo data"
	@echo "  make db-reset      - Reset database (drop and recreate)"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make setup         - Full setup (install + check)"

# Install dependencies
install:
	uv sync --dev

# Run the development server
run:
	uv run uvicorn app.main:app --reload

# Run tests
test:
	uv run pytest -v

# Run tests with coverage
test-cov:
	uv run pytest --cov=app tests/

# Run integration tests
test-integration:
	uv run pytest tests_integration/ -v

# Run all tests (unit + integration)
test-all:
	uv run pytest tests/ tests_integration/ -v

# Clean up build artifacts and cache
clean:
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Full setup
setup: install
	@echo "Setup complete. Run 'make run' to start the server."

# Linting with ruff
lint:
	uv run ruff check app/ tests/ scripts/

# Format code with ruff
format:
	uv run ruff format app/ tests/ scripts/

# Check formatting without making changes
format-check:
	uv run ruff format --check app/ tests/ scripts/

# Display mock database information
seed-info:
	uv run python scripts/seed_info.py

# Verify API endpoints (requires running server)
verify-api:
	uv run python scripts/verify_api.py

# Database commands
db-migrate:
	uv run alembic upgrade head

db-seed:
	uv run python scripts/seed_db.py

db-reset:
	rm -f snake_arena.db
	uv run alembic upgrade head
	uv run python scripts/seed_db.py
