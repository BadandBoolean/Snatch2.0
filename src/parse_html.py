# Clean the source code obtained from the site to pass into the LLM
# Minifies the html to take less tokens

from bs4 import BeautifulSoup
from lxml import html, etree
from htmlmin import minify
import re

redundant_keywords = [
    "instagram",
    "privacy policy",
    "terms",
    "yelp",
    "facebook",
    "x.com",
    "cookies",
    "privacy",
    "sitemap",
    "linkedin",
    "twitter",
    "youtube",
    "pinterest",
    "whatsapp",
    "tiktok",
    "snapchat",
    "pinterest",
    'https://glossgenius.com"',
    'https://vagaro.com"',
    "https://static.glossgenius.com",
    'href="/"',
    'href="/favicon.ico"',
    'href="/_next/static',
    "<svg ",
    "mailto:",
    "png",
    "jpg",
    "jpeg",
    "gif",
]

clickable_element_tag_names = [
    "a",
    "button",
    "input",
    "select",
    "textarea",
    "label",
]

clickable_element_roles = [
    "button",
]

clickable_element_attr = [
    "href",
    "onclick",
]


# return a list of all elements deemed clickable
def get_clickable_elements_from_html(html_string):
    soup = BeautifulSoup(html_string, "html.parser")
    elements_list = []

    elements_with_tag_names = soup.find_all(clickable_element_tag_names)
    return elements_with_tag_names

    # TODO: figure out what we are going to do with this
    # Find elements with clickable attributes
    # elements_with_attributes = soup.find_all(has_clickable_attribute)
    # all_elements = elements_with_tag_names + elements_with_attributes
    # return all_elements


"""
# Define a function to check for clickable attributes
def has_clickable_attribute(tag):
    # has an attribute which is clickable. and also the

    return any(tag.has_attr(attr) for attr in clickable_element_attr)
"""


def parse_html(html_string):
    parser = html.HTMLParser(remove_comments=True)
    try:
        tree = html.fromstring(html_string, parser=parser)
    except Exception as e:
        print("Error parsing HTML:", e)
        return ""
    body = tree.find("body")
    if body is None:
        print("Error: No body tag found in HTML")
        return ""
    # Remove all <font>, <style>, and <script> elements
    etree.strip_elements(
        body,
        "font",
        "style",
        "script",
        "svg",
        "iframe",
        "noscript",
        "img",
        with_tail=False,
    )
    # Serialize the tree back to a string
    cleaned_html = html.tostring(body, encoding="unicode", method="html")
    # remove some elements that are not needed
    scrubbed_html = remove_redundant_elements(cleaned_html)
    # remove style attributes
    further_scrubbed_html = remove_redundant_attr(scrubbed_html)
    # Minify the HTML
    minified_html = minify(
        further_scrubbed_html,
        remove_comments=True,
        remove_empty_space=True,
        remove_all_empty_space=True,
        reduce_boolean_attributes=True,
    )
    return minified_html


"""
# Remove elements relating to website fodder like Privacy
# Policy, Terms of Service, and Cookies. Remove links to
# social media like instagram, facebook, X, etc.
def remove_redundant_elements(html):
    # soupify the html
    soup_html = BeautifulSoup(html, "html.parser", multi_valued_attributes=None)

    for element in soup_html.find_all(
        string=lambda text: any(k.lower() in text.lower() for k in redundant_keywords)
    ):
        parent = element.parent
        if parent:
            parent.decompose()

    # kill all elements where href tag contains instagram
    # link
    for element in soup_html.find_all("a"):
        if "instagram" in element.get("href", ""):
            element.decompose()

    return str(soup_html)
"""


# removes heavy attributes like style
def remove_redundant_attr(html):
    # soupify the html
    soup_html = BeautifulSoup(html, "html.parser")

    for element in soup_html.find_all(True):
        if element.has_attr("style"):
            del element["style"]
        if element.has_attr("target"):
            del element["target"]
        # EXPERIMENTAL!!! remove class attribute from all
        # tags
        if element.has_attr("class"):
            del element["class"]

    return str(soup_html)


# create a python list of pairs of locator and
# selector values. for example 'title' and 'Select W
# Haircut'
# we need to make sure that
def make_selector_locator_pairs(tags, page):
    locator_pairs = []
    for tag in tags:
        selector_locator = find_selector_locator(tag)
        if selector_locator is not None:
            # we also want to find a class specifier for
            # each tag. it will be indexed in the same
            # location as the selector locator
            # empty string is no class found
            selector_locator = add_class_specifier(tag, selector_locator)
            selector_locator = add_date_if_exists(tag, selector_locator, page)
            locator_pairs.append(selector_locator)

    return locator_pairs


