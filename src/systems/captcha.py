"""
🔒 Captcha Detection and Resolution System for SimpleMMO Bot

Modern captcha detection using Playwright with automatic tab management.
Handles the "I'm a person! Promise!" captcha flow:
1. Detects captcha button
2. Opens captcha in new tab
3. Waits for user to solve manually
4. Detects success popup
5. Closes captcha tab and resumes bot
"""

import asyncio
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


class CaptchaSystem:
    """Modern captcha detection and handling system with tab management"""

    def __init__(self, config: dict[str, Any]):
        """Initialize Captcha System"""
        self.config = config
        self.is_initialized = False
        self.captcha_tab = None
        self.main_tab = None
        logger.info("🔒 Captcha System created")

    async def initialize(self) -> bool:
        """Initialize captcha system"""
        try:
            self.is_initialized = True
            logger.success("✅ Captcha System initialized")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to initialize Captcha System: {e}")
            return False

    async def is_captcha_present(self) -> bool:
        """Check if any type of captcha is present on current page"""
        try:
            # Check for regular travel page captcha
            if await self._is_travel_captcha_present():
                return True

            # Check for combat page captcha
            if await self._is_combat_captcha_present():
                return True

            return False

        except Exception as e:
            logger.debug(f"Error checking captcha: {e}")
            return False

    async def _is_travel_captcha_present(self) -> bool:
        """Check if travel page captcha button is present"""
        try:
            engine = await get_web_engine()
            page = await engine.get_page()

            if not page:
                return False

            # Look for the regular travel captcha button
            captcha_selectors = [
                'a[href="/i-am-not-a-bot?new_page=true"]',
                'a:has-text("I\'m a person! Promise!")',
                '//a[contains(text(), "I\'m a person!")]',
                '//a[contains(@href, "i-am-not-a-bot")]',
            ]

            for selector in captcha_selectors:
                try:
                    if selector.startswith("//"):
                        element = await page.query_selector(f"xpath={selector}")
                    else:
                        element = await page.query_selector(selector)

                    if element and await element.is_visible():
                        logger.debug(f"🔒 Travel captcha button found using selector: {selector}")
                        return True
                except Exception as e:
                    logger.debug(f"Travel captcha selector {selector} failed: {e}")
                    continue

            return False

        except Exception as e:
            logger.debug(f"Error checking travel captcha: {e}")
            return False

    async def _is_combat_captcha_present(self) -> bool:
        """Check if combat page captcha popup is present"""
        try:
            engine = await get_web_engine()
            page = await engine.get_page()

            if not page:
                return False

            # Look for the combat captcha popup button
            combat_captcha_selectors = [
                'a[href="/i-am-not-a-bot"][class*="btn-primary"]',
                'a:has-text("Press here to verify")',
                '//a[contains(text(), "Press here to verify")]',
                '//a[@href="/i-am-not-a-bot" and contains(@class, "btn-primary")]',
                'a[href="/i-am-not-a-bot"][target="_blank"]',
            ]

            for selector in combat_captcha_selectors:
                try:
                    if selector.startswith("//"):
                        element = await page.query_selector(f"xpath={selector}")
                    else:
                        element = await page.query_selector(selector)

                    if element and await element.is_visible():
                        logger.debug(f"🔒 Combat captcha popup found using selector: {selector}")
                        return True
                except Exception as e:
                    logger.debug(f"Combat captcha selector {selector} failed: {e}")
                    continue

            return False

        except Exception as e:
            logger.debug(f"Error checking combat captcha: {e}")
            return False

    async def solve_captcha(self) -> bool:
        """Solve any type of captcha that is present"""
        try:
            # Determine captcha type and handle accordingly
            if await self._is_combat_captcha_present():
                logger.info("🔒 Combat captcha detected - using combat resolution flow")
                return await self._solve_combat_captcha()
            elif await self._is_travel_captcha_present():
                logger.info("🔒 Travel captcha detected - using travel resolution flow")
                return await self._solve_travel_captcha()
            else:
                logger.debug("🔒 No captcha detected")
                return True

        except Exception as e:
            logger.error(f"❌ Error in solve_captcha: {e}")
            return False

    async def _solve_travel_captcha(self) -> bool:
        """Solve the regular travel page captcha"""
        return await self.wait_for_resolution()

    async def _solve_combat_captcha(self) -> bool:
        """
        Solve the combat captcha popup by navigating to travel page.
        This converts the complex combat captcha to a simple travel captcha.
        """
        logger.warning("🔒 COMBAT CAPTCHA DETECTED! Navigating to travel page to simplify...")

        # Import StepSystem dynamically to avoid circular imports
        try:
            from systems.steps import StepSystem
        except ImportError:
            try:
                from src.systems.steps import StepSystem
            except ImportError:
                logger.error("❌ Could not import StepSystem for navigation")
                return False

        # Create a temporary StepSystem instance to use navigation
        temp_steps = StepSystem(self.config)
        await temp_steps.initialize()

        # Navigate to travel page
        navigation_success = await temp_steps.navigate_to_travel()

        if navigation_success:
            logger.success("✅ Navigated to travel page - captcha should now be in simple format")
            # Give a moment for the page to load
            await asyncio.sleep(2)

            # Now check if there's a travel captcha present and solve it
            if await self._is_travel_captcha_present():
                logger.info("🔒 Travel captcha detected after navigation - solving...")
                return await self._solve_travel_captcha()
            else:
                logger.success("✅ No captcha detected after navigation - continuing")
                return True
        else:
            logger.error("❌ Failed to navigate to travel page")
            return False

    async def _click_combat_captcha_button(self) -> bool:
        """Click the 'Press here to verify' button in combat popup"""
        try:
            engine = await get_web_engine()
            page = await engine.get_page()

            if not page:
                return False

            # Store reference to main tab
            self.main_tab = page

            # Find and click the combat captcha button
            combat_captcha_selectors = [
                'a[href="/i-am-not-a-bot"][target="_blank"]',
                'a:has-text("Press here to verify")',
                '//a[contains(text(), "Press here to verify")]',
                '//a[@href="/i-am-not-a-bot" and contains(@class, "btn-primary")]',
            ]

            for selector in combat_captcha_selectors:
                try:
                    if selector.startswith("//"):
                        element = await page.query_selector(f"xpath={selector}")
                    else:
                        element = await page.query_selector(selector)

                    if element and await element.is_visible():
                        logger.info("🔒 Clicking combat captcha button...")
                        await element.click()
                        await asyncio.sleep(2)  # Wait for new tab to open
                        return True

                except Exception as e:
                    logger.debug(f"Failed to click combat captcha with selector {selector}: {e}")
                    continue

            return False

        except Exception as e:
            logger.error(f"Error clicking combat captcha button: {e}")
            return False

    async def _close_combat_captcha_popup(self) -> bool:
        """Close the combat captcha popup by clicking the X button"""
        try:
            engine = await get_web_engine()
            page = await engine.get_page()

            if not page:
                return False

            # Look for the close button (X) in the popup
            close_button_selectors = [
                'path[stroke-linecap="round"][stroke-linejoin="round"][d="M6 18L18 6M6 6l12 12"]',
                'button[aria-label="Close"]',
                "button.swal2-close",
                ".swal2-close",
                '//button[contains(@aria-label, "Close")]',
                '//path[@d="M6 18L18 6M6 6l12 12"]/..',  # Parent of the path element
                '//path[@d="M6 18L18 6M6 6l12 12"]/../..',  # Grandparent of the path element
            ]

            for selector in close_button_selectors:
                try:
                    if selector.startswith("//"):
                        element = await page.query_selector(f"xpath={selector}")
                    else:
                        element = await page.query_selector(selector)

                    if element and await element.is_visible():
                        logger.info("🔒 Closing combat captcha popup...")
                        await element.click()
                        await asyncio.sleep(1)  # Wait for popup to close

                        # Verify popup is closed
                        if not await self._is_combat_captcha_present():
                            logger.success("✅ Combat captcha popup closed successfully")
                            return True

                except Exception as e:
                    logger.debug(f"Failed to close popup with selector {selector}: {e}")
                    continue

            # Alternative approach: try ESC key
            try:
                logger.debug("🔒 Trying ESC key to close popup...")
                await page.keyboard.press("Escape")
                await asyncio.sleep(1)

                if not await self._is_combat_captcha_present():
                    logger.success("✅ Combat captcha popup closed with ESC key")
                    return True
            except Exception as e:
                logger.debug(f"ESC key approach failed: {e}")

            return False

        except Exception as e:
            logger.error(f"Error closing combat captcha popup: {e}")
            return False

    async def wait_for_resolution(self, timeout: int = 600) -> bool:
        """
        Handle complete captcha resolution flow:
        1. Click the captcha button to open new tab
        2. Wait for user to solve captcha manually
        3. Detect success popup
        4. Close captcha tab and return to main tab
        """
        try:
            logger.warning("🔒 CAPTCHA DETECTED! Starting resolution process...")

            # Step 1: Click the captcha button
            if not await self._click_captcha_button():
                logger.error("❌ Failed to click captcha button")
                return False

            # Step 2: Wait for captcha tab and monitor it
            if not await self._wait_for_captcha_tab():
                logger.error("❌ Captcha tab not found")
                return False

            # Step 3: Wait for user to solve captcha (monitor success popup)
            logger.info("🧑‍💻 Please solve the captcha manually in the new tab...")
            if not await self._wait_for_captcha_success(timeout):
                logger.error("❌ Captcha resolution timeout or failed")
                return False

            # Step 4: Close captcha tab and return to main tab
            await self._close_captcha_tab_and_return()

            logger.success("✅ Captcha resolved successfully! Resuming bot...")
            return True

        except Exception as e:
            logger.error(f"❌ Error in captcha resolution: {e}")
            return False

    async def _click_captcha_button(self) -> bool:
        """Click the captcha button to open new tab"""
        try:
            engine = await get_web_engine()
            page = await engine.get_page()

            if not page:
                return False

            # Store reference to main tab
            self.main_tab = page

            # Find and click the captcha button
            captcha_selectors = [
                'a[href="/i-am-not-a-bot?new_page=true"]',
                'a:has-text("I\'m a person! Promise!")',
                '//a[contains(@href, "i-am-not-a-bot")]',
            ]

            for selector in captcha_selectors:
                try:
                    if selector.startswith("//"):
                        element = await page.query_selector(f"xpath={selector}")
                    else:
                        element = await page.query_selector(selector)

                    if element and await element.is_visible():
                        logger.info("🔒 Clicking captcha button...")
                        await element.click()
                        await asyncio.sleep(1)  # Wait for new tab to open
                        return True

                except Exception as e:
                    logger.debug(f"Failed to click with selector {selector}: {e}")
                    continue

            return False

        except Exception as e:
            logger.error(f"Error clicking captcha button: {e}")
            return False

    async def _wait_for_captcha_tab(self) -> bool:
        """Wait for captcha tab to open and store reference"""
        try:
            engine = await get_web_engine()
            context = await engine.get_context()

            if not context:
                return False

            # Wait for new tab to appear
            for _attempt in range(10):  # Wait up to 5 seconds
                pages = context.pages
                for page in pages:
                    if "i-am-not-a-bot" in page.url:
                        self.captcha_tab = page
                        logger.info(f"🔒 Found captcha tab: {page.url}")
                        return True

                await asyncio.sleep(0.5)

            logger.warning("⚠️ Captcha tab not found after 5 seconds")
            return False

        except Exception as e:
            logger.error(f"Error waiting for captcha tab: {e}")
            return False

    async def _wait_for_captcha_success(self, timeout: int) -> bool:
        """Wait for success popup in captcha tab"""
        try:
            if not self.captcha_tab:
                return False

            logger.info(f"⏳ Waiting for you to solve the captcha... (timeout: {timeout}s)")

            start_time = asyncio.get_event_loop().time()

            while (asyncio.get_event_loop().time() - start_time) < timeout:
                try:
                    # Check for success popup
                    success_selectors = [
                        'h2.swal2-title:has-text("Success!")',
                        '#swal2-title:has-text("Success!")',
                        '.swal2-title:has-text("Success!")',
                        '//h2[contains(text(), "Success!")]',
                    ]

                    for selector in success_selectors:
                        try:
                            if selector.startswith("//"):
                                element = await self.captcha_tab.query_selector(f"xpath={selector}")
                            else:
                                element = await self.captcha_tab.query_selector(selector)

                            if element and await element.is_visible():
                                logger.success("🎉 Success popup detected! Captcha solved!")
                                return True

                        except Exception:
                            continue

                    # Log progress every 30 seconds
                    elapsed = asyncio.get_event_loop().time() - start_time
                    if elapsed % 30 < 1:  # Log every 30s
                        logger.info(
                            f"⏳ Still waiting for captcha resolution... ({elapsed:.0f}s elapsed)"
                        )

                except Exception as e:
                    # If captcha tab is closed or error, check if we're back on main page
                    if "target closed" in str(e).lower():
                        logger.info("🔒 Captcha tab closed, checking if resolved...")
                        # Check if captcha is gone from main tab
                        if not await self.is_captcha_present():
                            return True

                await asyncio.sleep(1)  # Check every second

            return False

        except Exception as e:
            logger.error(f"Error waiting for captcha success: {e}")
            return False

    async def _close_captcha_tab_and_return(self) -> bool:
        """Close captcha tab and return focus to main tab"""
        try:
            # Close captcha tab if it exists
            if self.captcha_tab:
                try:
                    logger.info("🔒 Closing captcha tab...")
                    await self.captcha_tab.close()
                    self.captcha_tab = None
                except Exception as e:
                    logger.debug(f"Error closing captcha tab: {e}")

            # Return focus to main tab
            if self.main_tab:
                try:
                    logger.info("🔒 Returning to main tab...")
                    await self.main_tab.bring_to_front()
                    await asyncio.sleep(1)  # Give time for focus
                except Exception as e:
                    logger.debug(f"Error returning to main tab: {e}")

            # Reset references
            self.captcha_tab = None
            self.main_tab = None

            logger.success("🔒 Captcha tab closed, focus returned to main tab")
            return True

        except Exception as e:
            logger.error(f"Error managing tabs: {e}")
            return False

    async def get_captcha_info(self) -> dict[str, Any]:
        """Get information about current captcha state"""
        return {
            "present": await self.is_captcha_present(),
            "type": "i-am-not-a-bot" if await self.is_captcha_present() else "none",
            "captcha_tab_open": self.captcha_tab is not None,
            "main_tab_stored": self.main_tab is not None,
        }
