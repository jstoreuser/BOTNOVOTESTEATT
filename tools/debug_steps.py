"""
🔍 Debug Script - Test Step System

Script para testar o sistema de steps e ver por que o bot não está andando.
"""

import asyncio
import sys
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from loguru import logger


async def test_step_system():
    """Test the step system to see what's wrong"""
    try:
        # Import systems
        from automation.web_engine import get_web_engine
        from systems.steps import StepSystem

        logger.info("🔧 Testing Step System...")

        # Get web engine
        web_engine = await get_web_engine()
        if not web_engine:
            logger.error("❌ Failed to get web engine")
            return

        logger.success("✅ Web engine connected")

        # Get page info
        page = await web_engine.get_page()
        if page:
            url = page.url
            title = await page.title()
            logger.info(f"📍 Current URL: {url}")
            logger.info(f"📄 Page title: {title}")

        # Create step system
        config = {
            "bot_name": "Debug Bot",
            "log_level": "DEBUG",
        }

        steps = StepSystem(config)
        await steps.initialize()

        logger.info("🔍 Testing step availability...")

        # Test step availability multiple times
        for i in range(5):
            step_available = await steps.is_step_available()
            logger.info(f"👣 Step available check {i + 1}: {step_available}")

            if step_available:
                logger.info("✅ Step is available! Trying to take step...")
                step_taken = await steps.take_step()
                logger.info(f"👣 Step taken result: {step_taken}")
                break
            else:
                logger.info("⏳ Step not available, checking page elements...")

                # Check for step elements manually
                try:
                    button_elements = await page.query_selector_all("button")
                    link_elements = await page.query_selector_all("a")

                    logger.info(
                        f"🔍 Found {len(button_elements)} buttons and {len(link_elements)} links"
                    )

                    # Look for step-related elements
                    step_buttons = []
                    step_links = []

                    for btn in button_elements:
                        text = await btn.inner_text()
                        if "step" in text.lower():
                            step_buttons.append(text.strip())

                    for link in link_elements:
                        text = await link.inner_text()
                        if "step" in text.lower():
                            step_links.append(text.strip())

                    logger.info(f"🎯 Step buttons found: {step_buttons}")
                    logger.info(f"🎯 Step links found: {step_links}")

                    # Check specific selectors
                    take_step_btn = await page.query_selector("button:has-text('Take a step')")
                    take_step_link = await page.query_selector("a:has-text('Take a step')")

                    if take_step_btn:
                        is_visible = await take_step_btn.is_visible()
                        is_enabled = await take_step_btn.is_enabled()
                        logger.info(
                            f"🔍 Take step button - visible: {is_visible}, enabled: {is_enabled}"
                        )

                    if take_step_link:
                        is_visible = await take_step_link.is_visible()
                        logger.info(f"🔍 Take step link - visible: {is_visible}")

                except Exception as e:
                    logger.error(f"❌ Error checking elements: {e}")

            await asyncio.sleep(2)

        logger.info("🏁 Test completed")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_step_system())
