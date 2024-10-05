from openai import OpenAI
from nav_response_format import NavResponseFormat
from scrape_website import get_landing_page_html
import datetime
llmclient = OpenAI()

current_time = datetime.datetime.now()

system_message = f'You are a helpful assistant and your objective is to act like a Selenium WebDriver and find and report available appointments in the next 24 hours and the current date and time is{current_time} The user is going to provide you excerpts of html from a website, and you are going to tell the user what you would do next if you were the webdriver. Note that the appointment information that you seek may not be present on the page, so in that case you should provide me what you would navigate to next in order to get closer to your end goal. Your response should be structured. Please provide me with information for only ONE best interaction. Here are some details for the fields: for datetimes please provide me with a list of strings which are the available appointments, but ONLY if you see them. If you do not see them, please keep as None. For action, your choices are either Proceed, Report, or Kill. Proceed means you need to navigate because the appointments are not visible on screen yet, Report means you can see appointments and are ready to report them in datetimes. Kill means you think you have reached a dead end - either because there are NO available appointments in the next 24 hours (and you can see a calendar view of some kind) OR you think the next best decision would be to hit back() on the webdriver. If you are not sure what to do, please respond with None. For method, your choices are Click which corresponds with the click() method in Selenium Webdriver, or Navigate. You should say Navigate if the element you want to interact with has a href attribute. This is the PREFERRED interaction, as click() sometimes does not work. You should only use click if the element you want to interact with doesn\'t have a href attribute OR it is a dynamic react element that is going to alter the page in some way, and you need it to get to the next state. For attribute provide either \'href\' or None. Always provide the XPATH of the element you are interacting with, UNLESS you are actually providing the date and time. Please respond with ONLY this EXACT format. Do not provide any additional explanation or commentary. Do notprovide any additional information or context. Do not respond with anything other than the EXACT best action you would take. Now the user will provide you with the html excerpt from the website'



def a_prompt():

    completion = llmclient.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": get_html_string()},
        ],
        response_format=NavResponseFormat,
    )

    response = completion.choices[0].message.parsed
    return response

def get_html_string():
    # get the html string from the website
    html_string = get_landing_page_html("https://www.backstagesf.com/")
    # print(html_string)
    return html_string

# testing the function
if __name__ == "__main__":
    response = a_prompt()
    print(response)

