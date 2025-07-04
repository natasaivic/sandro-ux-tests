# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A project to gradually implement e2e tests for the Sandro Paris website using Playwright and pytest.

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

## Environment Configuration

- Environment variables are stored in `.env` file
- Key variables include:
  - `BASE_URL`: Target website URL (defaults to https://us.sandro-paris.com/)
  - `HEADLESS`: Browser visibility (true/false)
  - `BROWSER`: Browser type (chromium/firefox/webkit)
  - `TIMEOUT`: Test timeout in milliseconds

## Dependencies

- `pytest`: Test framework
- `playwright`: Browser automation
- `pytest-playwright`: Pytest integration for Playwright
- `pytest-html`: HTML test reports

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_navigation.py

# Run with browser UI visible
pytest --headed
```

## Test Implementation Notes

### Modal Handling
- Tests automatically handle privacy consent modals using "Agree and Close" button
- Promotional banners are closed using `.close-button` selector
- Modal handling is implemented with conditional checks to avoid test failures

### Navigation Strategy
- Primary: Uses promotional banner links ("Shop Women") when available
- Fallback: Uses main navigation selectors for reliability
- Multiple selector strategies ensure tests work across different page states

### Test Timing
- Uses `wait_for_load_state("load")` instead of `networkidle` for better reliability
- Includes 5-second pause before browser closes for visual confirmation
- Timeout handling prevents hanging tests

### Product Selection Strategy
- Uses `.product a` selector for finding product links (tested and reliable)
- Validates minimum product count before attempting selection
- Selects second product (index 1) to avoid potential featured/promotional first items
- 3-second timeout allows for dynamic content loading

### Size Selection Implementation
- **Custom dropdown handling**: Uses `.attribute-size .dropdown-toggle` to open size selector
- **Option filtering**: Automatically skips "SIZE GUIDE" (first option) and selects actual sizes
- **Size validation**: Selects second option (`nth(1)`) which corresponds to first actual size (FR 0 / XS)
- **Multiple selector strategies**: Handles both dropdown and direct size option clicking
- **Panel management**: Closes size guide panels that may interfere with cart functionality

### Add to Cart Implementation
- **Button detection**: Uses multiple text variations ("Add to Cart", "ADD TO CART", "Add to Bag")
- **Size prerequisite**: Ensures size is selected before attempting cart addition
- **Error resilience**: Handles overlapping panels using force clicks and escape key
- **Cart verification**: Confirms successful addition through UI feedback and confirmation messages

### Error Handling Strategies
- **Force clicks**: Uses `click(force=True)` for elements outside viewport
- **Escape key fallback**: Presses escape when modal close buttons fail
- **Timeout management**: Uses shorter timeouts (3-5 seconds) for better UX
- **Graceful degradation**: Continues test execution even when non-critical elements fail

### Current Test Coverage
- **Homepage navigation and verification** - Title, URL, and content validation
- **Women's section navigation** - Modal handling and category access
- **Product discovery and selection** - Finds 32+ products and selects second item
- **Product page verification** - Confirms successful navigation to product details
- **Size selection workflow** - Custom dropdown navigation and size validation
- **Cart functionality** - Complete add-to-cart flow with verification
- **Complete e-commerce flow** - Full customer journey from homepage to cart

### Selector Strategy Notes
- **Product selector**: `.product a` (proven to work with 32+ products)
- **Size dropdown**: `.attribute-size .dropdown-toggle` and `.dropdown-menu`
- **Size options**: `nth(1)` to skip SIZE GUIDE and select first actual size
- **Add to cart**: Multiple button text variations with fallback strategies
- **Modal selectors**: `button:has-text('Agree and Close')` and `.close-button`
- **Panel close**: `.user-contextual-sidepanel .close` with force click capability