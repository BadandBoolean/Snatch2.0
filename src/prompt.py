from openai import OpenAI
from nav_response_format import NavResponses
from scrape_website import get_and_parse_html
import datetime
llmclient = OpenAI()

current_time = datetime.datetime.now()

system_message = f'''You are a helpful assistant and your objective is to act
like a Selenium WebDriver and find and report available
appointments in the next 24 hours from now. The current date
and time is {current_time}. The user is going to provide you
an excerpt of html from a website, and you are going to tell
the user what you would do next if you were the webdriver.
You MUST follow the following rules when doing this task and
responding to the user: 1. The appointment information that
you seek MIGHT not be present on the page so in that case
you should provide me where you would go next on the website
in order to get closer to your end goal. 2. Your response
should be structured. 3. Please provide me with information
for only ONE best interaction, UNLESS you think you are on a
page with a multiselect of stylists, services, or other
relevant options, in which case the field \'multi\' should
be True, and you should provide me multiple nav responses.
4. For datetimes please provide me with a list of strings
which are the available appointments, but ONLY if you see
them. If you do not see them, please keep as None. 5. For
action, your choices are Proceed, Report or Kill. Proceed
means you need to navigate because the appointments are not
visible on screen yet, Report means you can see appointments
and are ready to report them in datetimes in the same
response. Kill means you think you have reached a dead end -
either because there are NO available appointments in the
next 24 hours (and you can see a calendar view of some kind)
OR you think the next best decision would be to hit back()
on the webdriver. 6. For xpath, always provide the XPATH of
the element you are interacting with, or None if action is
Report or Kill. Make sure that the xpath is in a VALID
format only and that it points to an ELEMENT which can be
interacted with, and not something else. 7. For method, your
choices are Click which corresponds with the click() method
in Selenium Webdriver, Navigate, or None. You should say
Navigate ONLY if the element you want to interact with has a
href attribute. This is the preferred interaction, as
click() sometimes does not work. However, DO NOT SAY
NAVIGATE IF THERE IS NO href attribute present in the
element's xpath. You should use click if the element you
want to interact with doesn\'t have a href attribute OR it
is a dynamic react element that is going to alter the page
in some way, and you need it to get to the next state.
Provide None if action is Report or Kill. 8. For attribute,
provide either \'href\' if method is Navigate, or None if
method is Click or None. 9. If you see stylist or service
multi-select options, you must prioritise selecting those
over any book now buttons. This is because the book now
buttons may lead you to loop over and over again. Please be
thoughtful about this. 10. Please respond in ONLY this EXACT
format. Do not provide any additional explanation or
commentary. Do not provide any additional information or
context. Do not respond with anything other than the EXACT
best action you would take, or actionS if you select
\'multi\' to be true. Now the user will provide you with the
html excerpt from the website:'''



def llm_analyse(html_string):

    completion = llmclient.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": html_string},
        ],
        response_format=NavResponses,
    )

    response = completion.choices[0].message.parsed
    return response

# testing function only
def get_html_string():
    # get the html string from the website
    html_string = get_and_parse_html("https://www.backstagesf.com/")
    # print(html_string)
    return html_string

# testing the function
if __name__ == "__main__":
    response = a_prompt()
    print(response)

