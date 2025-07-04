"""
🤖 SimpleMMO Bot Runner - Core Bot Logic

This module contains all the bot execution logic, separated from the main entry point.
The main.py file should only be responsible for starting the bot.
"""

import asyncio
from typing import TYPE_CHECKING, Any

from loguru import logger

# Constants
CYCLE_LOG_INTERVAL = 50  # Log status every 50 cycles (more efficient)
NAVIGATION_CHECK_INTERVAL = 500  # Check navigation every 500 cycles (less frequent)
MAIN_LOOP_DELAY = 0.1  # Slightly longer delay to reduce CPU usage

if TYPE_CHECKING:
    from config.types import BotConfig


class BotRunner:
    """
    🤖 Bot Runner Class for GUI Integration

    Provides better control and integration with GUI interfaces.
    """

    def __init__(self, config: "BotConfig"):
        """Initialize bot runner"""
        self.config = config
        self.running = False
        self.paused = False
        self.cycles = 0

        # Systems
        self.web_engine = None
        self.gathering = None
        self.healing = None
        self.steps = None
        self.combat = None
        self.captcha = None

        # Statistics
        self.stats = {
            "cycles": 0,
            "steps_taken": 0,
            "successful_steps": 0,
            "failed_steps": 0,
            "combat_wins": 0,
            "gathering_success": 0,
            "captcha_solved": 0,
            "healing_performed": 0,
        }

    async def initialize(self) -> bool:
        """Initialize all bot systems"""
        try:
            systems = await initialize_systems(self.config)
            if not systems:
                return False

            self.web_engine, self.gathering, self.healing, self.steps, self.combat, self.captcha = (
                systems
            )
            return True

        except Exception as e:
            logger.error(f"❌ Failed to initialize bot: {e}")
            return False

    async def run_cycle(self) -> dict[str, bool]:
        """Run a single bot cycle and return results"""
        if not self.web_engine:
            raise RuntimeError("Bot not initialized")

        self.cycles += 1
        self.stats["cycles"] = self.cycles
        results: dict[str, bool] = {}

        try:
            # Check for captcha first (highest priority)
            captcha_handled = await check_and_handle_captcha(self.captcha)
            if captcha_handled:
                self.stats["captcha_solved"] += 1
                results["captcha"] = True
                return results

            # Check for gathering opportunities
            gather_result = await check_and_handle_gathering(self.gathering)
            if gather_result:
                self.stats["gathering_success"] += 1
                results["gathering"] = True
                return results

            # Check for combat opportunities
            combat_result = await check_and_handle_combat(self.combat)
            if combat_result:
                self.stats["combat_wins"] += 1
                results["combat"] = True
                return results

            # Check character health
            healing_result = await check_and_handle_healing(self.healing)
            if healing_result:
                self.stats["healing_performed"] += 1
                results["healing"] = True
                return results

            # Check for step availability
            step_result = await check_and_handle_step(self.steps)
            if step_result:
                self.stats["steps_taken"] += 1
                self.stats["successful_steps"] += 1
                results["step"] = True
            else:
                if self.steps and await self.steps.is_step_available():
                    self.stats["failed_steps"] += 1
                results["step"] = False

            # Check navigation if needed
            if self.cycles % NAVIGATION_CHECK_INTERVAL == 0:
                await _check_navigation_if_needed(self.web_engine, self.steps)

            return results

        except Exception as e:
            logger.error(f"❌ Error in bot cycle {self.cycles}: {e}")
            results["error"] = True
            return results

    def get_stats(self) -> dict[str, Any]:
        """Get current bot statistics"""
        return self.stats.copy()

    async def initialize(self):
        """Initialize the bot and all systems"""
        logger.info("🔧 Initializing bot systems...")

        systems = await initialize_systems(self.config)
        if not systems:
            raise RuntimeError("Failed to initialize bot systems")

        (self.web_engine, self.gathering, self.healing, self.steps, self.combat, self.captcha) = (
            systems
        )

        logger.success("✅ Bot initialized successfully")

    async def cleanup(self):
        """Cleanup bot and all systems"""
        try:
            await _cleanup_systems(self.web_engine)
            logger.success("✅ Bot cleanup completed")
        except Exception as e:
            logger.warning(f"⚠️ Cleanup warning: {e}")

    async def shutdown(self):
        """Shutdown bot and cleanup"""
        await self.cleanup()

    def update_config(self, new_config: "BotConfig") -> None:
        """Update bot configuration and propagate to all systems"""
        self.config.update(new_config)

        # Update each system's configuration
        systems = [self.gathering, self.healing, self.steps, self.combat, self.captcha]

        for system in systems:
            if system and hasattr(system, "config"):
                system.config.update(new_config)
                # Update specific auto flags
                if hasattr(system, "auto_gather"):
                    system.auto_gather = new_config.get("auto_gather", True)
                if hasattr(system, "auto_combat"):
                    system.auto_combat = new_config.get("auto_combat", True)
                if hasattr(system, "auto_heal"):
                    system.auto_heal = new_config.get("auto_heal", True)

        logger.info("⚙️ Configuration updated for all systems")


