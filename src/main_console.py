"""
🤖 SimpleMMO Bot - Console Entry Point

Console mode entry point for the SimpleMMO Bot.
All bot logic is in bot_runner.py - this file just starts the bot in console mode.
"""

import asyncio
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from loguru import logger

# Add src directory to Python path for direct execution
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(project_root))

# Import bot runner
try:
    from core.bot_runner import run_bot
except ImportError as e:
    try:
        from src.core.bot_runner import run_bot
    except ImportError as e2:
        logger.error(f"Failed to import bot runner: {e}")
        logger.error(f"Alternative import also failed: {e2}")
        sys.exit(1)

if TYPE_CHECKING:
    from config.types import BotConfig


async def main():
    """
    🚀 Main entry point for SimpleMMO Bot Console Mode
    """
    try:
        # Basic configuration
        config: BotConfig = {
            "bot_name": "SimpleMMO Bot Console",
            "log_level": "INFO",
            "browser_headless": False,
            "auto_heal": True,
            "auto_gather": True,
            "auto_combat": True,
        }

        # Run the bot using the runner module
        await run_bot(config)

    except Exception as e:
        logger.error(f"❌ Critical error in main: {e}")
    finally:
        try:
            # Final cleanup
            logger.info("🔚 Bot execution complete")
        except Exception as e:
            logger.warning(f"⚠️ Final cleanup warning: {e}")


def sync_main():
    """Synchronous wrapper for the async main function."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    sync_main()
