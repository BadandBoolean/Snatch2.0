# recursive_function_v2.py
# uses playwright-python to navigate websites and find and
# return dates and times
from playwright.sync_api import sync_playwright
from history_v2 import (
    new_pw_caught_up_history,
    make_history_and_add_url,
    add_action_to_history_list,
    find_date_from_history_list,
)
from parse_html import get_filtered_clickable_tags, make_selector_locator_pairs
from bs4_to_playwright import make_and_execute_playwright_cmd


def recursive_function_v2(page, history_list, appointments):
    # if the history list is 10 clicks or longer, let's stop
    # and just return the appointments. that way we cut off
    # infinite loops
    if len(history_list) > 10:
        return appointments
    # every recursive run starts with parsing the html for
    # clickable tags
    filtered_clickable_tags = get_filtered_clickable_tags(page)

    # check for times. if we have times, we don't need to
    # click further.
    times_found = check_for_times(filtered_clickable_tags)
    if times_found:
        # somewhere we MUST have recorded the date we
        # clicked on as the third member of the tuple.
        date_for_these_times = find_date_from_history_list(history_list)
        appointments.append({"date": date_for_these_times, "times": times_found})
        return appointments

    # if we don't have times, we need to click further
    sl_pairs = make_selector_locator_pairs(filtered_clickable_tags, page)
    for sl_pair in sl_pairs:
        # make a new page caught up to the current history
        # list
        page = new_pw_caught_up_history(history_list)
        page = make_and_execute_playwright_cmd(page, sl_pair)
        history_list = add_action_to_history_list(history_list, sl_pair)
        # recursively call the function again
        appointments = recursive_function_v2(page, history_list, appointments)
    return appointments


def entry_point_one_place(place_url):
    with sync_playwright() as p:
        driver = p.chromium.launch(headless=True)
        page = driver.new_page()
        page.goto(place_url)
        history_list = make_history_and_add_url(place_url)

        # don't make threading for now.
        appointments = []
        # recursively call the function to get the
        # appointments
        recursive_function_v2(page, history_list, appointments)
        return appointments


# data structure for the return of iterative function is
# list of dictionaries
"""
Example data structure returned by recursive function: list of dictionaries
data = [
    {"date": "2024-11-15", "times": ["09:00 AM", "01:30 PM", "05:00 PM"]},
    {"date": "2024-11-16", "times": ["08:00 AM", "12:00 PM"]},
    {"date": "2024-11-17", "times": ["10:00 AM", "02:00 PM", "06:00 PM"]}
]
"""
