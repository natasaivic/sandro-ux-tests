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
# Activate virtual environment first
source venv/bin/activate

# Run all tests
pytest

# Run specific test file
pytest tests/test_navigation.py

# Run with browser UI visible (headless mode off)
pytest --headed

# Run with custom base URL
BASE_URL=https://staging.sandro-paris.com pytest

# Run with HTML report
pytest --html=test-results/report.html
```

## Available Tests

- `test_navigation.py` - Complete navigation flow from homepage to product selection
  - `test_navigate_to_homepage` - Verifies homepage loads correctly
  - `test_navigate_to_women_section` - End-to-end navigation: Homepage → Women's Section → Product Selection

## Test Coverage

### Navigation Flow
1. **Homepage verification** - Title, URL, and basic content checks
2. **Women's section navigation** - Modal handling and category navigation
3. **Product selection** - Finds and clicks on the second product from the listing
4. **Product page verification** - Confirms successful navigation to product details

## Test Features

- **Modal Handling**: Automatically handles privacy consent modals and promotional banners
- **Product Discovery**: Uses `.product a` selector to find product links (32+ products detected)
- **Robust Navigation**: Uses multiple selector strategies for reliable element finding
- **Visual Feedback**: 5-second pause before browser closes to see results
- **Headed Mode**: Tests run with visible browser by default
- **Product Selection**: Automatically selects the second product from the women's clothing listing

## Test Configuration

Tests are configured via `pytest.ini` with default settings:
- Browser: Chromium
- Mode: Headed (visible browser)
- Reports: HTML report generated in `test-results/`

## Project Structure

```
├── tests/              # Test files
│   └── test_navigation.py  # Homepage navigation test
├── requirements.txt    # Python dependencies
├── pytest.ini         # Pytest configuration
├── .env               # Environment variables
├── .gitignore         # Git ignore rules
├── venv/              # Virtual environment
└── README.md          # This file
```
