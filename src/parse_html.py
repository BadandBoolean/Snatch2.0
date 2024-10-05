# Clean the source code obtained from the site to pass into the LLM
# Minifies the html to take less tokens 

from bs4 import BeautifulSoup
from lxml import html, etree
from htmlmin import minify

def parse_html(html_string):
    parser = html.HTMLParser(remove_comments=True)
    try:
        tree = html.fromstring(html_string, parser=parser)
    except Exception as e:
        print("Error parsing HTML:", e)
        return ''

    body = tree.find('body')
    if body is None:
        print("Error: No body tag found in HTML")
        return ''

    # Remove all <font>, <style>, and <script> elements
    etree.strip_elements(body, 'font', 'style', 'script', 'svg', 'iframe', 'noscript', 'img', with_tail=False)
    
    # Serialize the tree back to a string
    cleaned_html = html.tostring(body, encoding='unicode', method='html')

    # Minify the HTML
    minified_html = minify(cleaned_html, remove_comments=True, remove_empty_space=True, remove_all_empty_space=True, reduce_boolean_attributes=True)
    
    return minified_html

