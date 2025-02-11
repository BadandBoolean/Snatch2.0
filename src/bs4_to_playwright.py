import asyncio
from playwright.async_api import expect


# takes in the playwright page object and a tuple of
# selector and locator, determines the appropriate
# playwright command, executes it, and returns the page
async def make_and_execute_playwright_cmd(driver, page, pair_tuple):
    selector = pair_tuple[0]
    locator = pair_tuple[1]
    class_name = pair_tuple[2]
    print(pair_tuple)

    if selector == "label":
        element = await page.get_by_label(locator).scroll_into_view_if_needed()
    elif selector == "href" and class_name != "":
        element = page.locator(f'[href="{locator}"]').filter(
            has=page.locator(f".{class_name}")
        )
        print("the element found is:" + str(element))
        element = await element.scroll_into_view_if_needed()
    elif selector == "text":
        element = await page.get_by_text(locator).scroll_into_view_if_needed()
    elif selector == "placeholder":
        element = await page.get_by_placeholder(locator).scroll_into_view_if_needed()
    elif selector == "alt":
        element = await page.get_by_alt_text(locator).scroll_into_view_if_needed()
    elif selector == "title":
        element = await page.get_by_title(locator).scroll_into_view_if_needed()
    elif selector == "test-id":
        element = await page.get_by_test_id(locator).scroll_into_view_if_needed()
    else:
        raise ValueError(f"Unsupported selector type: {selector}")

    if class_name != "":
        element = await element.filter(
            has=page.locator(f".{class_name}")
        ).scroll_into_view_if_needed()
        print("element here is" + str(element))

    else:
        # click the first element that matches the locator,
        # todo we should make this more rigorous
        element = element.first

    # await element.wait_for(state="visible")
    # await page.wait_for_load_state("networkidle")

    # is_visible = await element.is_visible()
    # is_enabled = await element.is_enabled()
    # print(f"Element visible: {is_visible}, enabled: {is_enabled}")
    try:

        await element.click(timeout=5000)
    except Exception as e:
        print(f"Regular click failed: {str(e)}")
        try:
            await element.click(force=True, timeout=5000)
        except Exception as e:
            print(f"Force click failed: {str(e)}")
            try:
                # Get the selector for the filtered element
                selector_handle = await element.evaluate("el => el.outerHTML")
                await page.evaluate(
                    """
                    (html) => {
                        const template = document.createElement('template');
                        template.innerHTML = html;
                        const element = document.querySelector(html);
                        if (element) {
                            element.click();
                            return true;
                        }
                        return false;
                    }
                """,
                    selector_handle,
                )
            except Exception as e:
                print(f"JavaScript click failed: {str(e)}")

    return page


async def check_element_visible(page, pair_tuple):
    selector = pair_tuple[0]
    locator = pair_tuple[1]
    class_name = pair_tuple[2]
    print(pair_tuple)

    if selector == "label":
        element = page.get_by_label(locator)
    elif selector == "href":
        element = page.locator(f'[href="{locator}"]')
    elif selector == "text":
        element = page.get_by_text(locator)
    elif selector == "placeholder":
        element = page.get_by_placeholder(locator)
    elif selector == "alt":
        element = page.get_by_alt_text(locator)
    elif selector == "title":
        element = page.get_by_title(locator)
    elif selector == "test-id":
        element = page.get_by_test_id(locator)
    else:
        raise ValueError(
            f"Unsupported selector type duirng element visibility check: {selector}"
        )

    if class_name != "":
        element = element.filter(has=page.locator(f".{class_name}"))

    else:
        element = element.first

    try:
        # Wait for network to be idle first
        await page.wait_for_load_state("networkidle")
        await element.scroll_into_view_if_needed()

        # Check if element exists and is visible
        is_visible = await element.is_visible()

        if not is_visible:
            print("Element not visible")
            return False

        # Additional check using expect
        await expect(element).to_be_visible(timeout=5000)
        return True

    except Exception as e:
        print(f"Element not visible: {str(e)}")
        return False
