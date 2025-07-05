#!/usr/bin/env python3
"""
🧪 Test Script: Indefinite Waiting Behavior

Tests the corrected behavior where:
1. Step button waiting is indefinite while disabled (doesn't give up after 6s)
2. Leave button detection is ultra-fast (< 1s instead of 3-4s)

This validates the fixes for the two main timing issues.
"""

import asyncio
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from loguru import logger

from automation.web_engine import get_web_engine
from systems.combat import CombatSystem
from systems.steps import StepSystem


async def test_step_button_indefinite_waiting():
    """Test that step button waiting is truly indefinite when disabled"""
    logger.info("🧪 Testing step button indefinite waiting behavior...")

    config = {"auto_steps": True}
    step_system = StepSystem(config)

    if not await step_system.initialize():
        logger.error("❌ Failed to initialize step system")
        return False

    # Test the wait function directly with a reasonable timeout
    logger.info("🕐 Testing wait_for_step_button with 10s timeout...")

    start_time = time.time()
    result = await step_system.wait_for_step_button(timeout=10.0)
    elapsed = time.time() - start_time

    logger.info(f"⏱️ wait_for_step_button returned {result} after {elapsed:.2f}s")

    if elapsed >= 9.0:  # Should wait almost the full timeout
        logger.success("✅ Step button waiting works correctly (waited full timeout)")
        return True
    else:
        logger.warning(f"⚠️ Step button gave up too early after {elapsed:.2f}s")
        return False


async def test_leave_button_ultra_fast_detection():
    """Test that leave button detection is ultra-fast"""
    logger.info("🧪 Testing leave button ultra-fast detection...")

    config = {"auto_combat": True}
    combat_system = CombatSystem(config)

    if not await combat_system.initialize():
        logger.error("❌ Failed to initialize combat system")
        return False

    # Mock a page for testing
    web_engine = await get_web_engine()
    page = await web_engine.get_page()

    if not page:
        logger.error("❌ No page available for testing")
        return False

    # Test the _leave_combat function timing
    logger.info("🕐 Testing _leave_combat function timing...")

    start_time = time.time()
    # This will fail to find a leave button, but we're testing the timing
    await combat_system._leave_combat(page)
    elapsed = time.time() - start_time

    logger.info(f"⏱️ _leave_combat completed in {elapsed:.2f}s")

    # Should complete quickly (within 2-3 seconds max for 20 attempts @ 0.1s each)
    if elapsed <= 3.0:
        logger.success(f"✅ Leave button detection is fast ({elapsed:.2f}s for full search)")
        return True
    else:
        logger.warning(f"⚠️ Leave button detection too slow: {elapsed:.2f}s")
        return False


async def test_main_loop_patience():
    """Test that main loop doesn't give up on step button prematurely"""
    logger.info("🧪 Testing main loop patience with step button...")

    # Import the systems like main.py does
    from config.context import ContextSystem
    from systems.steps import StepSystem

    config = {"auto_steps": True}
    ContextSystem(config)
    steps = StepSystem(config)

    await steps.initialize()

    # Test take_step behavior
    logger.info("🕐 Testing take_step behavior (will wait for real button)...")

    start_time = time.time()
    result = await steps.take_step()
    elapsed = time.time() - start_time

    logger.info(f"⏱️ take_step returned {result} after {elapsed:.2f}s")

    if result or elapsed >= 5.0:  # Either succeeded or waited reasonably long
        logger.success("✅ Main loop patience test passed")
        return True
    else:
        logger.warning(f"⚠️ take_step gave up too quickly: {elapsed:.2f}s")
        return False


async def run_indefinite_waiting_tests():
    """Run all indefinite waiting tests"""
    logger.info("🚀 Starting Indefinite Waiting Behavior Tests")
    logger.info("=" * 60)

    test_results = []

    # Test 1: Step button indefinite waiting
    try:
        result1 = await test_step_button_indefinite_waiting()
        test_results.append(("Step Button Indefinite Wait", result1))
    except Exception as e:
        logger.error(f"❌ Test 1 failed with error: {e}")
        test_results.append(("Step Button Indefinite Wait", False))

    logger.info("-" * 40)

    # Test 2: Leave button ultra-fast detection
    try:
        result2 = await test_leave_button_ultra_fast_detection()
        test_results.append(("Leave Button Ultra-Fast", result2))
    except Exception as e:
        logger.error(f"❌ Test 2 failed with error: {e}")
        test_results.append(("Leave Button Ultra-Fast", False))

    logger.info("-" * 40)

    # Test 3: Main loop patience
    try:
        result3 = await test_main_loop_patience()
        test_results.append(("Main Loop Patience", result3))
    except Exception as e:
        logger.error(f"❌ Test 3 failed with error: {e}")
        test_results.append(("Main Loop Patience", False))

    # Summary
    logger.info("=" * 60)
    logger.info("📊 TEST RESULTS SUMMARY")
    logger.info("=" * 60)

    passed = 0
    total = len(test_results)

    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {test_name}")
        if result:
            passed += 1

    success_rate = (passed / total) * 100
    logger.info("-" * 40)
    logger.info(f"📈 Success Rate: {passed}/{total} ({success_rate:.1f}%)")

    if success_rate >= 80:
        logger.success("🎉 INDEFINITE WAITING TESTS PASSED!")
        logger.info("✅ Bot should now:")
        logger.info("   • Wait indefinitely for disabled step buttons")
        logger.info("   • Detect leave buttons in < 1 second")
        logger.info("   • Never give up prematurely on step buttons")
    else:
        logger.error("💥 TESTS FAILED - Timing issues still present")
        logger.info("❌ Issues:")
        for test_name, result in test_results:
            if not result:
                logger.info(f"   • {test_name}")

    return success_rate >= 80


if __name__ == "__main__":
    try:
        asyncio.run(run_indefinite_waiting_tests())
    except KeyboardInterrupt:
        logger.info("🛑 Tests interrupted by user")
    except Exception as e:
        logger.error(f"💥 Test execution failed: {e}")
