.PHONY: install format lint test sec

install:
	@poetry install

format:
	@blue src/. tests/.
	@isort src/. tests/.

lint:
	@blue --check src/. tests/.
	@isort --check src/. tests/.

test:
	@pytest tests/. -v