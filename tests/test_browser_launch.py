#!/usr/bin/env python3
"""
Quick test for the updated browser launch logic
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from loguru import logger
from src.automation.web_engine import WebAutomationEngine


async def test_browser_launch():
    """Test the browser launch functionality"""
    logger.info("🧪 Testing browser launch functionality...")

    # Create web engine
    config = {"browser_headless": False, "target_url": "https://web.simple-mmo.com/travel"}

    engine = WebAutomationEngine(config)

    # Test initialization
    success = await engine.initialize()

    if success:
        logger.success("✅ Browser launched successfully!")

        # Get page and test
        page = await engine.get_page()
        if page:
            current_url = page.url
            title = await page.title()
            logger.info(f"📍 Current URL: {current_url}")
            logger.info(f"📄 Page title: {title}")

        # Clean up
        await engine.shutdown()
        logger.info("🧹 Cleaned up successfully")
    else:
        logger.error("❌ Browser launch failed!")

    return success


if __name__ == "__main__":
    result = asyncio.run(test_browser_launch())
    if result:
        print("✅ Browser launch test PASSED")
    else:
        print("❌ Browser launch test FAILED")
