.PHONY: setup build deploy test

# Configuration variables
STACK_NAME ?= lambda-starter-template
ENVIRONMENT ?= dev
EVENT ?= events/event.json
AWS_REGION ?= us-east-1

# Python specific
PYTHON := python3
PIP := pip3
VENV := venv
VENV_ACTIVATE := . $(VENV)/bin/activate

# Setup development environment
setup:
	@echo "Setting up development environment..."
	$(PYTHON) -m venv $(VENV)
	$(VENV_ACTIVATE) && $(PIP) install --upgrade pip
	$(VENV_ACTIVATE) && $(PIP) install -r requirements.txt
	@echo "✅ Development environment set up successfully"

# Build SAM application
build:
	@echo "Building SAM application..."
	sam build

# Deploy SAM application
deploy: build
	@echo "Deploying SAM application to $(ENVIRONMENT) environment..."
	sam deploy --guided

# Test SAM application
test:
	@echo "Testing SAM application..."
	python -m pytest