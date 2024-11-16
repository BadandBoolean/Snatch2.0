import threading
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from prompt_drives_action import prompt_drives_action
from scrape_website import get_and_parse_html, set_up_driver
from history import add_to_history_and_return, catch_up_driver
from validate_xpath import validate_xpath_for_nav_link
from prompt_assistant import make_new_thread, run_llm_analysis

def recursive_function(
    executor, curr_html_string, driver, driver_history, this_place_thread
):
    # housekeeping
    thread_name = threading.current_thread().name
    print(f"Thread {thread_name} started")

    # analyse the html to determine what to do next.
    result = run_llm_analysis(curr_html_string, this_place_thread)
    print(f"Thread {thread_name}: llm analysis result: {result}")

    # in the case of multiple responses.
    if result.responses[0].multi:
        all_responses = result.responses
        print(
            f"Thread {thread_name}: multi-select detected, running all sequentially, but in the future we can run all of these drivers in parallel"
        )
        multichoice_results = []
        for nav_response in all_responses:
            print(
                f"Thread {thread_name}: running thread for nav response: {nav_response}"
            )

            # # validate the xpath if the method is Navigate
            # if nav_response.method == "Navigate":
            #     xpath = validate_xpath_for_nav_link(nav_response.xpath)
            #     if xpath is None:
            #         print(
            #             f"Thread {thread_name}: xpath validation failed, skipping this nav response. bad xpath is {nav_response.xpath}"
            #         )
            #         continue
            # else:
            #     # todo validate the click() method also!
            xpath = nav_response.xpath

            # run the recursive function on the driver, for
            # first response can use the same driver to save
            # time
            if all_responses.index(nav_response) == 0:
                print(
                    f"Thread {thread_name}: running thread for index 0, on the same driver. llm thread id is {this_place_thread.id}"
                )
                prompt_drives_action(
                    driver,
                    nav_response.action,
                    xpath,
                    nav_response.method,
                    nav_response.attribute,
                )
                new_html_string = get_and_parse_html(driver)
                # add the acton and locator to the history
                # passsed down to the recursive function
                new_history = add_to_history_and_return(
                    driver_history, nav_response.method, xpath, nav_response.attribute
                )
                res = recursive_function(
                    executor, new_html_string, driver, new_history, this_place_thread
                )
                if res is not None:
                    multichoice_results.append(res)
            # else need to spin up new driver and run it
            # through the current history before continuing
            else:
                print(
                    f"Thread {thread_name}: spinning up new driver on the same thread, and running it through the history, nav response index {nav_response}. llm thread id is {this_place_thread.id}"
                )
                # set up a new driver
                a_driver = set_up_driver()
                # catch the driver up to the history so we
                # are back in this state right now.
                catch_up_driver(a_driver, driver_history)
                prompt_drives_action(
                    a_driver,
                    nav_response.action,
                    xpath,
                    nav_response.method,
                    nav_response.attribute,
                )
                new_html_string = get_and_parse_html(a_driver)
                new_history = add_to_history_and_return(
                    driver_history, nav_response.method, xpath, nav_response.attribute
                )

                res = recursive_function(
                    executor, new_html_string, a_driver, new_history, this_place_thread
                )
                if res is not None:
                    multichoice_results.append(res)
        return results if results else None

    # Single best option only available. Proceed to
    # navigation with same driver

    elif result.responses[0].action == "Proceed" and result.responses[0].multi is False:
        # reassign for clarity
        single_response = result.responses[0]
        print(
            f"Thread {thread_name}: Navigating driver and repeating function on the same thread. llm thread id is {this_place_thread.id}"
        )

        # # validate the xpath if the method is Navigate
        # if single_response.method == "Navigate":
        #     xpath = validate_xpath_for_nav_link(single_response.xpath)
        #     if xpath is None:
        #         print(
        #             f"Thread {thread_name}: xpath validation failed, skipping this nav response. bad xpath is {single_response.xpath}"
        #         )
        #         return None
        # else:
        #     # todo validate the click() method also!
        xpath = single_response.xpath

        prompt_drives_action(
            driver,
            single_response.action,
            xpath,
            single_response.method,
            single_response.attribute,
        )
        new_html_string = get_and_parse_html(driver)
        new_history = add_to_history_and_return(
            driver_history, single_response.method, xpath, single_response.attribute
        )
        res = recursive_function(
            executor, new_html_string, driver, new_history, this_place_thread
        )
        # return the result of this recursive function thread
        return res
    elif result.responses[0].action == "Kill":
        print(f"Thread {thread_name}: Action is 'kill'; returning None")
        # Return None up the chain, this is a dead end and
        # there is no datetimes to report
        # let's kill this driver first through
        driver.quit()
        return None
    elif result.responses[0].action == "Report":
        # reassign for clarity
        single_response = result.responses[0]
        print(f"Thread {thread_name}: Action is 'report'; returning result.datetimes")
        driver.quit()
        return single_response.datetimes
    else:
        print(f"Thread {thread_name}: Unexpected result '{result}'")
        return None
    print(f"Thread {thread_name}: Ending iterative_function")


if __name__ == "__main__":
    # test recursive_function with just one top thread
    print("Main Thread: Starting the iterative process")

    driver = set_up_driver()
    driver.get("https://www.backstagesf.com")
    initial_html_string = get_and_parse_html(driver)

    driver_history = {"first_url": "https://www.backstagesf.com", "steps": []}

    this_place_thread = make_new_thread()

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(
            recursive_function,
            executor,
            initial_html_string,
            driver,
            driver_history,
            this_place_thread,
        )
        results = future.result()
        print("Main Thread: Iterative process has completed")
        print("Main Thread: Collected results:", results)
