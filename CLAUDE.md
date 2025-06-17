# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python CLI chatbot template project using modern Python (>=3.13) with uv for dependency management.

## Commands

### Running the application
```bash
python main.py
```

### Project management
```bash
# Install dependencies (when added to pyproject.toml)
uv sync

# Add new dependencies
uv add <package-name>

# Run in development mode
uv run python main.py
```

## Architecture

- **main.py**: Entry point containing the main() function that prints a welcome message
- **pyproject.toml**: Project configuration using modern Python packaging standards
- Currently a minimal template with no external dependencies

## ライブラリ

- 日本語の対応した cursesライブラリを使用しています。
