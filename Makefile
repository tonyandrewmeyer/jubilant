
.PHONE: help
help:
	@echo "Usage: make [target]\n\nTargets:"
	@awk -F: '/^[a-z]+:/ { print "   ", $$1 }' Makefile

.PHONY: fmt
fmt:
	uvx ruff@0.8.1 format

.PHONY: lint
lint:
	uvx ruff@0.8.1 check
	uvx ruff@0.8.1 format --check

.PHONY: static
static:
	uvx pyright@1.1.389

.PHONY: unit
unit:
	uvx pytest@8.3.4
