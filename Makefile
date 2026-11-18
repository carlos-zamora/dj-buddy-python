# Developer commands for dj-buddy-python (Linux, macOS and CI).
# On Windows without make, run scripts/check.ps1 instead; it runs the same steps as `make check`.
# Every command goes through `uv run`, so it uses the project's locked environment.

.PHONY: help install lint format typecheck test cov check clean

# Show the available targets.
help:
	@echo "make install    - create .venv and install locked dependencies"
	@echo "make lint       - ruff lint and format check (no changes)"
	@echo "make format     - apply ruff fixes and formatting"
	@echo "make typecheck  - mypy"
	@echo "make test       - pytest"
	@echo "make cov        - pytest with a coverage report"
	@echo "make check      - lint + typecheck + test (what CI runs)"
	@echo "make clean      - remove caches and build output"

# Create the virtual environment from uv.lock. --locked fails if uv.lock is out of date.
install:
	uv sync --locked

# Lint and check formatting without modifying files.
lint:
	uv run ruff check .
	uv run ruff format --check .

# Apply safe lint fixes and reformat the code.
format:
	uv run ruff check --fix .
	uv run ruff format .

# Type-check the package (strict on djbuddy.core and djbuddy.recommend).
typecheck:
	uv run mypy

# Run the test suite.
test:
	uv run pytest

# Run the test suite with a line and branch coverage report.
cov:
	uv run pytest --cov --cov-report=term-missing

# The gate every change must pass: lint, types, tests.
check: lint typecheck test

# Remove caches and build artifacts.
clean:
	rm -rf .mypy_cache .pytest_cache .ruff_cache .coverage htmlcov build dist
	find . -type d -name __pycache__ -not -path "./.venv/*" -exec rm -rf {} +
