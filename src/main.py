"""
🤖 SimpleMMO Bot - Entry Point

Clean entry point for the SimpleMMO Bot.
All bot logic is in bot_runner.py - this file just starts the bot.
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
    from bot_runner import run_bot
except ImportError as e:
    logger.error(f"Failed to import bot runner: {e}")
    sys.exit(1)

if TYPE_CHECKING:
    from config.types import BotConfig


async def main():
    """
    🚀 Main entry point for SimpleMMO Bot
    """
    try:
        # Basic configuration
        config: "BotConfig" = {
            "bot_name": "SimpleMMO Bot Modern",
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
