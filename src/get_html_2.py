# get html from webpage
# give to v2 llm assistant
# run response through bs4
# print soup
from playwright.sync_api import Page, expect, sync_playwright, TimeoutError
import time
from scrape_website import get_and_parse_html, get_and_parse_html_from_html
from prompt_assistant import make_new_thread, run_llm_analysis
from bs4 import BeautifulSoup


if __name__ == "__main__":

    # with sync_playwright() as p:
    # driver = p.chromium.launch(headless=False)
    # page = driver.new_page()
    # page.goto("https://annakonyukova.glossgenius.com/booking-flow")

    # get the string in html_string.txt
    # Read the content of html_string.txt
    with open("html_string.txt", "r") as file:
        html_string_from_file = file.read()

    html_string = get_and_parse_html_from_html(html_string_from_file)
    # print(html_string)
    # write html string to a file
    # with open("html_string.txt", "w") as f:
    #  f.write(html_string)

    thread = make_new_thread()

    response = run_llm_analysis(html_string, thread)
    # print(response)

    # beautifuul soup the htmls in response
    htmls = response
    print(htmls)

    # driver.close()
