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


def test_navigate_to_women_section(page: Page):
    """Test navigation to Women section from homepage"""
    base_url = os.getenv("BASE_URL", "https://us.sandro-paris.com/")
    
    # Navigate to homepage
    page.goto(base_url)
    
    # Wait for page to load
    page.wait_for_load_state("load")
    
    # Handle privacy consent modal if present
    privacy_close_button = page.locator("button:has-text('Agree and Close')")
    if privacy_close_button.is_visible():
        privacy_close_button.click()
    
    # Close promotional banner if present
    banner_close = page.locator(".close-button").first
    if banner_close.is_visible():
        banner_close.click()
    
    # Use the "Shop Women" link from the promotional banner (more reliable)
    women_link = page.locator("a:has-text('Shop Women')")
    if women_link.is_visible():
        women_link.click()
    else:
        # Fallback to main navigation
        women_nav_link = page.locator("nav a[href*='women'], nav a:has-text('Women')").first
        expect(women_nav_link).to_be_visible()
        women_nav_link.click()
    
    # Verify navigation to Women section
    expect(page).to_have_url(re.compile(r".*women.*", re.IGNORECASE))
    
    # Verify Women section page loaded
    expect(page.locator("body")).to_be_visible()
    
    # Verify page contains clothing categories (indicating successful navigation to women's section)
    expect(page.locator("h1")).to_contain_text("All Clothing", ignore_case=True)
    
    # Wait for product grid to load
    page.wait_for_timeout(3000)  # Give time for products to load
    
    # Find product links (tested working selector)
    product_links = page.locator(".product a")
    
    # Ensure we have at least 2 products
    expect(product_links.first).to_be_visible()
    count = product_links.count()
    assert count >= 2, f"Expected at least 2 products, but found {count}"
    
    # Click on the second product (index 1)
    second_product = product_links.nth(1)
    expect(second_product).to_be_visible()
    second_product.click()
    
    # Verify navigation to product detail page
    expect(page.locator("body")).to_be_visible()
    
    # Verify we're on a product page (URL should contain product info)
    page.wait_for_load_state("load")
    expect(page.locator("h1, .product-title, [data-testid*='title']")).to_be_visible()
    
    # Pause for 5 seconds to see the results
    page.wait_for_timeout(5000)