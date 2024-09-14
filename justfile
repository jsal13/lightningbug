set shell := ["zsh", "-cu"]

default:
  just --list

venv: 
  pip install --upgrade uv
  uv venv \
    && uv pip install -r requirements.txt \
    && uv pip install -r requirements-dev.txt

test:
  python -m pytest --doctest-modules ./tests
