
# scrape a website for appointments, up to 48 hours from now. 

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import urllib.request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parse_html import parse_html

def get_landing_page_html(url):
    # set up 
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    wait = WebDriverWait(driver, 120)
    # get page source
    main_html = driver.execute_script("return document.documentElement.outerHTML;")
    # parse the html
    parsed_html = parse_html(main_html)
    return parsed_html




# for testing!!!
if __name__ == "__main__":
    # set up 
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.backstagesf.com/")
    wait = WebDriverWait(driver, 120)

    button_to_press = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'glossgenius.com')]")))
    href_to_go_to = button_to_press.get_attribute('href')
    driver.get(href_to_go_to)

    button_to_press = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='ClassicButton_button__iVdWj' and text()='Book Now']")))
    href_to_go_to = button_to_press.get_attribute('href')
    driver.get(href_to_go_to)

    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "gg-dropdown__control")))
    element.click()
    # wait a bit
    time.sleep(2)

    '''
    # get all the html agian 
    body_html = driver.execute_script("return document.body.outerHTML;")
    # write it to a file 
    with open("body_html.html", "w") as f:
        f.write(body_html)
    '''

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='react-select-2-option-0']")))
    element.click()
    # wait a bit
    time.sleep(2)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Select Keratin+ Haircut']")))
    element.click()
    # wait a bit
    time.sleep(2)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'BookingHeader_btnBook__lrjRh')]")))
    element.click()
    # wait a bit
    time.sleep(2)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'rdp-nav_button_next')]")))
    element.click()
    # wait a bit
    time.sleep(2)

    # get all the html agian 
    # make sure to clear the current file  main_html.html   
    open("main_html.html", "w").close()
    main_html = driver.execute_script("return document.documentElement.outerHTML;")
    # parse the html
    parsed_html = parse_html(main_html)
    # write it to a file 
    with open("main_html.html", "w") as f:
        
        f.write(parsed_html)


    time.sleep(20)




    '''
    # find + wait to be clickable 
    button_to_press = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-title='Stylists']")))
    # get href
    href_to_go_to = button_to_press.get_attribute('href')
    driver.get(href_to_go_to)
    
    button_to_press = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Book an Appointment')]")))
    href_to_go_to = button_to_press.get_attribute('href')
    driver.get(href_to_go_to)

    driver.back()

    button_to_press = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'rodneyrbarney.fullslate.com')]")))
    href_to_go_to = button_to_press.get_attribute('href')
    driver.get(href_to_go_to)

    button_to_press = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/services/1')]")))
    href_to_go_to = button_to_press.get_attribute('href')
    driver.get(href_to_go_to)

    button_to_press = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'start=6113')]")))
    href_to_go_to = button_to_press.get_attribute('href')
    driver.get(href_to_go_to)

    button_to_press = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/book?day=6113&services%5B%5D=1&time=43200')]")))
    href_to_go_to = button_to_press.get_attribute('href')
    driver.get(href_to_go_to)


    time.sleep(20)
    '''

    








    '''
    # Step 2: Click the "Click Here To Book Online" button/link
    # Wait until the link is clickable
    
    book_online_button = driver.find_element(By.LINK_TEXT, "CLICK HERE TO BOOK ONLINE")
    # tell driver to get the href of the link in the button
    book_online_button_href = book_online_button.get_attribute('href')
    # tell driver to go to the href
    driver.get(book_online_button_href)

    print(driver.current_url)
    start = time.time()
    wait = WebDriverWait(driver, 120) # this doesn't actually wait yet
    wait.until(EC.url_contains('annakonyukova.glossgenius.com'))
    end = time.time()
    print(end - start)
    start = time.time()
    book_now_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/booking-flow" and text()="Book Now"]')))
    end = time.time()
    print(end - start)
    

    book_now_button_href = book_now_button.get_attribute('href')
    driver.get(book_now_button_href)
    print(driver.current_url)
    time.sleep(2)




    


    
    
    

    
    test_url = "https://www.backstagesf.com/"
    
    result = find_book_now_button(test_url)
    
    if result:
        print("Success! Found a 'Book Now' element")
        
    else:
        print("Test failed: No 'Book Now' element found.")
        '''

# we are actually going to make this into a state machine where the goal is to get to the state where time/date is on the screen. 


# Types of states, where a state is the current page we think we are on. the goal is to get to, and record, the time and date states. 
 #   - book now 
  #  - select service
   # - select stylist
 #   - find time
 #   - find date

# any professional and any service are preferred categories. 

# the state where we are in the book now page. this could also be the landing page. 
def state_book_now_page(driver):
    # most important thing to find is any time/date selector. tihs could be a dropdown, or a date/time picker, or a button date/time. 

    time_selector_input = driver.find_element(By.XPATH, "//input[@type='text']")
    time_selector_button = driver.find_element(By.XPATH, "//button[@type='button']")






# master function
def scrape_website(website_url):
    # todo: link all children here
    driver = webdriver.Chrome()
    
    elements = find_book_now_button(website_url, driver)
    # now we want to check what happens on clicking that button. 
    element.click()
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.staleness_of(element))
    # Print the new URL
    print("New URL:", driver.current_url)
    # if there are no options to select services + stylists, and we
    # are in a different url, then it might be that we have more book-now
    # to find and click through. 
    preference_selector_elements = find_preference_selectors(driver)


    # just using the first returned element for now. 
    recursive_middle_layer(elements[0], driver)


    return
    

def find_book_now_button(website_url, driver):
    try:
        # Navigate to the website
        driver.get(website_url)
            
        # Wait for the page to load (adjust the time as needed)
        time.sleep(5)

        # Use Selenium to find buttons with text containing "book" or "book now"
        book_buttons = driver.find_elements(By.XPATH, """
        //button[
        contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'book')
        or 
        contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'appointment')
        ]
        """)
        if book_buttons:
                print(f"Found {len(book_buttons)} 'Book Now' button(s)")
                for button in book_buttons:
                    print(button)
                    print(button.text)
                return book_buttons # Return the first matching button
            
        # If no button found, try looking for links
        book_links = driver.find_elements(By.XPATH, """
        //a[
        contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'book')
        or 
        contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'appointment')
        ]
    """)
        if book_links:
            print(f"Found {len(book_links)} 'Book Now' link(s)")
            
            # print text for all links
            for link in book_links:
                print(link)
                print(link.text)
            return book_links # Return the first matching link
            
        print("No 'Book Now' button or link found")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def recursive_middle_layer(element, driver):
    element.click()
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.staleness_of(element))
        
    # Print the new URL
    print("New URL:", driver.current_url)

