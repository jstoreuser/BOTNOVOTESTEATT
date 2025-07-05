#!/usr/bin/env python3
"""
Simple Stop/Start Test

This script tests stop/start functionality by running a simplified version
without the GUI complexity. Run this to validate the core fix.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import logging
from automation.web_engine import WebEngineManager

# Simple logging setup (reduced spam)
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)

async def test_stop_start():
    """Test basic stop/start cycle"""

    print("🧪 Testing Stop/Start Cycle")

    # Test 1: Get initial instance
    print("📝 Step 1: Get initial web engine...")
    manager = await WebEngineManager.get_instance()

    page = await manager.get_page()
    if not page:
        print("❌ No page available")
        return False

    print(f"✅ Initial setup successful - Page title: {await page.title()}")

    # Test 2: Force reset (stop)
    print("📝 Step 2: Force reset (simulating stop)...")
    await WebEngineManager.force_reset()
    print("✅ Force reset complete")

    # Test 3: Get new instance (start)
    print("📝 Step 3: Get new instance (simulating start)...")
    manager = await WebEngineManager.get_instance()

    page = await manager.get_page()
    if not page:
        print("❌ No page available after restart")
        return False

    try:
        title = await page.title()
        print(f"✅ Restart successful - Page title: {title}")
        return True
    except Exception as e:
        print(f"❌ Page operation failed after restart: {e}")
        return False

async def main():
    """Main test"""
    try:
        success = await test_stop_start()
        if success:
            print("🎉 Stop/Start test PASSED")
            return 0
        else:
            print("❌ Stop/Start test FAILED")
            return 1
    except Exception as e:
        print(f"❌ Test crashed: {e}")
        return 1
    finally:
        try:
            await WebEngineManager.force_reset()
        except Exception:
            pass

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
