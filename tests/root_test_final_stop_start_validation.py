#!/usr/bin/env python3
"""
Final Stop/Start Validation Test

This test specifically validates that after a stop/start cycle:
1. The web engine can be reset and reinitialized
2. A valid Playwright page is obtained
3. No 'NoneType' object has no attribute 'send' errors occur
4. The bot can perform basic operations

Run this test to validate the final fix.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from automation.web_engine import WebEngineManager
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_stop_start_cycle():
    """Test the complete stop/start cycle"""

    logger.info("🧪 Starting Stop/Start Cycle Validation Test")

    # Test 1: Initial startup
    logger.info("📝 Test 1: Initial startup")

    manager = WebEngineManager.get_instance()
    success = await manager.initialize()

    if not success:
        logger.error("❌ Initial startup failed")
        return False

    page = await manager.get_page()
    if not page:
        logger.error("❌ No page after initial startup")
        return False

    logger.info("✅ Initial startup successful")

    # Test 2: Basic page operation
    logger.info("📝 Test 2: Basic page operation")

    try:
        title = await page.title()
        url = page.url
        logger.info(f"✅ Page accessible - Title: {title}, URL: {url}")
    except Exception as e:
        logger.error(f"❌ Page operation failed: {e}")
        return False

    # Test 3: Force reset (simulating stop)
    logger.info("📝 Test 3: Force reset (simulating stop)")

    await manager.force_reset()
    logger.info("✅ Force reset completed")

    # Test 4: Re-initialization (simulating start)
    logger.info("📝 Test 4: Re-initialization (simulating start)")

    # Get fresh instance
    manager = WebEngineManager.get_instance()
    success = await manager.initialize()

    if not success:
        logger.error("❌ Re-initialization failed")
        return False

    page = await manager.get_page()
    if not page:
        logger.error("❌ No page after re-initialization")
        return False

    logger.info("✅ Re-initialization successful")

    # Test 5: Post-restart page operation
    logger.info("📝 Test 5: Post-restart page operation")

    try:
        title = await page.title()
        url = page.url
        logger.info(f"✅ Post-restart page accessible - Title: {title}, URL: {url}")
    except Exception as e:
        logger.error(f"❌ Post-restart page operation failed: {e}")
        return False

    # Test 6: Multiple stop/start cycles
    logger.info("📝 Test 6: Multiple stop/start cycles")

    for i in range(3):
        logger.info(f"   Cycle {i+1}/3")

        # Stop
        await manager.force_reset()

        # Start
        manager = WebEngineManager.get_instance()
        success = await manager.initialize()

        if not success:
            logger.error(f"❌ Cycle {i+1} initialization failed")
            return False

        page = await manager.get_page()
        if not page:
            logger.error(f"❌ Cycle {i+1} no page")
            return False

        # Test operation
        try:
            title = await page.title()
            logger.info(f"   ✅ Cycle {i+1} successful")
        except Exception as e:
            logger.error(f"❌ Cycle {i+1} page operation failed: {e}")
            return False

    logger.info("🎉 All tests passed! Stop/Start cycle is working correctly.")
    return True

async def main():
    """Main test runner"""
    try:
        success = await test_stop_start_cycle()

        if success:
            logger.info("✅ FINAL VALIDATION: PASSED")
            return 0
        else:
            logger.error("❌ FINAL VALIDATION: FAILED")
            return 1

    except Exception as e:
        logger.error(f"❌ Test crashed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Cleanup
        try:
            manager = WebEngineManager.get_instance()
            await manager.force_reset()
        except Exception:
            pass

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
