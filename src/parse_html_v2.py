import asyncio
from playwright.async_api import async_playwright, Page, ElementHandle
from typing import List

REDUNDANT_KEYWORDS = [
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


async def get_clickable_elements(page: Page, original_url: str) -> List[ElementHandle]:

    clickable_selector = (
        "a, "
        "button, "
        "input[type='button'], "
        "input[type='submit'], "
        "[role='button'], "
        "[role='link'], "
        "[onclick], "
        "[onmousedown], "
        "[onmouseup], "
        "[ondblclick]"
    )

    # Query all potential clickable elements
    elements = await page.query_selector_all(clickable_selector)
    clickable = []

    for element in elements:
        # skip elements that are not visible and not disabled
        if await element.is_disabled() or not await element.is_visible():
            continue

        outer_html = await element.evaluate("(node) => node.outerHTML")
        outer_html_lower = outer_html.lower()

        # skip if element contains ref link to original url
        if f'href="{original_url}"' in outer_html_lower:
            continue

        skip_element = False
        for keyword in REDUNDANT_KEYWORDS:
            if keyword in outer_html_lower:
                skip_element = True
                break

        if skip_element:
            continue
        clickable.append(element)
    return clickable


async def explore_clicks_recursively(
    page: Page, original_url: str, max_depth: int, depth: int, visited_paths: set
):

    if depth > max_depth:
        return

    clickables_in_this_state = await get_clickable_elements(page, original_url)
    print(
        f"[Depth={depth}] Found {len(clickables_in_this_state)} clickable elements on {page.url}"
    )

    # We'll iterate over each clickable element
    for index, elem in enumerate(clickables_in_this_state):

        tag_name = await elem.evaluate("(node) => node.tagName.toLowerCase()")
        text_content = (await elem.inner_text() or "").strip()[:30]
        element_id = f"{tag_name}:{text_content} (idx={index} depth={depth})"
        click_path = (page.url, depth, element_id)
        if click_path in visited_paths:
            continue
        visited_paths.add(click_path)
        print(f"  [Depth={depth}] Clicking on element -> {element_id}")

        try:
            await elem.click()
            await page.wait_for_timeout(5000)
            await explore_clicks_recursively(
                page, original_url, max_depth, depth + 1, visited_paths
            )
        except Exception as e:
            print(f"  [Depth={depth}] Click failed on {element_id}, error: {e}")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        url = "https://www.backstagesf.com"
        await page.goto(url)
        await page.wait_for_load_state("domcontentloaded")

        max_depth = 10
        visited_paths = set()

        await explore_clicks_recursively(
            page, url, max_depth=max_depth, depth=0, visited_paths=visited_paths
        )

        clickable = await get_clickable_elements(page, url)
        print(f"Found {len(clickable)} clickable elements.")
        for element in clickable:

            print(element)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
