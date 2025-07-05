#!/usr/bin/env python3
"""
Quick Stop/Start Test

Simplified test that focuses only on the stop/start issue without complex bot logic.
This validates that the WebEngine can be reset and reinitialized correctly.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_basic_stop_start():
    """Test the basic stop/start functionality"""
    print("🧪 Testing basic stop/start functionality")

    try:
        # Import here to handle path issues
        from automation.web_engine import WebEngineManager

        print("✅ Import successful")

        # Step 1: Get initial instance
        print("\n📝 Step 1: Get initial web engine...")
        try:
            engine = await WebEngineManager.get_instance()
            print(f"✅ Got engine instance: {type(engine)}")

            # Check if it's initialized
            if engine.is_initialized:
                print("✅ Engine is initialized")

                # Try to get a page
                page = await engine.get_page()
                if page:
                    title = await page.title()
                    print(f"✅ Got page with title: {title}")
                else:
                    print("⚠️ No page available")
            else:
                print("⚠️ Engine not initialized")

        except Exception as e:
            print(f"❌ Error in step 1: {e}")
            return False

        # Step 2: Force reset
        print("\n📝 Step 2: Force reset...")
        try:
            await WebEngineManager.force_reset()
            print("✅ Force reset completed")
        except Exception as e:
            print(f"❌ Error in force reset: {e}")
            return False

        # Step 3: Get new instance
        print("\n📝 Step 3: Get new instance...")
        try:
            engine = await WebEngineManager.get_instance()
            print(f"✅ Got new engine instance: {type(engine)}")

            # Check if it's initialized
            if engine.is_initialized:
                print("✅ New engine is initialized")

                # Try to get a page
                page = await engine.get_page()
                if page:
                    title = await page.title()
                    print(f"✅ Got page with title: {title}")
                    print("🎉 Stop/Start test PASSED!")
                    return True
                else:
                    print("❌ No page available after restart")
                    return False
            else:
                print("❌ New engine not initialized")
                return False

        except Exception as e:
            print(f"❌ Error in step 3: {e}")
            return False

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main function"""
    try:
        success = await test_basic_stop_start()
        if success:
            print("\n✅ All tests passed!")
            return 0
        else:
            print("\n❌ Tests failed!")
            return 1
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
        return 1
    except Exception as e:
        print(f"\n❌ Test crashed: {e}")
        return 1
    finally:
        # Clean up
        try:
            from automation.web_engine import WebEngineManager
            await WebEngineManager.force_reset()
        except Exception:
            pass

if __name__ == "__main__":
    import asyncio
    exit_code = asyncio.run(main())
    print(f"\nExit code: {exit_code}")
    sys.exit(exit_code)
