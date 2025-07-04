"""
🩺 Healing System for SimpleMMO Bot

Modern healing system using Playwright.
Based on the original Selenium implementation but updated for modern web automation.
"""

from typing import Any

from loguru import logger

# Robust import mechanism for both direct execution and module import
try:
    from ..automation.web_engine import get_web_engine
except ImportError:
    try:
        from automation.web_engine import get_web_engine
    except ImportError:
        from src.automation.web_engine import get_web_engine


class HealingSystem:
    """Modern healing system for SimpleMMO Bot"""

    def __init__(self, config: dict[str, Any]):
        """Initialize Healing System"""
        self.config = config
        self.is_initialized = False
        self.auto_heal = config.get("auto_heal", True)
        logger.info("🩺 Healing System created")

    async def initialize(self) -> bool:
        """Initialize healing system"""
        try:
            self.is_initialized = True
            logger.success("✅ Healing System initialized")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to initialize Healing System: {e}")
            return False

    async def check_health_status(self) -> dict[str, Any]:
        """Check current health status"""
        try:
            engine = await get_web_engine()
            page = await engine.get_page()

            if not page:
                return {"is_dead": False, "hp_percentage": 100}

            # Check if character is dead
            is_dead = await self._is_character_dead(page)

            return {
                "is_dead": is_dead,
                "hp_percentage": 0 if is_dead else 100,  # Simplified for now
                "needs_healing": is_dead,
            }

        except Exception as e:
            logger.debug(f"Error checking health status: {e}")
            return {"is_dead": False, "hp_percentage": 100}

    async def _is_character_dead(self, page) -> bool:
        """Check if character is dead"""
        try:
            # Look for death indicators
            death_selectors = [
                '//a[contains(text(), "How do I heal?")]',
                '//div[contains(text(), "You have died")]',
                '//button[contains(text(), "Heal Character")]',
            ]

            for selector in death_selectors:
                element = await page.query_selector(f"xpath={selector}")
                if element and await element.is_visible():
                    return True

            return False
        except Exception:
            return False

    async def needs_healing(self, health_info: dict[str, Any]) -> bool:
        """Determine if healing is needed"""
        if not self.auto_heal:
            return False

        return health_info.get("is_dead", False) or health_info.get("needs_healing", False)

    async def perform_healing(self) -> bool:
        """Perform healing action"""
        try:
            if not self.auto_heal:
                logger.info("Auto-heal disabled, skipping")
                return False

            logger.info("💊 Performing healing...")

            engine = await get_web_engine()
            page = await engine.get_page()

            if not page:
                return False

            # Navigate to healer
            await page.goto("https://web.simple-mmo.com/healer?new_page_refresh=true")
            await page.wait_for_load_state("networkidle")

            # Look for heal button
            heal_button = await page.query_selector('button:has-text("Heal Character")')

            if heal_button and await heal_button.is_visible():
                await heal_button.click()
                await page.wait_for_load_state("networkidle")

                # Navigate back to travel
                await page.goto("https://web.simple-mmo.com/travel")
                await page.wait_for_load_state("networkidle")

                logger.success("✅ Healing completed successfully")
                return True
            else:
                logger.warning("⚠️ Heal button not found")
                return False

        except Exception as e:
            logger.error(f"❌ Error during healing: {e}")
            return False

    async def get_healing_cost(self) -> int:
        """Get cost of healing (for future implementation)"""
        return 0  # Placeholder

    async def can_afford_healing(self) -> bool:
        """Check if player can afford healing (for future implementation)"""
        return True  # Placeholder
