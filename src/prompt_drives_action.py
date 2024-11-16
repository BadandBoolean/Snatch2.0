# Based on parameters which is the LLM recommended action,
# the webdriver will drive the user to the next state.
# returns the html of the next state.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time


def prompt_drives_action(driver, action, xpath, method, attribute):
    wait = WebDriverWait(driver, 30)

    original_window = driver.current_window_handle
    original_number_of_windows = len(driver.window_handles)

    try:
        # identify the element by xpath
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        if method == "Click":
            driver.execute_script(
                "var ele = arguments[0];ele.addEventListener('click', function() {ele.setAttribute('automationTrack','true');});",
                element,
            )
            element.click()
            is_clicked = "false"
            while is_clicked == "false":
                try:

                    is_clicked = element.get_attribute("automationTrack")
                    if is_clicked == "true":
                        continue
                    time.sleep(1)
                    element.click()
                except StaleElementReferenceException:
                    continue

        elif method == "Navigate":
            link = element.get_attribute(attribute)
            if link is None:
                return None
            # navigate to the href
            driver.get(link)

        else:
            # It could be None.
            # I really ought to have better handling in this
            # instance here
            time.sleep(5)
            return None

        windows = driver.window_handles
        if len(windows) != original_number_of_windows:
            new_window = windows[-1]
            driver.switch_to.window(new_window)

    except TimeoutException:
        return None
