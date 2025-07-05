#!/usr/bin/env python3
"""
Test bot runner initialization specifically
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from loguru import logger
from src.bot_runner import BotRunner
from src.config.types import BotConfig


async def test_bot_runner():
    """Test the bot runner initialization"""
    logger.info("🧪 Testing bot runner initialization...")

    # Create config
    config: BotConfig = {
        "auto_steps": True,
        "auto_gather": True,
        "auto_heal": True,
        "auto_combat": True,
        "auto_captcha": True,
        "browser_headless": False,
        "target_url": "https://web.simple-mmo.com/travel",
    }

    # Create bot runner
    bot_runner = BotRunner(config)

    try:
        # Test initialization
        logger.info("🔧 Testing initialization...")
        success = await bot_runner.initialize()

        if success:
            logger.success("✅ Bot runner initialized successfully!")

            # Get some basic info
            stats = bot_runner.get_stats()
            logger.info(f"📊 Bot stats: {stats}")

            # Cleanup
            await bot_runner.cleanup()
            logger.info("🧹 Cleanup completed")

            return True
        else:
            logger.error("❌ Bot runner initialization failed!")
            return False

    except Exception as e:
        logger.error(f"❌ Exception during bot runner test: {e}")
        logger.exception("Full traceback:")
        return False


if __name__ == "__main__":
    result = asyncio.run(test_bot_runner())
    if result:
        print("\n🎉 Bot runner test PASSED!")
    else:
        print("\n❌ Bot runner test FAILED!")