date_pattern = re.compile(r"^(?:[1-9]|[12][0-9]|3[01])$")


def add_class_specifier(tag, selector_locator):
    if tag.has_attr("class"):
        selector_locator = (
            selector_locator[0],  # selector
            selector_locator[1],  # locator
            " ".join(tag["class"]),  # class specifier
        )
    else:
        selector_locator = (
            selector_locator[0],  # selector
            selector_locator[1],  # locator
            "",  # class specifier - empty string
        )
    return selector_locator


def add_date_if_exists(tag, selector_locator, page):
    if tag.string and date_pattern.search(tag.string.strip()):
        # let's also find the month in the code
        month = find_month_in_code(page)
        if month is not None:
            # add a string consisting of date and month to
            # end of selector locator
            selector_locator = (
                selector_locator[0],  # selector
                selector_locator[1],  # locator
                selector_locator[2],  # class
                tag.string.strip() + " " + month,  # date
            )
    return selector_locator


def find_selector_locator(tag):
    # first finding for get_by_alt_text
    if tag.has_attr("alt"):
        return ("alt", tag["alt"])

    # find by href attribute
    if tag.has_attr("href"):
        return ("href", tag["href"])

    # text
    if tag.text is not None:
        # make sure the text is not empty either
        if tag.text.strip() != "":
            return ("text", tag.text)

    # now the cases for getting by placeholder
    if tag.has_attr("placeholder"):
        return ("placeholder", tag["placeholder"])

    # title
    if tag.has_attr("title"):
        return ("title", tag["title"])

    # now the cases for getting by label. there are two ways
    # here
    if tag.has_attr("aria-label"):
        return ("label", tag["aria-label"])
    if tag.name == "label":
        return ("label", tag.text)

    # test-id
    if tag.has_attr("data-testid"):
        return ("test-id", tag["data-testid"])

    else:
        return


time_pattern = re.compile(r":.*\b(?:AM|PM|am|pm)\b")


def check_for_times(tags):
    times_found = []
    for tag in tags:
        if tag.string and time_pattern.search(tag.string):
            times_found.append(tag.string)
    return times_found


async def get_filtered_clickable_tags(page):
    # first get the html
    main_html = await page.evaluate("document.documentElement.outerHTML")
    all_clickable_tags = get_clickable_elements_from_html(main_html)
    filtered_clickable_tags = filter_clickable_tags(all_clickable_tags)
    return filtered_clickable_tags


month_pattern = re.compile(
    r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\b",
    re.IGNORECASE,
)


def find_month_in_code(page):
    main_html = page.evaluate("document.documentElement.outerHTML")
    soup = BeautifulSoup(main_html, "html.parser")
    for tag in soup.find_all("code"):
        if month_pattern.search(tag.text):
            return tag.text


def filter_clickable_tags(all_clickable_tags):
    good_tags = []
    for tag in all_clickable_tags:
        html_string = str(tag)
        if any(k.lower() in html_string.lower() for k in redundant_keywords):
            pass
        else:
            good_tags.append(tag)

    return good_tags


# testing only
if __name__ == "__main__":
    # read from file

    OG_URL_TO_BE_REPLACED_AND_FILTERED_OUT = "https://backstagesf.com"
    CURR_URL_TO_BE_REPLACED_AND_FILTERED_OUT = (
        "https://www.annakonyukova.glossgenius.com/booking-flow"
    )

    with open("html_string.txt", "r") as file:
        html_string_from_file = file.read()

    tags = get_clickable_elements_from_html(html_string_from_file)
    print("number of original tags: ", len(tags))
    # filter the tags further to remove the ones which
    # contain any of the keywords.
    good_tags = []
    for tag in tags:
        # stringify
        html_string = str(tag)

        if any(k.lower() in html_string.lower() for k in redundant_keywords):
            pass
        else:
            good_tags.append(tag)

    # todo: filter out the tags containing og and curr url

    for tag in good_tags:
        print(tag)
        print("\n")
    print("number of filtered tags: ", len(good_tags))
    print("we removed ", len(tags) - len(good_tags), " tags, good job!")

    # check if the text of any tag contains a time
    times = check_for_times(good_tags)

    locator_pairs = make_selector_locator_pairs(good_tags)

    print("number of locator pairs: ", len(locator_pairs))

    for pair in locator_pairs:
        print(pair)
