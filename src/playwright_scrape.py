"""Scrape Website using Playwright-Python
"""

import re
from playwright.sync_api import Page, expect, sync_playwright, TimeoutError
import time
from scrape_website import get_and_parse_html
from prompt_assistant import make_new_thread, run_llm_analysis


def get_dynamic_selector(page, selector_type, locator):
    if selector_type == "label":
        print("label selector")
        return page.get_by_label(locator)
    elif selector_type == "text":
        print("text selector")
        return page.get_by_text(locator)
    elif selector_type == "placeholder":
        print("placeholder selector")
        return page.get_by_placeholder(locator)
    elif selector_type == "alt_text":
        print("alt_text selector")
        return page.get_by_alt_text(locator)
    elif selector_type == "title":
        print("title selector")
        return page.get_by_title(locator)
    elif selector_type == "test_id":
        print("test_id selector")
        return page.get_by_test_id(locator)
    elif selector_type == "xpath":
        print("xpath selector")
        return page.locator(locator)
    else:
        raise ValueError(f"Unsupported selector type: {selector_type}")


if __name__ == "__main__":

    with sync_playwright() as p:
        driver = p.chromium.launch(headless=False)
        page = driver.new_page()
        # get a page
        page.goto("https://annakonyukova.glossgenius.com/booking-flow")

        html_string = get_and_parse_html(page)

        # write html string to a file
        with open("html_string.txt", "w") as f:
            f.write(html_string)

        thread = make_new_thread()

        response = run_llm_analysis(html_string, thread)

        print(response)

       

        # locate and click for each nav response

        for nav_response in response.responses:
            selector = nav_response.selector
            locator = nav_response.locator



        element = get_dynamic_selector(page, selector, locator)

        print("clicking the element")
        element.click()
        print("element clicked")

        time.sleep(10)

        driver.close()
