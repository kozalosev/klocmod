export POETRY = $(HOME)/.local/bin/poetry

install:
	curl -sSL https://install.python-poetry.org | python3 - && \
		$(POETRY) self add "poetry-dynamic-versioning[plugin]" && \
		$(POETRY) install --all-extras && \
		$(POETRY) run pip install -r docs/requirements.txt
test:
	$(POETRY) run pytest
build:
	$(POETRY) build
build-docs:
	$(POETRY) add sphinx && $(POETRY) run sphinx-build docs build/sphinx
