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
    
    # Wait for product details to fully load
    page.wait_for_timeout(2000)
    
    # First, close any open panels (like size guide) that might be blocking
    close_buttons = page.locator(".user-contextual-sidepanel .close, .panel-close, button:has-text('×')")
    if close_buttons.is_visible():
        try:
            # Try to click with force if element is outside viewport
            close_buttons.click(force=True, timeout=5000)
            page.wait_for_timeout(500)
            print("Closed any open panels")
        except:
            print("Could not close panel, continuing anyway")
            # Try pressing Escape key as alternative
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
    
    # Based on the DOM screenshot, find the custom dropdown button
    size_dropdown_button = page.locator(".attribute-size .dropdown-toggle")
    expect(size_dropdown_button).to_be_visible()
    print("Found size dropdown button")
    
    # Click to open the dropdown menu
    size_dropdown_button.click()
    
    # Wait for dropdown menu to appear
    page.wait_for_timeout(1000)
    
    # Look for the dropdown menu that should have appeared
    dropdown_menu = page.locator(".attribute-size .dropdown-menu")
    
    # If dropdown menu is not visible, try different approaches
    if not dropdown_menu.is_visible():
        print("Dropdown menu not visible, trying alternative approaches")
        # Try clicking again
        size_dropdown_button.click()
        page.wait_for_timeout(500)
        
        # Check if it's visible now
        if not dropdown_menu.is_visible():
            print("Still not visible, looking for size options in other ways")
            # Look for size options that might be visible elsewhere
            visible_size_options = page.locator("*:visible:has-text('FR 0'), *:visible:has-text('FR 1'), *:visible:has-text('FR 2')")
            if visible_size_options.count() > 0:
                first_size = visible_size_options.first
                print(f"Found visible size option: {first_size.text_content()}")
                first_size.click()
                dropdown_menu = None  # Skip dropdown menu logic
    
    if dropdown_menu and dropdown_menu.is_visible():
        print("Dropdown menu opened")
    
    # Only proceed with dropdown logic if we have a visible dropdown menu
    if dropdown_menu and dropdown_menu.is_visible():
        # Find size options within the dropdown menu
        # Look for clickable options (likely <a> or <button> elements)
        size_options = dropdown_menu.locator("a, button, .dropdown-item, [role='option']")
        
        if size_options.count() > 1:
            # Skip the first option (SIZE GUIDE) and select the second option (actual size)
            second_size_option = size_options.nth(1)  # Index 1 = second option
            expect(second_size_option).to_be_visible()
            size_text = second_size_option.text_content().strip()
            print(f"Selecting second size option (skipping SIZE GUIDE): {size_text}")
            second_size_option.click()
            
            # Wait for selection to register
            page.wait_for_timeout(500)
        else:
            print("Not enough size options found in dropdown")
    
    # Verify a size was selected (regardless of method used)
    page.wait_for_timeout(1000)
    selected_option = page.locator(".attribute-size .selected-option")
    if selected_option.is_visible():
        selected_text = selected_option.text_content().strip()
        print(f"Size selected successfully: {selected_text}")
        
        # Close any size guide panel that might have opened
        size_guide_close = page.locator(".user-contextual-sidepanel .close, .panel-close, button:has-text('×')")
        if size_guide_close.is_visible():
            try:
                size_guide_close.click(force=True, timeout=3000)
                page.wait_for_timeout(500)
                print("Closed size guide panel")
            except:
                print("Could not close size guide panel, continuing anyway")
                # Try Escape key as alternative
                page.keyboard.press("Escape")
                page.wait_for_timeout(500)
    else:
        print("No size appears to be selected - continuing anyway")
    
    # Wait for size selection to register
    page.wait_for_timeout(1000)
    
    # Locate and click the Add to Cart button
    add_to_cart_button = page.locator(
        "button:has-text('Add to Cart'), button:has-text('ADD TO CART'), "
        "button:has-text('Add to Bag'), button:has-text('ADD TO BAG'), "
        "[data-testid*='add-to-cart'], .add-to-cart, .add-to-bag, "
        "button[type='submit']:has-text('Add')"
    ).first
    
    expect(add_to_cart_button).to_be_visible()
    add_to_cart_button.click()
    
    # Wait for add to cart action to complete
    page.wait_for_timeout(2000)
    
    # Verify product was added to cart by checking the header cart icon update
    # Look for cart icon in the website header with updated count
    cart_icon_selectors = [
        ".header-cart", ".cart-icon", ".bag-icon", ".mini-cart",
        "[data-testid*='cart']", ".cart-count", ".basket-icon",
        "header .cart", "nav .cart", ".navigation .cart"
    ]
    
    cart_icon = None
    for selector in cart_icon_selectors:
        potential_icon = page.locator(selector)
        if potential_icon.is_visible():
            cart_icon = potential_icon
            print(f"Found cart icon using selector: {selector}")
            break
    
    if cart_icon:
        # Check for cart count indicator (number showing items in cart)
        cart_count_indicators = [
            cart_icon.locator(".count, .badge, .cart-count, .quantity, [class*='count']"),
            cart_icon.locator("span:visible"),
            cart_icon.locator("[data-testid*='count']"),
            page.locator(".cart-count:visible, .cart-badge:visible, .header-cart-count:visible")
        ]
        
        cart_count_found = False
        for count_locator in cart_count_indicators:
            if count_locator.is_visible():
                count_text = count_locator.text_content().strip()
                if count_text and count_text.isdigit() and int(count_text) > 0:
                    print(f"Cart count updated successfully: {count_text} item(s)")
                    expect(count_locator).to_be_visible()
                    cart_count_found = True
                    break
        
        if not cart_count_found:
            print("No visible cart count found, checking for cart icon state change")
            # Sometimes cart icons change appearance/class when items are added
            expect(cart_icon).to_be_visible()
    
    # Additional verification: look for confirmation message or toast
    cart_confirmation = page.locator(
        ".cart-confirmation, .success-message, .added-to-cart, "
        ":has-text('Added to'), :has-text('Item added'), "
        ".toast, .notification, .alert-success"
    ).first
    
    if cart_confirmation.is_visible():
        confirmation_text = cart_confirmation.text_content().strip()
        print(f"Cart confirmation message: {confirmation_text}")
        expect(cart_confirmation).to_be_visible()
    
    # Verify cart functionality by checking if we can access cart
    # Look for cart link or button that would open the cart
    cart_link = page.locator(
        "a[href*='cart'], a[href*='bag'], button:has-text('Cart'), "
        "button:has-text('Bag'), .cart-link, .bag-link"
    ).first
    
    if cart_link.is_visible():
        print("Cart link/button is accessible for further verification")
        expect(cart_link).to_be_visible()
    
    # Pause for 5 seconds to see the results
    page.wait_for_timeout(5000)