"""
🎮 Teste Simples do Playwright Bot

Bot muito simples para testar Playwright sem configurações complexas.
"""

import asyncio

from loguru import logger
from playwright.async_api import async_playwright


async def simple_test():
    """
    🚀 Teste muito simples do Playwright
    """
    try:
        logger.info("🎮 Starting Simple Playwright Test")
        logger.info("📌 You should see a browser window opening...")

        # Start Playwright
        playwright = await async_playwright().start()

        # Launch browser (simple configuration)
        browser = await playwright.chromium.launch(headless=False)

        logger.success("✅ Browser opened successfully!")

        # Create page
        page = await browser.new_page()

        # Navigate to SimpleMMO
        logger.info("🌐 Navigating to SimpleMMO...")
        await page.goto("https://web.simple-mmo.com/travel")
        await page.wait_for_load_state("networkidle")

        logger.info("📍 Current URL: " + page.url)
        logger.info("📄 Page title: " + await page.title())

        # Look for step buttons
        logger.info("🔍 Looking for step buttons...")
        step_buttons = await page.query_selector_all('button:has-text("Take a step")')
        logger.info(f"📊 Found {len(step_buttons)} step buttons")

        if step_buttons:
            logger.info("🎯 Clicking first step button...")
            await step_buttons[0].click()
            await page.wait_for_load_state("networkidle")
            logger.success("✅ Step button clicked!")

        logger.info("⏰ Keeping browser open for 10 seconds...")
        await asyncio.sleep(10)

        # Cleanup
        await browser.close()
        await playwright.stop()

        logger.success("✅ Simple test completed!")

    except Exception as e:
        logger.error(f"💥 Error: {e}")
        logger.exception("Full traceback:")


def main():
    """Run the test"""
    asyncio.run(simple_test())


if __name__ == "__main__":
    main()
