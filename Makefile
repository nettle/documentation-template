all: help

VENV := . .venv/bin/activate

sync:
	@uv sync -q

init: sync
	@$(VENV) && echo "Run:  . .venv/bin/activate"

clean:
	rm -rf uv.lock
	rm -rf .venv
	rm -rf output
	rm -rf */*.pyc */__pycache__ .pytest_cache */*.egg-info

docx: sync
	@echo "Building DOCX"
	@$(VENV) && python -B tools/build-docx.py docs/system-design

pdf: sync
	@echo "Building PDF"
	@$(VENV) && python -B tools/build-pdf.py docs/system-design

help:
	@echo "Note: UV package manager for python is required"
	@echo "      https://github.com/astral-sh/uv"
	@echo "Goals:"
	@echo "   make init      - fetch all dependencies to .venv"
	@echo "   make clean     - remove artifacts"
	@echo "   make docx      - build DOCX from docs/system-design/"
	@echo "   make pdf       - build PDF from docs/system-design/"
