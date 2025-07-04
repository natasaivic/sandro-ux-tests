import os
import re
from playwright.sync_api import Page, expect


def test_navigate_to_homepage(page: Page):
    """Test navigation to Sandro Paris homepage"""
    base_url = os.getenv("BASE_URL", "https://us.sandro-paris.com/")
    
    # Navigate to homepage
    page.goto(base_url)
    
    # Verify page loaded successfully
    expect(page).to_have_title(re.compile(r".*Sandro.*", re.IGNORECASE))
    
    # Verify URL is correct
    expect(page).to_have_url(base_url)
    
    # Basic page content verification
    expect(page.locator("body")).to_be_visible()