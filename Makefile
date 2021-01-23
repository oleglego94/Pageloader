install:
	poetry install

test:
	poetry run pytest --cov=page_loader --cov-report xml tests/

lint:
	poetry run flake8 page_loader tests

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	poetry build

package-install:
	pip3 install --user dist/*.whl

package-uninstall:
	pip3 uninstall dist/*.whl

.PHONY: install test lint selfcheck check build package-install delete-build