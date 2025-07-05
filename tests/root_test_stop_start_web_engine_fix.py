"""
🧪 Test Stop/Start Fix - Web Engine Singleton Reset

This test validates that the stop/start sequence works properly
by ensuring the web engine singleton is reset between runs.
"""

import asyncio
import time
from pathlib import Path

# Add src to path
import sys
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir / "src"))

def test_web_engine_singleton_reset():
    """Test that web engine singleton can be reset properly"""
    print("\n🧪 Testing Web Engine Singleton Reset...")

    async def test_reset_sequence():
        # Import web engine manager
        from automation.web_engine import WebEngineManager

        print("   1. Creating first web engine instance...")
        engine1 = await WebEngineManager.get_instance()
        print(f"      Engine 1 ID: {id(engine1)}")

        print("   2. Getting same instance (should be identical)...")
        engine2 = await WebEngineManager.get_instance()
        print(f"      Engine 2 ID: {id(engine2)}")
        assert id(engine1) == id(engine2), "Should be same singleton instance"
        print("      ✅ Singleton working correctly")

        print("   3. Shutting down singleton...")
        await WebEngineManager.shutdown()
        print("      ✅ Singleton shutdown complete")

        print("   4. Creating new instance after shutdown...")
        engine3 = await WebEngineManager.get_instance()
        print(f"      Engine 3 ID: {id(engine3)}")
        assert id(engine3) != id(engine1), "Should be new instance after shutdown"
        print("      ✅ New instance created successfully")

        # Cleanup
        await WebEngineManager.shutdown()
        print("      ✅ Final cleanup complete")

    # Run the test
    asyncio.run(test_reset_sequence())
    print("   🎉 Web Engine Singleton Reset test passed!")

def test_bot_runner_reset():
    """Test bot runner reset functionality"""
    print("\n🧪 Testing Bot Runner Reset...")

    from core.bot_runner import BotRunner

    # Create bot runner
    config = {
        "auto_heal": True,
        "auto_gather": True,
        "auto_combat": True,
        "auto_steps": True,
        "auto_captcha": True,
        "browser_headless": False,
        "target_url": "https://web.simple-mmo.com/travel",
    }

    bot_runner = BotRunner(config)

    # Set some state
    bot_runner.running = True
    bot_runner.cycles = 50
    bot_runner.stats["steps_taken"] = 25

    print(f"   Before reset - Running: {bot_runner.running}, Cycles: {bot_runner.cycles}")

    # Test reset
    async def run_reset():
        await bot_runner.reset_state()

    asyncio.run(run_reset())

    print(f"   After reset - Running: {bot_runner.running}, Cycles: {bot_runner.cycles}")

    # Verify
    assert not bot_runner.running, "Should not be running after reset"
    assert bot_runner.cycles == 0, "Cycles should be reset to 0"
    assert bot_runner.stats["steps_taken"] == 0, "Stats should be reset"

    print("   ✅ Bot Runner reset test passed!")

def simulate_stop_start_sequence():
    """Simulate the actual stop/start sequence that happens in GUI"""
    print("\n🧪 Simulating Stop/Start Sequence...")

    async def simulate_sequence():
        from automation.web_engine import WebEngineManager
        from core.bot_runner import BotRunner

        # Simulate starting bot (first time)
        print("   1. First bot start...")
        config = {
            "auto_heal": True,
            "auto_gather": True,
            "auto_combat": True,
            "auto_steps": True,
            "auto_captcha": True,
            "browser_headless": False,
            "target_url": "https://web.simple-mmo.com/travel",
        }

        bot_runner1 = BotRunner(config)
        engine1 = await WebEngineManager.get_instance()
        print(f"      Bot 1 ID: {id(bot_runner1)}")
        print(f"      Engine 1 ID: {id(engine1)}")

        # Simulate stop bot
        print("   2. Stopping bot...")
        bot_runner1.running = False
        await bot_runner1.reset_state()

        # Critical: Reset web engine singleton (this is the fix)
        print("   3. Resetting web engine singleton...")
        await WebEngineManager.shutdown()
        print("      ✅ Web engine singleton reset")

        # Simulate delay between stop and start
        print("   4. Delay between stop and start...")
        await asyncio.sleep(1.0)

        # Simulate starting bot again
        print("   5. Second bot start...")
        bot_runner2 = BotRunner(config)
        engine2 = await WebEngineManager.get_instance()
        print(f"      Bot 2 ID: {id(bot_runner2)}")
        print(f"      Engine 2 ID: {id(engine2)}")

        # Verify they are different instances
        assert id(bot_runner1) != id(bot_runner2), "Bot runners should be different"
        assert id(engine1) != id(engine2), "Engines should be different after reset"

        print("      ✅ Fresh instances created successfully!")

        # Cleanup
        await WebEngineManager.shutdown()

    asyncio.run(simulate_sequence())
    print("   🎉 Stop/Start sequence simulation passed!")

def main():
    """Run all tests"""
    print("🧪 Testing Stop/Start Fix - Web Engine Singleton Reset")
    print("=" * 65)

    try:
        # Test 1: Web engine singleton reset
        test_web_engine_singleton_reset()

        # Test 2: Bot runner reset
        test_bot_runner_reset()

        # Test 3: Full stop/start sequence
        simulate_stop_start_sequence()

        print("\n" + "=" * 65)
        print("🎉 ALL TESTS PASSED!")
        print("\nKey improvements verified:")
        print("✅ Web engine singleton can be reset properly")
        print("✅ Bot runner resets state completely")
        print("✅ Stop/Start sequence creates fresh instances")
        print("\nThe fix should resolve:")
        print("🔧 Stop → Start crash due to stale web engine")
        print("🔧 Context destroyed errors on restart")
        print("🔧 'NoneType' object has no attribute 'send' errors")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
