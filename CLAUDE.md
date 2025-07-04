# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A project to gradually implement e2e tests for the Sandro Paris website using Playwright and pytest.

## Development Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_filename.py

# Run with browser UI visible
pytest --headed
```