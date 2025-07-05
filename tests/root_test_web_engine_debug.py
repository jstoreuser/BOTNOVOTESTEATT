"""
🔍 Web Engine Debug Test

Script especializado para diagnosticar o problema de inicialização do web engine
após stop/start do bot.
"""

import asyncio
import time
from pathlib import Path

# Add src to path
import sys
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir / "src"))

from loguru import logger

async def test_web_engine_initialization():
    """Test detailed web engine initialization process"""
    print("\n🔍 Testing Web Engine Initialization...")

    from automation.web_engine import WebAutomationEngine, WebEngineManager

    # Test 1: Clean slate initialization
    print("\n   Test 1: Clean Slate Initialization")
    print("   " + "="*50)

    # Ensure clean start
    await WebEngineManager.shutdown()

    try:
        engine = await WebEngineManager.get_instance()
        print(f"      ✅ Engine created: {id(engine)}")
        print(f"      ✅ Is initialized: {engine.is_initialized}")

        # Test page availability
        page = await engine.get_page()
        print(f"      ✅ Page available: {page is not None}")

        if page:
            url = page.url
            title = await page.title()
            print(f"      ✅ Page URL: {url}")
            print(f"      ✅ Page title: {title}")

        # Test context destruction check
        is_destroyed = await engine.is_context_destroyed()
        print(f"      ✅ Context destroyed: {is_destroyed}")

    except Exception as e:
        print(f"      ❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()

    # Test 2: Reset and re-initialize
    print("\n   Test 2: Reset and Re-initialize")
    print("   " + "="*50)

    try:
        print("      🔄 Shutting down engine...")
        await WebEngineManager.shutdown()

        print("      ⏳ Waiting 1 second...")
        await asyncio.sleep(1.0)

        print("      🔄 Re-initializing engine...")
        engine2 = await WebEngineManager.get_instance()
        print(f"      ✅ New engine created: {id(engine2)}")
        print(f"      ✅ Is initialized: {engine2.is_initialized}")

        # Test page availability
        page2 = await engine2.get_page()
        print(f"      ✅ Page available: {page2 is not None}")

        if page2:
            url2 = page2.url
            title2 = await page2.title()
            print(f"      ✅ Page URL: {url2}")
            print(f"      ✅ Page title: {title2}")

        # Test context destruction check
        is_destroyed2 = await engine2.is_context_destroyed()
        print(f"      ✅ Context destroyed: {is_destroyed2}")

    except Exception as e:
        print(f"      ❌ Re-initialization failed: {e}")
        import traceback
        traceback.print_exc()

    # Final cleanup
    await WebEngineManager.shutdown()

async def test_browser_connection_methods():
    """Test different browser connection methods"""
    print("\n🔍 Testing Browser Connection Methods...")

    from automation.web_engine import WebAutomationEngine

    # Test direct engine creation (bypassing singleton)
    print("\n   Test: Direct Engine Creation")
    print("   " + "="*30)

    config = {
        "browser_headless": False,
        "target_url": "https://web.simple-mmo.com/travel",
    }

    engine = WebAutomationEngine(config)

    try:
        print("      🔄 Initializing engine...")
        result = await engine.initialize()
        print(f"      ✅ Initialization result: {result}")

        if result:
            print("      ✅ Engine initialized successfully!")

            page = await engine.get_page()
            print(f"      ✅ Page obtained: {page is not None}")

            if page:
                print(f"      ✅ Page URL: {page.url}")
                print(f"      ✅ Page title: {await page.title()}")

                # Test context destruction
                is_destroyed = await engine.is_context_destroyed()
                print(f"      ✅ Context destroyed: {is_destroyed}")
            else:
                print("      ❌ No page available after initialization")
        else:
            print("      ❌ Engine initialization failed")

    except Exception as e:
        print(f"      ❌ Engine test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await engine.cleanup()

async def simulate_bot_cycle():
    """Simulate a bot cycle to see where it fails"""
    print("\n🔍 Simulating Bot Cycle...")

    from automation.web_engine import WebEngineManager

    try:
        # Step 1: Get web engine (like bot_runner does)
        print("   Step 1: Getting web engine...")
        engine = await WebEngineManager.get_instance()
        print(f"      ✅ Engine obtained: {id(engine)}")

        # Step 2: Check context destruction (like bot_runner does)
        print("   Step 2: Checking context destruction...")
        is_destroyed = await engine.is_context_destroyed()
        print(f"      ✅ Context destroyed check: {is_destroyed}")

        if is_destroyed:
            print("      ❌ Context is destroyed - this is the problem!")

            # Debug: Check engine state
            print("      🔍 Debugging engine state:")
            print(f"         - Is initialized: {engine.is_initialized}")
            print(f"         - Has playwright: {engine.playwright is not None}")
            print(f"         - Has browser: {engine.browser is not None}")
            print(f"         - Has context: {engine.context is not None}")
            print(f"         - Has page: {engine.page is not None}")

            # Try to get page directly
            page = await engine.get_page()
            print(f"         - get_page() result: {page is not None}")

        else:
            print("      ✅ Context is healthy!")

    except Exception as e:
        print(f"      ❌ Bot cycle simulation failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await WebEngineManager.shutdown()

def main():
    """Run all diagnostic tests"""
    print("🔍 Web Engine Debug Test")
    print("=" * 60)
    print("This will help diagnose the stop/start crash issue")
    print("=" * 60)

    async def run_all_tests():
        # Test 1: Basic initialization
        await test_web_engine_initialization()

        # Test 2: Connection methods
        await test_browser_connection_methods()

        # Test 3: Simulate bot cycle
        await simulate_bot_cycle()

        print("\n" + "=" * 60)
        print("🔍 Debug tests completed!")
        print("\nPlease check the output above to identify:")
        print("1. Where initialization fails")
        print("2. When page/context becomes None")
        print("3. Why context destruction check returns True")

    try:
        asyncio.run(run_all_tests())
    except Exception as e:
        print(f"\n❌ Debug test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
