
POETRY := $(shell command -v poetry 2> /dev/null)
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
integrationTest: $(INSTALL_STAMP)
	$(POETRY) run pytest test -m "integration" -n 4 .

.PHONY: build
build:
	docker compose build ${TARGET}

.PHONY: push
push: build
	docker compose push ${TARGET}
