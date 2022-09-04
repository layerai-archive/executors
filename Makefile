
POETRY := $(shell command -v poetry 2> /dev/null)
TAG_SUFFIX := "-v.$(shell git rev-parse --short HEAD)"
INSTALL_STAMP := .install.stamp

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

.PHONY: integrationTest
integration-test: $(INSTALL_STAMP) build
	$(POETRY) run pytest -n 8 -vv -m "integration" test --tag-suffix=$(TAG_SUFFIX)

.PHONY: build
build:
	TAG_SUFFIX=$(TAG_SUFFIX) docker compose build ${TARGET}

.PHONY: push
push: build
	TAG_SUFFIX=${TAG_SUFFIX} docker compose push ${TARGET}
	TAG_SUFFIX=${PUSH_OVERWRITE_SUFFIX} docker compose push ${TARGET}
