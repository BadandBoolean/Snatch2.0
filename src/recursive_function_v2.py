# recursive_function_v2.py
# uses playwright-python to navigate websites and find and
# return dates and times
from playwright.async_api import async_playwright
from history_v2 import (
    new_pw_caught_up_history,
    make_history_and_add_url,
    add_action_to_history_list,
    find_date_from_history_list,
)
from parse_html import (
    get_filtered_clickable_tags,
    make_selector_locator_pairs,
    check_for_times,
)
from bs4_to_playwright import make_and_execute_playwright_cmd, check_element_visible
import asyncio


async def recursive_function_v2(page, history_list, appointments):
    # if the history list is 10 clicks or longer, let's stop
    # and just return the appointments. that way we cut off
    # infinite loops
    if len(history_list) > 10:
        return appointments
    # every recursive run starts with parsing the html for
    # clickable tags
    filtered_clickable_tags = await get_filtered_clickable_tags(page)

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
    print("sl_pairs: ", sl_pairs)
    for sl_pair in sl_pairs:
        # make a new page caught up to the current history
        # list. we also have to make a new driver here and
        # pass it in
        # element_visible = await check_element_visible(page, sl_pair)
        # print("element" + str(sl_pair) + " is " + str(element_visible))
        # if not element_visible:
        #   continue  # pass to next pair, this element is not visible.
        async with async_playwright() as p:
            new_driver = await p.chromium.launch(headless=False)
            new_page = await new_pw_caught_up_history(new_driver, history_list)
            new_page = await make_and_execute_playwright_cmd(
                new_driver, new_page, sl_pair
            )
            new_history_list = add_action_to_history_list(history_list, sl_pair)
            # recursively call the function again

            appointments = await recursive_function_v2(
                new_page, new_history_list, appointments
            )
    return appointments


async def entry_point_one_place(place_url):
    async with async_playwright() as p:
        driver = await p.chromium.launch(headless=False)
        context = await driver.new_context()
        try: 
            await context.tracing.start(
                screenshots=True,
                snapshots=True,
            )
            page = await context.new_page()
            await page.goto(place_url)
            history_list = make_history_and_add_url(place_url)

            # don't make threading for now.
            appointments = []
            # recursively call the function to get the
            # appointments
            appointments = await recursive_function_v2(page, history_list, appointments)
            await context.tracing.stop(path="test-results/trace.zip")
            await context.close()
            await driver.close()
            return appointments
        except Exception as e:
            print(e)
            await context.tracing.stop(path="test-results/trace.zip")
            await context.close()
            await driver.close()


if __name__ == "__main__":
    appointments = asyncio.run(entry_point_one_place("https://www.backstagesf.com/"))
    for appointment in appointments:
        print(appointment)

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
