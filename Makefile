
POETRY := $(shell command -v poetry 2> /dev/null)
REQUIRED_POETRY_VERSION := 1.1.15
INSTALL_STAMP := .install.stamp
TEST_SELECTOR := test
TEST_PYTHON_VERSION := all
TEST_FLAVOR := all

ifneq ($(shell $(POETRY) --version | awk '{print $$3}'), $(REQUIRED_POETRY_VERSION))
$(error "Please use Poetry version $(REQUIRED_POETRY_VERSION). Simply run: poetry self update $(REQUIRED_POETRY_VERSION)")
endif

install: $(INSTALL_STAMP)

$(INSTALL_STAMP): pyproject.toml poetry.lock
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) install
	touch $(INSTALL_STAMP)

.PHONY: format
format: $(INSTALL_STAMP)
	$(POETRY) run isort .
	$(POETRY) run black .

.PHONY: lint
lint: $(INSTALL_STAMP)
	$(POETRY) run isort --check-only .
	$(POETRY) run black --check . --diff

.PHONY: check
check: $(INSTALL_STAMP) lint

.PHONY: build
build:
	docker compose build ${TARGET}

.PHONY: integration-test
integration-test: $(INSTALL_STAMP) build
	$(POETRY) run pytest $(TEST_SELECTOR) \
		--python-version $(TEST_PYTHON_VERSION) --flavor $(TEST_FLAVOR) \
		-m "integration" -n 4

.PHONY: push
push: build
	docker compose push ${TARGET}
