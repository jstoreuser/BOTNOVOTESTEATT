#!/usr/bin/env python3
"""
Test GUI bot initialization specifically
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from loguru import logger
from src.bot_runner import BotRunner
from src.config.types import BotConfig


async def test_gui_bot_initialization():
    """Test the exact same initialization that GUI uses"""
    logger.info("🧪 Testing GUI bot initialization...")

    # Create config exactly like GUI does
    config: BotConfig = {
        "auto_heal": True,
        "auto_gather": True,
        "auto_combat": True,
        "auto_steps": True,
        "auto_captcha": True,
        "browser_headless": False,
        "target_url": "https://web.simple-mmo.com/travel",
    }

    logger.info(f"📋 Config: {config}")

    # Create bot runner exactly like GUI does
    bot_runner = BotRunner(config)

    try:
        # Test initialization
        logger.info("🔧 Testing initialization...")
        success = await bot_runner.initialize()

        if success:
            logger.success("✅ Bot runner initialized successfully!")

            # Test a single cycle
            logger.info("🔄 Testing single bot cycle...")
            await bot_runner.run_cycle()
            logger.success("✅ Bot cycle completed!")

            # Get stats
            stats = bot_runner.get_stats()
            logger.info(f"📊 Bot stats: {stats}")

            return True
        else:
            logger.error("❌ Bot runner initialization failed!")
            return False

    except Exception as e:
        logger.error(f"❌ Exception during bot initialization: {e}")
        logger.exception("Full traceback:")
        return False
    finally:
        # Don't cleanup to keep browser running
        logger.info("🎯 Keeping browser running for GUI test")


if __name__ == "__main__":
    result = asyncio.run(test_gui_bot_initialization())
    if result:
        print("\n🎉 GUI bot initialization test PASSED!")
        print("💡 You can now test the GUI!")
    else:
        print("\n❌ GUI bot initialization test FAILED!")
