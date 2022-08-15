SHELL := /bin/bash
.DEFAULT_GOAL := help
.PHONY: coverage deps help lint push test shell
TF_VERSION = "v1.0.8"

coverage:  ## Run tests with coverage
	coverage erase
	coverage run --include=auto_infra/* -m pytest -ra
	coverage report -m

deps:  ## Install dependencies
	poetry install	

disable-venv: ## In buildkite disable virtualenv in Poetry
	poetry config virtualenvs.create false

lint:  ## Lint and Python Black formatting check
	poetry install
	flake8 auto_infra tests
	black --check auto_infra tests

push:  ## Push code with tags
	git push && git push --tags

test:  ## Run tests
	@echo "Checking for terraform version ${TF_VERSION}" 
	terraform version | grep "Terraform ${TF_VERSION}"
	pytest -ra

shell: ## Poetry venv shell
	poetry shell

build: ## Run poetry build
	poetry build
