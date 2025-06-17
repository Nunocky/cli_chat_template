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

## Functionality

- これは pythonで書かれた CLI Chat Interfaceの雛形です。
- ユーザーが入力したテキスト、およびそのテキストに対してコンピュータが処理したテキストを出力します。
- やり取りは以下のように鳴ります。
  - まずユーザーがテキストを入力します。
  - そのテキストに対してコンピュータが処理を行い、結果を出力します。コンピュータの処理はアプリケーションごとに変わるので、コールバック関数などを使って実装者が定義できるようにします。また、出力はストリーミングに対応します。
  - これをユーザーが終了するまで繰り返します。終了は、 Ctrl-D (Unix) または Ctrl-Z (Windows)、もしくはテキスト `/quit` で行います。
- その他のフックとして以下が用意されています。
  - on_start: アプリケーション開始時に呼び出されるコールバック
  - on_input: ユーザーが入力したテキストに対して呼び出されるコールバック
  - on_output: コンピュータが出力したテキストに対して呼び出されるコールバック
  - on_exit: アプリケーション終了時に呼び出されるコールバック
  - on_error: エラー発生時に呼び出されるコールバック

## Architecture

- **main.py**: Entry point containing the main() function that prints a welcome message
- **pyproject.toml**: Project configuration using modern Python packaging standards
- Currently a minimal template with no external dependencies

## ライブラリ

- 日本語の対応した cursesライブラリを使用しています。
