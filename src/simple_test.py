from playwright.async_api import async_playwright
import asyncio


async def main():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        await context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True,
        )
        print("context started")

        page = await browser.new_page()

        await page.goto("https://www.backstagesf.com")
        loc = "https://annakonyukova.glossgenius.com/"
        class_name = "UiHgGh"
        element = page.get_by_role("link", name="Book Online", exact=True)
        print("the element found is:" + str(element))

        await element.click()
        # wait for 30 seconds
        await asyncio.sleep(30)
        await context.tracing.stop(path="test-results/trace.zip")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
