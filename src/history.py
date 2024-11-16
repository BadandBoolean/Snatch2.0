"""
add to the history of a webdriver's actions 
the format of the history is like this: 

history = {
    'first_url': 'www.example.com',
    'steps': [
        {'method': 'Navigate', 'xpath': 'some_xpath', 'href': 'some_href'},
        {'method': 'Click', 'xpath': 'some_xpath', 'href': ''},
        # Add more steps as they come
    ]
}

if method is click, there is no href, so just leave it as an empty string

to access first_url:
history['first_url']

to access steps:
history['steps']

to access a specific step:
history['steps'][0]

to access the method:
history['steps'][0]['method']

to access the xpath:
history['steps'][0]['xpath']

to access the href:
history['steps'][0]['href']

"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def add_to_history_and_return(current_history, method, xpath, href):
    current_history["steps"].append({"method": method, "xpath": xpath, "href": href})

    return current_history


def catch_up_driver(driver, history):
    # have driver go through history and execute steps
    wait = WebDriverWait(driver, 120)
    driver.get(history["first_url"])

    for step in history["steps"]:
        if step["method"] == "Click":
            # wait for the element to be clickable
            element = wait.until(EC.element_to_be_clickable((By.XPATH, step["xpath"])))
            # click the element
            element.click()
        elif step["method"] == "Navigate":
            # wait for the element to be clickable
            element = wait.until(EC.element_to_be_clickable((By.XPATH, step["xpath"])))
            # navigate to the href
            driver.get(step["href"])  # this is the href that the driver should get
        else:
            # this should never happen, but just in case for
            # debugging purposes
            print(f"Unknown method: {step['method']}")
