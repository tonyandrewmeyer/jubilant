
.PHONE: help
help:
	@echo "Usage: make [target]\n\nTargets:"
	@awk -F: '/^[a-z]+:/ { print "   ", $$1 }' Makefile

.PHONY: fmt
fmt:
	uv run ruff format

.PHONY: lint
lint:
	uv run ruff check
	uv run ruff format --check

.PHONY: static
static:
	uv run pyright

.PHONY: unit
unit:
	uv run pytest
