#!/usr/bin/env python3
"""
Test travel page navigation and redirection handling
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from loguru import logger
from src.automation.web_engine import get_web_engine


async def test_travel_navigation():
    """Test travel page navigation and redirection handling"""
    logger.info("🧪 Testing travel page navigation...")

    try:
        # Get web engine
        engine = await get_web_engine()
        page = await engine.get_page()

        if not page:
            logger.error("❌ Could not get page")
            return False

        # Test 1: Check current URL
        current_url = page.url
        logger.info(f"📍 Current URL: {current_url}")

        # Test 2: Navigate to home page (simulate redirection)
        logger.info("🔄 Simulating redirection to home page...")
        await page.goto("https://web.simple-mmo.com/")
        await page.wait_for_load_state("networkidle")

        new_url = page.url
        logger.info(f"📍 After redirection: {new_url}")

        # Test 3: Use ensure_on_travel_page to get back
        logger.info("🧭 Testing ensure_on_travel_page...")
        success = await engine.ensure_on_travel_page()

        if success:
            final_url = page.url
            logger.info(f"📍 Final URL: {final_url}")

            if final_url.endswith("/travel"):
                logger.success("✅ Successfully returned to travel page!")
                return True
            else:
                logger.error(f"❌ Failed to return to travel page, still at: {final_url}")
                return False
        else:
            logger.error("❌ ensure_on_travel_page failed")
            return False

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        logger.exception("Full traceback:")
        return False


if __name__ == "__main__":
    result = asyncio.run(test_travel_navigation())
    if result:
        print("\n🎉 Travel navigation test PASSED!")
        print("💡 Redirection handling is working correctly!")
    else:
        print("\n❌ Travel navigation test FAILED!")
