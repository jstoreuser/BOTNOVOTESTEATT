"""
🎮 Teste Visual do Playwright Bot

Bot simples para demonstrar o Playwright funcionando com browser visível.
Você poderá ver o browser abrindo e executando ações.
"""

import asyncio
import sys
from pathlib import Path

# Add bot root directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from loguru import logger


async def test_playwright_visual():
    """
    🚀 Teste visual do Playwright - você verá o browser abrindo!
    """
    try:
        logger.info("🎮 Starting Playwright Visual Test")
        logger.info("📌 You should see a browser window opening...")

        # Import web engine
        from core.web_engine import WebAutomationEngine

        # Create engine with visible browser
        config = {
            "browser_headless": False,  # IMPORTANTE: Browser visível!
            "target_url": "https://web.simple-mmo.com/travel",
            "debugging_port": 9223,  # Porta diferente para evitar conflitos
        }

        logger.info("🌐 Creating web automation engine...")
        engine = WebAutomationEngine(config)

        logger.info("🚀 Initializing browser (you should see it opening)...")
        success = await engine.initialize()

        if not success:
            logger.error("❌ Failed to initialize browser")
            return

        logger.success("✅ Browser opened! Check your screen.")

        # Get the page
        page = await engine.get_page()
        if not page:
            logger.error("❌ No page available")
            return

        logger.info("📍 Current URL: " + page.url)
        logger.info("📄 Page title: " + await page.title())

        # Simple test actions
        logger.info("🔍 Looking for 'Take a step' buttons...")

        # Find step buttons
        step_buttons = await page.query_selector_all('button:has-text("Take a step")')
        logger.info(f"📊 Found {len(step_buttons)} step buttons")

        if step_buttons:
            logger.info("🎯 Clicking first step button...")
            try:
                await step_buttons[0].click()
                logger.success("✅ Step button clicked!")

                # Wait a bit for page to update
                await asyncio.sleep(2)

                logger.info("📍 New URL: " + page.url)

            except Exception as e:
                logger.warning(f"⚠️ Could not click step button: {e}")
        else:
            logger.info("ℹ️ No step buttons found - that's normal on some pages")

        # Test finding other elements
        logger.info("🔍 Looking for other elements...")

        # Look for attack buttons
        attack_buttons = await page.query_selector_all(
            'button:has-text("Attack"), a:has-text("Attack")'
        )
        logger.info(f"⚔️ Found {len(attack_buttons)} attack elements")

        # Look for gather buttons
        gather_buttons = await page.query_selector_all(
            'button:has-text("gather"), button:has-text("Gather")'
        )
        logger.info(f"⛏️ Found {len(gather_buttons)} gather elements")

        logger.info("⏰ Keeping browser open for 10 seconds so you can see it...")
        await asyncio.sleep(10)

        logger.info("🧹 Cleaning up...")
        await engine.shutdown()

        logger.success("✅ Visual test completed successfully!")
        logger.info(
            "👀 Did you see the browser window? It should have opened and navigated to SimpleMMO!"
        )

    except Exception as e:
        logger.error(f"💥 Error in visual test: {e}")
        logger.exception("Full error traceback:")


def main():
    """Synchronous wrapper"""
    try:
        asyncio.run(test_playwright_visual())
    except KeyboardInterrupt:
        logger.info("🛑 Test interrupted by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")


if __name__ == "__main__":
    main()
