# Variables
VENV=venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
PYCACHE=$(shell find . -name "__pycache__")

venv:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

install: venv
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) -m unittest discover -s tests

run:
	$(PYTHON) -m cli.wgagent $(ARGS)

# Limpieza de cachés de Python
clean:
	@echo "[*] Cleaning Python cache..."
	@rm -rf $(PYCACHE)

clean-all: clean
	@echo "[*] Removing virtual environment..."
	@rm -rf $(VENV)
	@echo "[*] All cleaned!"
