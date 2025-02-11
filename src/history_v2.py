# make, go through, and retrieve history
from playwright.async_api import async_playwright
from bs4_to_playwright import make_and_execute_playwright_cmd
import asyncio


def add_action_to_history_list(history_list, selector_locator_pair):
    if len(history_list) == 0:
        raise Exception("History list is empty")
    # add the action to the history list
    history_list.append(selector_locator_pair)
    return history_list


def make_history_and_add_url(url):
    history_list = []
    history_list.append(url)
    return history_list


# spin up a new playwright and catch up to the current spot in history
async def new_pw_caught_up_history(driver, history_list):
    async with async_playwright() as p:
        page = await driver.new_page()
        await page.goto(history_list[0])
        for step in history_list[1:]:
            # find and execute the right playwright python
            # function, return the page
            page = await make_and_execute_playwright_cmd(driver, page, step)

    return page


def find_date_from_history_list(history_list):
    if len(history_list) < 3:
        raise Exception("History list is not long enough, something is wrong")
    for selector_locator_date in history_list:
        if selector_locator_date[3] is not None:
            return selector_locator_date[3]
    raise Exception("Could not find date in history list")


"""
date structure for history list:

history_list = ["website_url", ("selector", "locator", "maybe_date"), ("selector", "locator", "maybe_date"), ("selector", "locator", "maybe_date")]"""
