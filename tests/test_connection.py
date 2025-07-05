#!/usr/bin/env python3
"""
Test if bot can connect to running Chromium
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from loguru import logger
from src.automation.web_engine import WebAutomationEngine


async def test_connection():
    """Test connection to running browser"""
    logger.info("🔗 Testing connection to running Chromium...")

    # Create web engine (should connect to existing browser)
    config = {"browser_headless": False, "target_url": "https://web.simple-mmo.com/travel"}
    engine = WebAutomationEngine(config)

    # Test connection
    success = await engine.initialize()

    if success:
        logger.success("✅ Connected to running browser!")

        # Get page info
        page = await engine.get_page()
        if page:
            current_url = page.url
            title = await page.title()
            logger.info(f"📍 Current URL: {current_url}")
            logger.info(f"📄 Page title: {title}")

            # Test if we can find step buttons
            step_buttons = await page.query_selector_all('button:has-text("Take a step")')
            logger.info(f"👣 Found {len(step_buttons)} step buttons")

        else:
            logger.warning("⚠️ Could not get page")

        # Clean up (don't close browser, just disconnect)
        await engine.cleanup()
        logger.info("🔌 Disconnected from browser (browser still running)")

    else:
        logger.error("❌ Could not connect to browser")

    return success


if __name__ == "__main__":
    result = asyncio.run(test_connection())
    if result:
        print("\n🎉 Connection test PASSED!")
    else:
        print("\n❌ Connection test FAILED!")
