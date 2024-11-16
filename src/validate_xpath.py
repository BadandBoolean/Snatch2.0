'''
# Your original XPath selecting the <span>
xpath = "//a[contains(@href, '/book')]/span[@data-testid='book-now']"

# Find the <span> element
element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

# Navigate to the parent <a> element
parent_a = element.find_element_by_xpath('..')  # '..' selects the parent node

# Get the 'href' attribute from the <a> element
link = parent_a.get_attribute('href')

# Navigate to the URL
driver.get(link)
'''
import re

'''  
 Returns:
str: The validated and possibly adjusted XPath string.
None: If the XPath cannot be adjusted to the correct
format.
'''
def validate_xpath_for_nav_link(xpath_string):
    print(f"Validating received string: {xpath_string}")
    # Remove any attribute selectors at the end (e.g., /@href)
    xpath_string = re.sub(r'/@[\w\-]+$', '', xpath_string)

    # Ensure the XPath does not contain unions (|), which select multiple elements
    if '|' in xpath_string:
        return None  # Cannot process XPaths that select multiple elements

    # Define the allowed tag names
    allowed_tags = ['a', 'link', 'area']

    # Split the XPath into steps correctly
    xpath_parts = split_xpath(xpath_string)

    # Initialize variables
    adjusted_xpath = ''
    allowed_tag_found = False

    # Iterate backwards over the XPath parts to find the allowed tag with '@href' condition
    for i in range(len(xpath_parts), 0, -1):
        # Reconstruct the XPath up to this point
        temp_xpath = '/'.join(xpath_parts[:i])
        last_part = xpath_parts[i - 1]
        # Remove predicates to get the tag name
        tag_name_match = re.match(r'^([a-zA-Z]+)', last_part)
        tag_name = tag_name_match.group(1).lower() if tag_name_match else ''

        if tag_name in allowed_tags:
        
            allowed_tag_found = True
            

    if allowed_tag_found:
        # Reconstruct the adjusted_xpath properly, adding back leading slashes
        if xpath_string.startswith('//'):
            adjusted_xpath = '//' + adjusted_xpath
        elif xpath_string.startswith('/'):
            adjusted_xpath = '/' + adjusted_xpath
        return adjusted_xpath
    else:
        # No allowed tag with '@href' found in the XPath
        return None

def split_xpath(xpath_string):
    """
    Splits an XPath expression into its steps, correctly handling predicates.
    """
    xpath_steps = []
    bracket_level = 0
    current_step = ''
    i = 0
    while i < len(xpath_string):
        char = xpath_string[i]
        if char == '/' and bracket_level == 0:
            if current_step:
                xpath_steps.append(current_step)
                current_step = ''
            i += 1
            continue
        else:
            current_step += char
            if char == '[':
                bracket_level += 1
            elif char == ']':
                bracket_level -= 1
        i += 1
    if current_step:
        xpath_steps.append(current_step)
    return xpath_steps


def validate_xpath_for_get_element(xpath_string): 
    pass

if __name__ == '__main__':
    # xpath = "//a[contains(@href, '/book')]/span[@data-testid='book-now']"
    # xpath = "//a[contains(@href, '/book')]
    xpath = "bad xpath"

    print(validate_xpath_for_nav_link(xpath))