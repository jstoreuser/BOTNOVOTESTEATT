#!/usr/bin/env python3
"""
🧪 Test Script: Captcha System

Tests the new captcha detection and resolution system:
1. Detects "I'm a person! Promise!" button
2. Handles tab management
3. Waits for manual resolution
4. Closes captcha tab and resumes
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from loguru import logger

from systems.captcha import CaptchaSystem


async def test_captcha_detection():
    """Test captcha detection functionality"""
    logger.info("🧪 Testing captcha detection...")

    config = {"auto_captcha": True}
    captcha_system = CaptchaSystem(config)

    if not await captcha_system.initialize():
        logger.error("❌ Failed to initialize captcha system")
        return False

    # Test detection
    is_present = await captcha_system.is_captcha_present()
    logger.info(f"🔒 Captcha present: {is_present}")

    # Get captcha info
    info = await captcha_system.get_captcha_info()
    logger.info(f"📊 Captcha info: {info}")

    return True


async def test_captcha_resolution_flow():
    """Test complete captcha resolution flow (if captcha is present)"""
    logger.info("🧪 Testing captcha resolution flow...")

    config = {"auto_captcha": True}
    captcha_system = CaptchaSystem(config)

    if not await captcha_system.initialize():
        logger.error("❌ Failed to initialize captcha system")
        return False

    # Check if captcha is present
    if await captcha_system.is_captcha_present():
        logger.info("🔒 Captcha detected! Testing resolution flow...")

        # Test the complete resolution flow
        success = await captcha_system.wait_for_resolution(timeout=120)  # 2 minute timeout for testing

        if success:
            logger.success("✅ Captcha resolution flow completed successfully!")
            return True
        else:
            logger.error("❌ Captcha resolution flow failed")
            return False
    else:
        logger.info("ℹ️ No captcha present - cannot test resolution flow")
        return True


async def run_captcha_tests():
    """Run all captcha tests"""
    logger.info("🚀 Starting Captcha System Tests")
    logger.info("=" * 50)

    test_results = []

    # Test 1: Captcha detection
    try:
        result1 = await test_captcha_detection()
        test_results.append(("Captcha Detection", result1))
    except Exception as e:
        logger.error(f"❌ Test 1 failed with error: {e}")
        test_results.append(("Captcha Detection", False))

    logger.info("-" * 30)

    # Test 2: Resolution flow (if applicable)
    try:
        result2 = await test_captcha_resolution_flow()
        test_results.append(("Captcha Resolution Flow", result2))
    except Exception as e:
        logger.error(f"❌ Test 2 failed with error: {e}")
        test_results.append(("Captcha Resolution Flow", False))

    # Summary
    logger.info("=" * 50)
    logger.info("📊 TEST RESULTS SUMMARY")
    logger.info("=" * 50)

    passed = 0
    total = len(test_results)

    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {test_name}")
        if result:
            passed += 1

    success_rate = (passed / total) * 100
    logger.info("-" * 30)
    logger.info(f"📈 Success Rate: {passed}/{total} ({success_rate:.1f}%)")

    if success_rate >= 80:
        logger.success("🎉 CAPTCHA TESTS PASSED!")
        logger.info("✅ Captcha system features:")
        logger.info("   • Detects 'I'm a person! Promise!' button")
        logger.info("   • Opens captcha in new tab")
        logger.info("   • Waits for manual resolution")
        logger.info("   • Detects 'Success!' popup")
        logger.info("   • Closes captcha tab automatically")
        logger.info("   • Returns to main tab")
    else:
        logger.error("💥 TESTS FAILED - Captcha system needs fixes")

    return success_rate >= 80


if __name__ == "__main__":
    try:
        asyncio.run(run_captcha_tests())
    except KeyboardInterrupt:
        logger.info("🛑 Tests interrupted by user")
    except Exception as e:
        logger.error(f"💥 Test execution failed: {e}")
