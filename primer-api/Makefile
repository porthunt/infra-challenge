SHELL := /bin/bash

init:
	@pip install -r requirements-dev.txt -r requirements.txt

lint:
	flake8 app/ tests/
	black --line-length 79 --check app/ tests/

unit:
	pytest --disable-pytest-warnings tests/unit/

functional:
	pytest --disable-pytest-warnings tests/functional/

test: unit functional

run: lint test