async def initialize_systems(config: "BotConfig") -> tuple[Any, ...] | None:
    """Initialize all bot systems"""
    logger.info("🔧 Initializing bot systems...")

    # Import here to avoid circular imports
    from automation.web_engine import get_web_engine
    from systems.captcha import CaptchaSystem
    from systems.combat import CombatSystem
    from systems.gathering import GatheringSystem
    from systems.healing import HealingSystem
    from systems.steps import StepSystem

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
        ("Captcha", captcha),
    ]

    for name, system in systems:
        try:
            if hasattr(system, "initialize"):
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
    captcha_present = await captcha.is_captcha_present()

    if captcha_present:
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
    gather_available = await gathering.is_gathering_available()

    if gather_available:
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
    combat_available = await combat.is_combat_available()

    if combat_available:
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
    health_status = await healing.check_health_status()

    if health_status.get("needs_healing", False):
        logger.info(f"❤️ Character needs healing! (HP: {health_status.get('hp_percenttage', '?')}%)")
        healing_success = await healing.perform_healing()
        if healing_success:
            logger.success("✅ Healing completed - continuing...")
            return True
        else:
            logger.warning("⚠️ Healing failed - continuing...")
    return False


async def check_and_handle_step(steps) -> bool:
    """Check and handle step taking"""
    step_available = await steps.is_step_available()

    if step_available:
        logger.debug("👣 Step available - taking step to trigger new event...")
        step_taken = await steps.take_step(fast_mode=True)  # Use fast mode for automation
        if step_taken:
            logger.info("✅ Step taken - checking for new events...")
            return True
        else:
            logger.warning("⚠️ Step failed - continuing...")
    # Note: Removed the else clause that logged "Step not available"
    # This reduces spam and allows continuous checking of other opportunities
    return False


async def _check_navigation_if_needed(web_engine, steps) -> None:
    """Check if we need to navigate to travel page if we're not on a game page"""
    try:
        page = await web_engine.get_page()
        if page:
            current_url = page.url
            if not current_url or "simple-mmo.com" not in current_url:
                logger.debug("🗺️ Not on game page - navigating to travel page...")
                await steps.navigate_to_travel()
                await asyncio.sleep(1)  # Brief wait after navigation
    except Exception as e:
        logger.debug(f"Navigation check failed: {e}")


async def _cleanup_systems(web_engine) -> None:
    """Clean up systems before exit"""
    try:
        logger.info("🧹 Cleaning up systems...")
        if web_engine:
            await web_engine.shutdown()
        logger.success("✅ Cleanup complete")
    except Exception as e:
        logger.warning(f"⚠️ Cleanup warning (non-critical): {e}")


async def run_bot_loop(web_engine, gathering, healing, steps, combat, captcha) -> None:
    """Main bot automation loop"""
    logger.info("🚀 Starting bot automation loop...")

    # Keep track of cycles for reduced logging
    cycles = 0
    last_cycle_log = 0

    try:
        while True:
            cycles += 1

            # Every 50 cycles, show a status update (reduced frequency)
            if cycles % CYCLE_LOG_INTERVAL == 1 or cycles - last_cycle_log >= CYCLE_LOG_INTERVAL:
                logger.info(f"🔄 Cycle {cycles} - Scanning for opportunities...")
                last_cycle_log = cycles

                # Add detailed status for debugging (even less frequent)
                if cycles % 100 == 1:  # Every 100 cycles, show detailed status
                    try:
                        page = await web_engine.get_page()
                        if page:
                            url = page.url
                            title = await page.title()
                            logger.info(f"📍 Current URL: {url}")
                            logger.info(f"📄 Page title: {title}")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not get page info: {e}")

            # Check for captcha first (highest priority)
            captcha_handled = await check_and_handle_captcha(captcha)
            if captcha_handled:  # If captcha was resolved, continue to next iteration
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

            # If step not available, don't wait - just continue checking other things
            # This ensures we keep detecting gathering, combat, etc. while waiting for steps

            # Check if we need to navigate to travel page (much less frequently)
            if cycles % NAVIGATION_CHECK_INTERVAL == 0:  # Every 500 cycles (about every 50 seconds)
                await _check_navigation_if_needed(web_engine, steps)

            # Optimized delay - longer since opportunities are usually detected within 2s
            await asyncio.sleep(MAIN_LOOP_DELAY)

    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Unexpected error in bot loop: {e}")
    finally:
        await _cleanup_systems(web_engine)


async def run_bot(config: "BotConfig") -> None:
    """
    Main bot execution function.

    Args:
        config: Bot configuration dictionary
    """
    logger.info("🤖 Starting SimpleMMO Bot - Modern Edition")
    logger.info("⚙️ Configuration loaded")

    # Initialize all systems
    systems = await initialize_systems(config)
    if not systems:
        logger.error("❌ Failed to initialize systems")
        return

    web_engine, gathering, healing, steps, combat, captcha = systems

    # Run the main bot loop
    await run_bot_loop(web_engine, gathering, healing, steps, combat, captcha)
