
# takes in the playwright page object and a tuple of
# selector and locator, determines the appropriate
# playwright command, executes it, and returns the page 
def make_and_execute_playwright_cmd(page, pair_tuple):
    selector = pair_tuple[0]
    locator = pair_tuple[1]
    if selector == "label":
        page.get_by_label(locator).click()
    elif selector == "text":
        page.get_by_text(locator).click()
    elif selector == "placeholder":
        page.get_by_placeholder(locator).click()
    elif selector == "alt":
        page.get_by_alt_text(locator).click()
    elif selector == "title":
        page.get_by_title(locator).click()
    elif selector == "test_id":
        page.get_by_test_id(locator).click()
    else:
        raise ValueError(f"Unsupported selector type: {selector}")

    return page