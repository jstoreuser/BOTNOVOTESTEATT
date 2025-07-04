"""
👣 Step/Movement System for SimpleMMO Bot

Advanced movement automation using Playwright:
- Smart step detection based on original step.py
- Efficient movement patterns with human-like timing
- Navigation optimization and fallback mechanisms
- Anti-detection measures and multiple detection strategies

Modernized version of the original step.py using Playwright instead of Selenium
"""

from __future__ import annotations

import asyncio
import random
from typing import Any

from loguru import logger

# Constants for magic values
DISABLED_BUTTON_LOG_INTERVAL = 30  # seconds
MISSING_BUTTON_LOG_INTERVAL = 15  # seconds
DEFAULT_STEP_TIMEOUT = 60.0  # seconds
MAX_STEP_ATTEMPTS = 3
POST_STEP_DELAY_RANGE = (0.5, 1.5)  # seconds

# Robust import mechanism for both direct execution and module import
try:
    from ..automation.web_engine import get_web_engine
except ImportError:
    try:
        from automation.web_engine import get_web_engine
    except ImportError:
        from src.automation.web_engine import get_web_engine


class StepSystem:
    """
    👣 Advanced Step/Movement System

    Features:
    - Intelligent step detection (multiple XPath strategies)
    - Optimized movement patterns with human-like delays
    - Navigation management and travel page handling
    - Fallback mechanisms for reliability
    - Performance tracking and statistics
    """

    def __init__(self, config: dict[str, Any]):
        """Initialize Step System"""
        self.config = config
        self.web_engine = None
        self.step_stats = {
            "steps_taken": 0,
            "successful_steps": 0,
            "failed_steps": 0,
            "total_time": 0.0,
            "average_delay": 0.0,
        }

        # Step timing configuration (human-like patterns)
        self.step_delay_min = config.get("step_delay_min", 1.0)
        self.step_delay_max = config.get("step_delay_max", 3.0)
        self.fast_step_delay_min = 0.2
        self.fast_step_delay_max = 0.7

        # Detection strategies (from original step.py)
        self.step_selectors = [
            # Primary button selectors
            "button:has-text('Take a step')",
            "button:text('Take a step')",
            "button:contains('Take a step')",
            "button:contains('step')",
            # Input button selectors
            "input[type='submit'][value*='Take a step']",
            "input[type='button'][value*='Take a step']",
            # Link selectors (fallback)
            "a:has-text('Take a step')",
            "a:contains('Take a step')",
            "a:text('Take a step')",
            "a:contains('step')",
            # Generic selectors
            "[onclick*='step']",
            ".step-button",
            "#step-btn",
        ]

        logger.info("👣 Step System initialized with modern Playwright")

    def _ensure_web_engine_available(self) -> None:
        """Ensure web engine is available, raise if not"""
        if not self.web_engine:
            raise RuntimeError("Web engine not available")

    async def initialize(self) -> bool:
        """Initialize step system"""
        try:
            self.web_engine = await get_web_engine()
            self._ensure_web_engine_available()

            logger.success("👣 Step System ready")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to initialize Step System: {e}")
            return False

    async def is_step_available(self) -> bool:
        """Check if step is available on current page - Ultra-fast detection"""
        if not self.web_engine or not self.web_engine.page:
            return False

        try:
            # Use the fastest selector first
            element = await self.web_engine.page.query_selector("button:has-text('Take a step')")
            if element:
                is_visible = await element.is_visible()
                is_enabled = await element.is_enabled()
                return is_visible and is_enabled

            # Quick fallback check
            element = await self.web_engine.page.query_selector("a:has-text('Take a step')")
            if element:
                is_visible = await element.is_visible()
                is_enabled = await element.is_enabled()
                return is_visible and is_enabled
            else:
                return False
        except Exception as e:
            logger.debug(f"Error checking step availability: {e}")
            return False

    async def _check_button_disabled_styling(self, element) -> bool:
        """Check if button has disabled styling"""
        classes = await element.get_attribute("class") or ""
        style = await element.get_attribute("style") or ""

        # Check for common disabled indicators
        is_disabled_by_class = "disabled" in classes.lower() or "opacity-40" in classes
        is_disabled_by_style = "opacity: 0.4" in style or "opacity:0.4" in style

        return is_disabled_by_class or is_disabled_by_style

    async def _check_button_availability(self) -> tuple[bool, bool, bool]:
        """Check button availability and state

        Returns:
            (button_found, is_fully_available, is_disabled_by_styling)
        """
        # Try button first
        element = await self.web_engine.page.query_selector("button:has-text('Take a step')")
        if not element:
            # Try link fallback
            element = await self.web_engine.page.query_selector("a:has-text('Take a step')")

        if not element:
            return False, False, False

        is_visible = await element.is_visible()
        is_enabled = await element.is_enabled()

        if not (is_visible and is_enabled):
            return True, False, False

        is_disabled_by_styling = await self._check_button_disabled_styling(element)
        is_fully_available = not is_disabled_by_styling

        return True, is_fully_available, is_disabled_by_styling

    async def _handle_disabled_button_wait(self, start_time: float, last_log_time: float) -> float:
        """Handle waiting when button is disabled"""
        elapsed = asyncio.get_event_loop().time() - start_time
        if elapsed - last_log_time >= DISABLED_BUTTON_LOG_INTERVAL:
            logger.info(f"⏳ Step button disabled for {elapsed:.1f}s - waiting patiently...")
            return elapsed
        return last_log_time

    async def _handle_missing_button_wait(self, start_time: float, last_log_time: float, timeout: float) -> tuple[bool, float]:
        """Handle waiting when button is missing

        Returns:
            (should_continue, new_last_log_time)
        """
        elapsed = asyncio.get_event_loop().time() - start_time

        # If button has never been found and timeout exceeded, give up
        if elapsed > timeout:
            logger.warning(f"⏰ Step button not found after {timeout}s timeout")
            return False, last_log_time

        # Reduced logging frequency for missing button
        if elapsed - last_log_time >= MISSING_BUTTON_LOG_INTERVAL:
            logger.debug(f"⏳ Searching for step button... ({elapsed:.1f}s)")
            return True, elapsed

        return True, last_log_time

    async def wait_for_step_button(self, timeout: float = DEFAULT_STEP_TIMEOUT) -> bool:
        """
        Wait for step button to become available (enabled) - INDEFINITE WAITING MODE

        This method waits for the 'Take a step' button to be both visible and enabled.
        It will wait indefinitely while the button exists but is disabled (opacity styling).
        Only returns False if the button completely disappears or there's an error.

        Args:
            timeout: Maximum time to wait if button is completely missing

        Returns:
            True if button becomes available, False only if button disappears or error
        """
        if not self.web_engine or not self.web_engine.page:
            return False

        try:
            logger.debug("⏳ Waiting for step button to become available (will wait indefinitely while disabled)...")

            start_time = asyncio.get_event_loop().time()
            last_log_time = 0  # Track when we last logged to reduce spam

            while True:
                button_found, is_fully_available, is_disabled_by_styling = await self._check_button_availability()

                if button_found:

                    if is_fully_available:
                        logger.success("✅ Step button is available and enabled!")
                        return True
                    elif is_disabled_by_styling:
                        # Button exists but is disabled - wait indefinitely (reduced logging)
                        last_log_time = await self._handle_disabled_button_wait(start_time, last_log_time)
                    # Removed the debug log for "not visible/enabled" to reduce spam
                else:
                    # Button not found
                    should_continue, last_log_time = await self._handle_missing_button_wait(
                        start_time, last_log_time, timeout
                    )
                    if not should_continue:
                        return False

                # Wait a bit before checking again (optimized for responsiveness)
                await asyncio.sleep(0.2)

        except Exception as e:
            logger.error(f"❌ Error waiting for step button: {e}")
            return False

    async def take_step(self, fast_mode: bool = False) -> bool:
        """
        Take a step - Main function with intelligent waiting

        This is the main entry point for taking steps. It includes smart waiting
        logic to handle temporarily disabled buttons.

        Args:
            fast_mode: If True, use minimal delays (for rapid navigation)
        """
        if not self.web_engine or not self.web_engine.page:
            logger.warning("👣 Web engine not available for step")
            return False

        try:
            logger.info("👣 Attempting to take step with smart waiting...")

            # Quick check first
            if await self.is_step_available():
                logger.debug("👣 Step immediately available")
                return await self._take_step_internal(fast_mode)

            # If not available, check if we're on a page that might have steps
            url = self.web_engine.page.url
            if "travel" in url.lower() or "simple-mmo.com" in url:
                logger.info("⏳ Step not immediately available, waiting for button...")

                # Wait for step button to become available (indefinitely if disabled)
                if await self.wait_for_step_button(timeout=60.0):  # 60s timeout only for missing buttons
                    logger.success("✅ Step button became available!")
                    return await self._take_step_internal(fast_mode)
                else:
                    logger.warning("⏰ Step button not found after extensive wait, may need to navigate")
                    return False
            else:
                logger.debug("📍 Not on a game page, step not expected")
                return False

        except Exception as e:
            logger.error(f"❌ Error in take_step: {e}")
            return False

    async def _take_step_internal(self, fast_mode: bool = False) -> bool:
        """
        Take a step - Main function with multiple strategies

        Args:
            fast_mode: If True, use minimal delays (for rapid navigation)
        """
        if not self.web_engine or not self.web_engine.page:
            logger.warning("👣 Web engine not available for step")
            return False

        try:
            logger.debug("👣 Attempting to take step...")  # Changed from info to debug
            self.step_stats["steps_taken"] += 1

            # Strategy 1: Fast step (optimized)
            if await self._take_step_fast():
                return await self._finalize_step_success(fast_mode)

            # Strategy 2: Comprehensive search (fallback)
            if await self._take_step_comprehensive():
                return await self._finalize_step_success(fast_mode)

            # Strategy 3: Original-style detection (last resort)
            if await self._take_step_original_style():
                return await self._finalize_step_success(fast_mode)

            # No step available
            logger.debug("👣 No step available")
            self.step_stats["failed_steps"] += 1
            return False

        except Exception as e:
            logger.error(f"❌ Error taking step: {e}")
            self.step_stats["failed_steps"] += 1
            return False

    async def _take_step_fast(self) -> bool:
        """Fast step taking - optimized for speed"""
        try:
            # Primary fast selectors
            fast_selectors = [
                "button:has-text('Take a step')",
                "button:contains('Take a step')",
                "a:has-text('Take a step')",
            ]

            for selector in fast_selectors:
                try:
                    element = await self.web_engine.page.query_selector(selector)
                    if element:
                        is_visible = await element.is_visible()
                        is_enabled = await element.is_enabled()

                        if is_visible and is_enabled:
                            # Minimal delay for human-like behavior
                            delay = random.uniform(
                                self.fast_step_delay_min, self.fast_step_delay_max
                            )
                            await asyncio.sleep(delay)

                            await element.click()
                            # Removed debug log for successful fast step to reduce spam
                            return True

                except Exception:
                    # Removed debug log for failed selectors to reduce spam
                    continue

            return False

        except Exception as e:
            logger.debug(f"Fast step strategy failed: {e}")
            return False

    async def _take_step_comprehensive(self) -> bool:
        """Comprehensive step detection - tries all selectors"""
        try:
            logger.debug("👣 Using comprehensive step detection...")

            for i, selector in enumerate(self.step_selectors):
                try:
                    element = await self.web_engine.page.query_selector(selector)
                    if element:
                        is_visible = await element.is_visible()
                        is_enabled = await element.is_enabled()

                        if is_visible and is_enabled:
                            # Get element text for logging
                            try:
                                text = await element.inner_text()
                                text = text.strip()[:30] if text else "N/A"
                            except Exception:
                                text = "N/A"

                            logger.debug(f"👣 Found step element {i+1}: '{text}' using {selector}")

                            # Human-like delay
                            delay = random.uniform(self.step_delay_min, self.step_delay_max)
                            await asyncio.sleep(delay)

                            await element.click()
                            logger.info(f"👣 Step taken using comprehensive selector: {selector}")
                            return True

                except Exception as e:
                    logger.debug(f"Comprehensive selector {selector} failed: {e}")
                    continue

            return False

        except Exception as e:
            logger.debug(f"Comprehensive step strategy failed: {e}")
            return False

    async def _take_step_original_style(self) -> bool:
        """Original step.py style detection - multiple elements check"""
        try:
            logger.debug("👣 Using original-style step detection...")

            # Get all potential step elements
            buttons = await self.web_engine.page.query_selector_all(
                "button:has-text('Take a step')"
            )
            links = await self.web_engine.page.query_selector_all("a:has-text('Take a step')")

            all_elements = buttons + links
            logger.debug(f"👣 Found {len(all_elements)} potential step elements")

            # Check only first 3 elements (like original)
            for i, element in enumerate(all_elements[:3]):
                try:
                    is_visible = await element.is_visible()
                    is_enabled = await element.is_enabled()

                    try:
                        text = await element.inner_text()
                        text = text.strip()[:20] if text else "N/A"
                    except Exception:
                        text = "N/A"

                    logger.debug(
                        f"👣 Element {i+1}: '{text}' (visible: {is_visible}, enabled: {is_enabled})"
                    )

                    if is_visible and is_enabled:
                        # Original-style delay
                        delay = random.uniform(1.5, 2.5)
                        logger.debug(f"👣 Waiting {delay:.2f}s before click (original style)")
                        await asyncio.sleep(delay)

                        await element.click()
                        logger.info("👣 Step taken using original-style detection")
                        return True
                    else:
                        logger.debug(f"👣 Element {i+1} not available for click")

                except Exception as e:
                    logger.debug(f"Error checking element {i+1}: {e}")
                    continue

            return False

        except Exception as e:
            logger.debug(f"Original-style step strategy failed: {e}")
            return False

    async def _finalize_step_success(self, fast_mode: bool) -> bool:
        """Finalize successful step"""
        try:
            self.step_stats["successful_steps"] += 1

            logger.success("👣 Step completed successfully")

            # Post-step delay (unless in fast mode)
            if not fast_mode:
                post_delay = random.uniform(0.5, 1.5)
                await asyncio.sleep(post_delay)

            return True

        except Exception as e:
            logger.debug(f"Error finalizing step: {e}")
            return True  # Still consider it successful

    async def navigate_to_travel(self) -> bool:
        """Navigate to travel page (from original navegar_para_travel)"""
        if not self.web_engine or not self.web_engine.page:
            logger.warning("👣 Web engine not available for navigation")
            return False

        try:
            logger.info("🧭 Navigating to travel page...")

            travel_url = self.config.get("travel_url", "https://web.simple-mmo.com/travel")
            await self.web_engine.page.goto(travel_url)

            # Wait for page to load
            await asyncio.sleep(2.0)

            # Verify we're on travel page
            if await self.is_on_travel_page():
                logger.success("🧭 Successfully navigated to travel page")
                return True
            else:
                logger.warning("⚠️ Navigation completed but not on travel page")
                return False

        except Exception as e:
            logger.error(f"❌ Error navigating to travel: {e}")
            return False

    async def is_on_travel_page(self) -> bool:
        """Check if we're currently on travel page"""
        if not self.web_engine or not self.web_engine.page:
            return False

        try:
            url = self.web_engine.page.url
            return "travel" in url.lower()

        except Exception as e:
            logger.debug(f"Error checking travel page: {e}")
            return False

    async def get_available_actions(self) -> dict[str, bool]:
        """Get all available actions on current page"""
        try:
            actions = {
                "step": await self.is_step_available(),
                "gather": False,  # Will be implemented by gathering system
                "fight": False,  # Will be implemented by combat system
                "heal": False,  # Will be implemented by healing system
            }

            return actions

        except Exception as e:
            logger.debug(f"Error getting available actions: {e}")
            return {"step": False, "gather": False, "fight": False, "heal": False}

    def get_step_stats(self) -> dict[str, Any]:
        """Get step statistics"""
        try:
            success_rate = 0.0
            if self.step_stats["steps_taken"] > 0:
                success_rate = (
                    self.step_stats["successful_steps"] / self.step_stats["steps_taken"]
                ) * 100

            return {
                **self.step_stats,
                "success_rate": success_rate,
                "system_ready": self.web_engine is not None,
            }

        except Exception as e:
            logger.debug(f"Error getting step stats: {e}")
            return {"error": str(e)}

    # === COMPATIBILITY FUNCTIONS ===
    # These functions provide compatibility with the original step.py

    async def dar_step(self, fast_mode: bool = False) -> bool:
        """
        Compatibility function for original dar_step

        Args:
            fast_mode: If True, use minimal delays
        """
        return await self.take_step(fast_mode=fast_mode)

    async def tentar_passo_modular(self) -> bool:
        """Compatibility function for original tentar_passo_modular"""
        return await self.take_step(fast_mode=True)

    async def executar_step_interno(self) -> bool:
        """Compatibility function for original executar_step_interno"""
        return await self.take_step(fast_mode=True)

    async def verificar_botoes_step(self) -> int:
        """Count available step buttons (compatibility function)"""
        if not self.web_engine or not self.web_engine.page:
            return 0

        try:
            # Count all potential step elements
            buttons = await self.web_engine.page.query_selector_all(
                "button:has-text('Take a step')"
            )
            links = await self.web_engine.page.query_selector_all("a:has-text('Take a step')")

            total = len(buttons) + len(links)
            logger.debug(f"👣 Found {total} step buttons/links")
            return total

        except Exception as e:
            logger.debug(f"Error counting step buttons: {e}")
            return 0

    async def shutdown(self) -> None:
        """Shutdown step system"""
        logger.info("👣 Shutting down Step System...")

        # Log final statistics
        stats = self.get_step_stats()
        logger.info(f"👣 Final step statistics: {stats}")


# === GLOBAL FUNCTIONS FOR COMPATIBILITY ===


async def take_step() -> bool:
    """Global function for taking a step"""
    try:
        # This would need to be implemented in context system
        logger.debug("Global take_step function called")
        return False
    except Exception as e:
        logger.error(f"❌ Error in global take_step: {e}")
        return False
