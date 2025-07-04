"""
🤖 SimpleMMO Bot - Modern Automation

Simple main entry point for the SimpleMMO Bot using modern technologies:
- Playwright for web automation
- Async/await for performance
- Modular architecture
"""

import asyncio
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

from loguru import logger

# Constants
CYCLE_LOG_INTERVAL = 10  # Log status every 10 cycles

# Add src directory to Python path for direct execution (before other imports)
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(project_root))

# Now we can import our modules
try:
    from automation.web_engine import get_web_engine
    from systems.captcha import CaptchaSystem
    from systems.combat import CombatSystem
    from systems.gathering import GatheringSystem
    from systems.healing import HealingSystem
    from systems.steps import StepSystem
except ImportError as e:
    logger.error(f"Failed to import systems: {e}")
    sys.exit(1)

if TYPE_CHECKING:
    from config.types import BotConfig


async def initialize_systems(config: "BotConfig") -> tuple[Any, ...] | None:
    """Initialize all bot systems"""
    logger.info("🔧 Initializing bot systems...")

    # Initialize web engine
    logger.info("🌐 Initializing web automation engine...")
    web_engine = await get_web_engine()
    if not web_engine:
        logger.error("❌ Failed to initialize web engine")
        return None

    logger.success("✅ Web engine ready")

    # Initialize systems
    gathering = GatheringSystem(config)
    healing = HealingSystem(config)
    steps = StepSystem(config)
    combat = CombatSystem(config)
    captcha = CaptchaSystem(config)

    # Initialize each system
    systems = [
        ("Gathering", gathering),
        ("Healing", healing),
        ("Steps", steps),
        ("Combat", combat),
        ("Captcha", captcha)
    ]

    for name, system in systems:
        try:
            if hasattr(system, 'initialize'):
                result = await system.initialize()
                if not result:
                    logger.error(f"❌ Failed to initialize {name} System")
                    return None
        except Exception as e:
            logger.error(f"❌ Error initializing {name} System: {e}")
            return None

    logger.success("✅ All systems initialized successfully")
    return web_engine, gathering, healing, steps, combat, captcha


async def check_and_handle_captcha(captcha) -> bool:
    """Check and handle captcha if present"""
    if await captcha.is_captcha_present():
        logger.warning("🔒 Captcha detected - resolving...")
        captcha_resolved = await captcha.solve_captcha()
        if not captcha_resolved:
            logger.error("❌ Failed to resolve captcha")
            await asyncio.sleep(5)
            return False
        logger.success("✅ Captcha resolved - continuing automation")
        return True
    return False


async def check_and_handle_gathering(gathering) -> bool:
    """Check and handle gathering opportunities"""
    if await gathering.is_gather_available():
        logger.info("⛏️ Gathering opportunity found!")
        success = await gathering.start_gathering()
        if success:
            logger.success("✅ Gathering completed - checking for new events...")
            return True
        else:
            logger.warning("⚠️ Gathering failed - continuing...")
    return False


async def check_and_handle_combat(combat) -> bool:
    """Check and handle combat opportunities"""
    if await combat.is_combat_available():
        logger.info("⚔️ Combat opportunity found!")
        success = await combat.start_combat()
        if success:
            logger.success("✅ Combat completed - checking for new events...")
            return True
        else:
            logger.warning("⚠️ Combat failed - continuing...")
    return False


async def check_and_handle_healing(healing) -> bool:
    """Check and handle character healing"""
    health_status = await healing.check_health()
    if health_status.get("needs_healing", False):
        logger.info("❤️ Character needs healing!")
        healing_success = await healing.heal_character()
        if healing_success:
            logger.success("✅ Healing completed - continuing...")
            return True
        else:
            logger.warning("⚠️ Healing failed - continuing...")
    return False


async def check_and_handle_step(steps) -> bool:
    """Check and handle step taking"""
    if await steps.is_step_available():
        logger.info("👣 No events found - taking step to trigger new event...")
        step_taken = await steps.take_step()
        if step_taken:
            logger.success("✅ Step taken - checking immediately for new events...")
            return True
        else:
            logger.warning("⚠️ Step failed - continuing...")
    return False


