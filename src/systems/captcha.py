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
        """Check if captcha button is present on current page"""
        try:
            engine = await get_web_engine()
            page = await engine.get_page()

            if not page:
                return False

            # Look for the specific captcha button
            captcha_selectors = [
                'a[href="/i-am-not-a-bot?new_page=true"]',
                'a:has-text("I\'m a person! Promise!")',
                '//a[contains(text(), "I\'m a person!")]',
                '//a[contains(@href, "i-am-not-a-bot")]',
            ]

            for selector in captcha_selectors:
                try:
                    if selector.startswith("//"):
                        # XPath selector
                        element = await page.query_selector(f"xpath={selector}")
                    else:
                        # CSS selector
                        element = await page.query_selector(selector)

                    if element and await element.is_visible():
                        logger.debug(f"🔒 Captcha button found using selector: {selector}")
                        return True
                except Exception as e:
                    logger.debug(f"Captcha selector {selector} failed: {e}")
                    continue

            return False

        except Exception as e:
            logger.debug(f"Error checking captcha: {e}")
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
                        logger.info(f"⏳ Still waiting for captcha resolution... ({elapsed:.0f}s elapsed)")

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
