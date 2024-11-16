from openai import OpenAI

from scrape_website import get_and_parse_html, set_up_driver
import datetime
import os
import time
from nav_response_format import NavResponses
from dotenv import load_dotenv

load_dotenv()

"""
messages = client.beta.threads.messages.list(
    thread_id=thread_id
)
print(messages.data[0].content[0].text.value)
"""

llmclient = OpenAI()
ASSISTANT_ID = os.getenv("ASSISTANT_ID_2")
current_time = datetime.datetime.now()


def run_llm_analysis(curr_html_string, this_place_thread):
    # first, add the current html string to the thread as a
    thread_message = llm_assistant_add_new_html_message(
        curr_html_string, this_place_thread.id
    )

    run = llm_assistant_start_run(this_place_thread.id)

    # wait for the assistant to finish this run and respond
    run = llmclient.beta.threads.runs.retrieve(
        thread_id=this_place_thread.id,
        run_id=run.id,
    )
    while run.status != "completed":
        time.sleep(2)
        run = llmclient.beta.threads.runs.retrieve(
            thread_id=this_place_thread.id,
            run_id=run.id,
        )

    # get the response which should be the most recent
    # message
    message = llmclient.beta.threads.messages.list(
        thread_id=this_place_thread.id, limit=1, order="desc"
    )

    response1 = message.data[0].content[0].text.value

    response = message.data[0].content[0].text.value

    # parse the response, which should just be a string
    # of html

    # parsed_response = NavResponses.parse_raw(response)

    # json loads
    # return parsed_response
    return response1


def make_new_thread():
    thread = llmclient.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": f"The current date and time are {current_time}. Remember, you MUST produce JSON per the instructions given to you",
            }
        ]
    )
    return thread


def llm_assistant_start_run(thread_id):
    run = llmclient.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID,
    )

    return run


def llm_assistant_add_new_html_message(html_string, thread_id):
    thread_message = llmclient.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=html_string,
    )
    return thread_message


if __name__ == "__main__":
    driver = set_up_driver()
    driver.get("https://www.backstagesf.com")
    html_string = get_and_parse_html(driver)
    thread = make_new_thread()
    response = run_llm_analysis(html_string, thread)
    print(response)