async def run_bot_loop(web_engine, gathering, healing, steps, combat, captcha) -> None:
    """Main bot automation loop"""
    logger.info("🚀 Starting bot automation loop...")

    # Keep track of cycles for reduced logging
    cycles = 0
    last_cycle_log = 0

    try:
        while True:
            cycles += 1

            # Every 10 cycles, show a status update
            if cycles % CYCLE_LOG_INTERVAL == 1 or cycles - last_cycle_log >= CYCLE_LOG_INTERVAL:
                logger.info(f"🔄 Cycle {cycles} - Checking current situation...")
                last_cycle_log = cycles

            # Check for captcha first (highest priority)
            captcha_handled = await check_and_handle_captcha(captcha)
            if captcha_handled is False:  # Captcha failed to resolve
                continue

            # Check for gathering opportunities
            if await check_and_handle_gathering(gathering):
                continue  # Check immediately for new events after gathering

            # Check for combat opportunities
            if await check_and_handle_combat(combat):
                continue  # Check immediately for new events after combat

            # Check character health
            if await check_and_handle_healing(healing):
                continue

            # If no events found, check if step is available
            if await check_and_handle_step(steps):
                continue  # Check immediately for new events after step
            else:
                # Handle step not available case with reduced logging
                await _handle_step_not_available(cycles, last_cycle_log, web_engine, steps)

            # Small delay to prevent CPU overuse
            await asyncio.sleep(0.1)

    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Unexpected error in bot loop: {e}")
    finally:
        await _cleanup_systems(web_engine)


async def _handle_step_not_available(cycles: int, last_cycle_log: int, web_engine, steps) -> None:
    """Handle case when step is not available"""
    # Only log this once per waiting session, not every cycle
    if cycles - last_cycle_log <= 1:  # Only log if we haven't recently logged cycle info
        logger.info("⏳ Step not available - waiting for button to appear...")

    # First, do a quick check if we might need to navigate
    current_url = ""
    try:
        page = await web_engine.get_page()
        if page:
            current_url = page.url
    except Exception:
        pass

    # If not on a game page at all, navigate first
    if not current_url or "simple-mmo.com" not in current_url:
        logger.info("🗺️ Not on game page - navigating to travel page...")
        await steps.navigate_to_travel()
        await asyncio.sleep(2)  # Wait after navigation
        return

    # If we're on a game page, just wait for the step button to appear
    if cycles - last_cycle_log <= 1:  # Only log once per waiting session
        logger.info("🕰️ On game page - waiting for step button...")

    # Wait for step button with indefinite patience (this handles the waiting internally)
    step_available = await steps.wait_for_step_button(timeout=30)
    if step_available:
        logger.success("✅ Step button became available!")
    else:
        logger.debug("⏳ Still waiting for step button...")


async def _cleanup_systems(web_engine) -> None:
    """Clean up systems before exit"""
    try:
        logger.info("🧹 Cleaning up systems...")
        if web_engine:
            await web_engine.shutdown()
        logger.success("✅ Cleanup complete")
    except Exception as e:
        logger.warning(f"⚠️ Cleanup warning (non-critical): {e}")


async def main():
    """
    🚀 Simple main entry point for SimpleMMO Bot
    """
    try:
        logger.info("🤖 Starting SimpleMMO Bot - Modern Edition")

        # Basic configuration
        config: BotConfig = {
            "bot_name": "SimpleMMO Bot Modern",
            "log_level": "INFO",
            "browser_headless": False,
            "auto_heal": True,
            "auto_gather": True,
            "auto_combat": True,
        }

        logger.info("⚙️ Configuration loaded")

        # Initialize all systems
        systems = await initialize_systems(config)
        if not systems:
            logger.error("❌ Failed to initialize systems")
            return

        web_engine, gathering, healing, steps, combat, captcha = systems

        # Run the main bot loop
        await run_bot_loop(web_engine, gathering, healing, steps, combat, captcha)

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
