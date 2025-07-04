# sandro-ux-tests

Automated end-to-end tests for core user flows on the Sandro Paris website, including navigation, product selection, cart management, and checkout, built with Playwright and pytest.

## Prerequisites

- Python 3.8+
- pip

## Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers:**
   ```bash
   playwright install
   ```

4. **Configure environment variables:**
   - Copy `.env` and update values as needed
   - Update `BASE_URL` to target environment

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_filename.py

# Run with browser UI visible
pytest --headed

# Run with custom base URL
BASE_URL=https://staging.sandro-paris.com pytest
```

## Project Structure

```
├── tests/              # Test files
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── .gitignore         # Git ignore rules
└── README.md          # This file
```
