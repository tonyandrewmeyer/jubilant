
.PHONY: help
help:
	@echo "Usage: make [target] [ARGS='additional args']\n\nTargets:"
	@awk -F: '/^[a-z-]+:/ { print "   ", $$1 }' Makefile

# Run all quick, local commands
.PHONY: all
all: format lint static unit

# Build documentation
.PHONY: docs
docs:
	$(MAKE) -C docs run

# Fix linting issues
.PHONY: fix
fix:
	uv run ruff check --fix

# Format the Python code
.PHONY: format
format:
	uv run ruff format

# Run integration tests (slow, require real Juju)
.PHONY: integration
integration:
	uv run pytest tests/integration -vv --log-level=INFO --log-format="%(asctime)s %(levelname)s %(message)s" $(ARGS)

# Perform linting
.PHONY: lint
lint:
	uv run ruff check
	uv run ruff format --diff

# Pack charms used by integration tests (requires charmcraft)
.PHONY: pack
pack:
	cd tests/integration/charms/testdb && charmcraft pack
	cd tests/integration/charms/testapp && charmcraft pack

# Publish to TestPyPI
.PHONY:
publish-test:
	rm -rf dist
	uv build
	uv publish --publish-url=https://test.pypi.org/legacy/ --token=$(UV_PUBLISH_TOKEN_TEST)

# Check static types
.PHONY: static
static:
	uv run pyright

# Run quick unit tests
.PHONY: unit
unit:
	uv run pytest tests/unit -vv --cov=jubilant $(ARGS)
