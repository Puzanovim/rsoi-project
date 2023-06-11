ROOT_DIR = identity_provider
SRC_DIR = $(ROOT_DIR)/identity_provider
TESTS = $(ROOT_DIR)/identity_provider_tests
PYTHON_DIR ?= venv/Lib/site-packages
CONFIG_FILE ?= setup.cfg

test:
	$(PYTHON_DIR)/pytest --cache-clear --cov=$(SRC_DIR) $(TESTS)

lint:
	$(PYTHON_DIR)/black --skip-string-normalization --line-length 120 --check $(SRC_DIR)
	$(PYTHON_DIR)/pylint --jobs 4 --rcfile pylintrc --errors-only --disable E1101,E0611,E1135,E1136,E1205 $(SRC_DIR)
	$(PYTHON_DIR)/mypy --cache-dir=/dev/null --config-file=$(CONFIG_FILE) $(SRC_DIR)

format:
	$(PYTHON_DIR)/isort $(SRC_DIR)
	$(PYTHON_DIR)/black --skip-string-normalization --line-length 120 $(SRC_DIR)
	$(PYTHON_DIR)/autoflake --recursive --in-place --remove-all-unused-imports --ignore-init-module-imports $(SRC_DIR)
	$(PYTHON_DIR)/unify --in-place --recursive --quote "'" $(SRC_DIR)

ci:	lint test