"""
🤖 SimpleMMO Bot v5.0.0 - Advanced AI-Powered Automation

Modern AI-powered automation bot for SimpleMMO with:
- Intelligent decision making engine
- Advanced captcha resolution
- Smart monitoring and analytics
- Modern GUI interface
- Playwright browser automation

Author: BotNovoTesteAtt Team
Version: 5.0.0
License: MIT
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import NoReturn

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from utils.config import load_config
from utils.logging import setup_logging
from ui.gui import ModernBotGUI
from core.bot_controller import BotController
from core.monitoring_system import MonitoringSystem
from core.ai_decision_engine import AIDecisionEngine


async def main() -> NoReturn:
    """
    🚀 Main entry point for SimpleMMO Bot v5.0.0

    Initializes all core components:
    - AI-powered decision engine
    - Modern GUI interface
    - Advanced monitoring system
    - Playwright automation engine
    - Smart captcha resolution

    Returns:
        NoReturn: Runs until user terminates
    """
    monitoring = None
    bot_controller = None

    try:
        # 📋 Load configuration
        config = await load_config()

        # 📝 Setup advanced logging
        logger = setup_logging(
            level=config.get("log_level", "INFO"),
            enable_file_logging=True,
            enable_analytics=True
        )

        logger.info("🤖 Starting SimpleMMO Bot v5.0.0 - AI-Powered Automation")
        logger.info(f"⚙️ Configuration loaded: {len(config)} settings")

        # 📊 Initialize monitoring system
        monitoring = MonitoringSystem(config)
        await monitoring.start_monitoring()
        logger.info("📊 Advanced monitoring system activated")

        # 🧠 Initialize AI decision engine
        ai_engine = AIDecisionEngine(config)
        await ai_engine.initialize()
        logger.info("🧠 AI decision engine initialized")

        # 🖥️ Initialize modern GUI
        gui = ModernBotGUI(config, monitoring)
        logger.info("🖥️ Modern GUI interface loaded")

        # 🎮 Initialize bot controller
        bot_controller = BotController(
            config=config,
            monitoring=monitoring,
            ai_engine=ai_engine,
            gui=gui
        )
        await bot_controller.initialize()
        logger.info("🎮 Bot controller ready for automation")

        # 🚀 Start the application
        logger.info("🚀 Launching application - Ready for AI-Human collaboration!")
        await gui.run_async(bot_controller)

    except KeyboardInterrupt:
        logger.info("� Application stopped by user request")
    except Exception as e:
        logger.error(f"❌ Critical error in main application: {e}")
        logger.exception("Full error traceback:")
        raise
    finally:
        # 🧹 Cleanup resources
        if bot_controller:
            await bot_controller.shutdown()
        if monitoring:
            await monitoring.stop_monitoring()
        logger.info("✅ Application cleanup completed successfully")

        # Initialize bot controller
        bot_controller = BotController(
            config=config,
            monitoring=monitoring
        )
        logger.info("🎮 Bot controller ready")

        # Initialize modern GUI interface
        gui = ModernBotGUI(
            config=config,
            logger=logger,
            bot_controller=bot_controller,
            monitoring=monitoring
        )
        logger.info("🖥️ Modern GUI interface initialized")

        # Setup cross-system connections
        bot_controller.set_gui_callback(gui.update_from_bot)
        gui.register_callback("start", bot_controller.start)
        gui.register_callback("stop", bot_controller.stop)

        logger.info("🔗 All systems connected and ready")
        logger.info("✨ SimpleMMO automation bot is now running!")
        logger.info("🧠 AI captcha resolution will be added in future updates")

        # Start the bot interface (async main loop)
        await gui.run_async()

    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user (Ctrl+C)")
        if monitoring:
            await monitoring.stop_monitoring()
        sys.exit(0)
    except Exception as e:
        logger.error(f"💥 Critical error: {e}", exc_info=True)
        if monitoring:
            monitoring.record_error("critical_startup_error", str(e))
            await monitoring.stop_monitoring()
        sys.exit(1)


def sync_main() -> None:
    """
    Synchronous wrapper for the async main function.

    This allows the bot to be run from multiple contexts:
    - Command line: python main.py
    - IDE: F5 debug mode
    - Task runner: VS Code tasks
    - Package scripts: entry points in pyproject.toml
    """
    try:
        # Use asyncio.run for proper async context management
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    sync_main()
