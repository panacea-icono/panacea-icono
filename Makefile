.PHONY: dev run lint fmt precommit test

PY=python3

dev:
	$(PY) -m uvicorn main_integrated:app --reload --host 0.0.0.0 --port 8000

run:
	$(PY) -m uvicorn main_integrated:app --host 0.0.0.0 --port 8000

lint:
	black --check . || true
	isort --check-only . || true
	flake8 . || true

fmt:
	black .
	isort .

precommit:
	pre-commit run --all-files || true

test:
	$(PY) - << 'PY'
import importlib; importlib.import_module('main_integrated'); print('OK')
PY
