.PHONY: *

greetings:
	@echo "Welcome! Select a proper target."

update_packages:
	sudo apt update -y && sudo apt upgrade -y
	python3 -m pip install --upgrade pip -v && \
        python3 -m pip install --upgrade setuptools wheel -v

install_p310: update_packages
	python3 -m pip install -r resources/requirements.txt -v --extra-index-url https://download.pytorch.org/whl/cu124
	python3 -m pip freeze

install_p311: update_packages
	python3 -m pip install -r resources/requirements.txt -v --extra-index-url https://download.pytorch.org/whl/cu124
	python3 -m pip freeze

format_check:
	python3 -m black --line-length=100 --check -t py310 -t py311 --required-version 24 .

format:
	python3 -m black --line-length=100 -t py310 -t py311 --required-version 24 .

lint:
	@echo "Checking code with Mypy."
	python3 -m mypy --config-file=resources/configs/mypy.ini .
	@echo "Checking code with Pyflakes."
	python3 -m pyflakes .
	@echo "Checking code with Pylint."
	python3 -m pylint --rcfile=resources/configs/.pylintrc --disable=C .

test:
	python3 -m pytest -vv --durations=15 --cov-config=resources/configs/.coveragerc --cov=. tests

all_checks: format_check lint test
