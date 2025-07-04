"""
🌐 Web Automation Engine for SimpleMMO Bot
            # If no existing browser, warn user
            logger.warning("⚠️ No existing browser found!")
            logger.info("🔧 Please run demo_bot_completo.py first to start browser with Profile 1")
            logger.info("💡 Or manually start Chromium with your profile")
        else:
            # Don't start new browser to avoid profile conflicts
            return Falsen web automation using Playwright (replaces Selenium completely).
Simplified and clean implementation for better maintainability.
"""

import subprocess
import time
from pathlib import Path
from typing import Any

from loguru import logger
from playwright.async_api import Browser, BrowserContext, Page, Playwright, async_playwright


class WebAutomationEngine:
    """Modern Web Automation Engine using Playwright"""

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize Web Automation Engine"""
        self.config = config or {}
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self.is_initialized = False

        # Configuration with defaults
        self.browser_headless = self.config.get("browser_headless", False)
        self.browser_type = self.config.get("browser_type", "chromium")
        self.debugging_port = self.config.get("debugging_port", 9222)
        self.user_data_dir = self.config.get("user_data_dir", r"C:\temp\playwright_profile")
        self.target_url = self.config.get("target_url", "https://web.simple-mmo.com/travel")

        logger.info("🌐 Web Automation Engine created (Playwright)")

    async def initialize(self) -> bool:
        """Initialize Playwright browser"""
        try:
            logger.info("🌐 Initializing Playwright browser...")

            # ALWAYS try to connect to existing browser first (Profile 1)
            logger.info("🔗 Prioritizing connection to existing browser with saved profile...")
            if await self._connect_to_existing_browser():
                logger.success("✅ Connected to existing browser with your saved profile!")
                self.is_initialized = True
                return True

            # If no existing browser, warn user
            logger.warning("⚠️ No existing browser found!")
            logger.info("� Please run demo_bot_completo.py first to start browser with Profile 1")
            logger.info("💡 Or manually start Chromium with your profile")

            # Don't start new browser to avoid profile conflicts
            return False

        except Exception as e:
            logger.error(f"❌ Failed to initialize browser: {e}")
            await self.cleanup()
            return False

    async def _connect_to_existing_browser(self) -> bool:
        """Try to connect to existing browser"""
        try:
            logger.info("🔗 Attempting to connect to existing browser on port 9222...")

            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.connect_over_cdp(
                f"http://localhost:{self.debugging_port}"
            )

            # Get existing context or create new one
            contexts = self.browser.contexts
            if contexts:
                self.context = contexts[0]
                pages = self.context.pages
                self.page = pages[0] if pages else await self.context.new_page()

                # Log current page info
                current_url = self.page.url
                page_title = await self.page.title()
                logger.success("✅ Connected to browser!")
                logger.info(f"📍 Current page: {page_title}")
                logger.info(f"🌐 Current URL: {current_url}")

            else:
                self.context = await self.browser.new_context()
                self.page = await self.context.new_page()
                logger.info("📄 Created new context and page")

            # Test if connection works
            await self.page.title()
            return True

        except Exception as e:
            logger.debug(f"Could not connect to existing browser: {e}")
            logger.info("💡 No browser running on port 9222")
            await self.cleanup()
            return False

    async def _start_new_browser(self) -> bool:
        """Start a new browser instance"""
        try:
            # Start Playwright
            self.playwright = await async_playwright().start()

            # Launch browser with simplified settings
            self.browser = await self.playwright.chromium.launch(
                headless=self.browser_headless,
                args=[
                    "--no-first-run",
                    "--no-default-browser-check",
                ],
            )

            # Create context with stealth settings
            self.context = await self.browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            )

            # Create page
            self.page = await self.context.new_page()

            # Navigate to target URL
            await self.page.goto(self.target_url)
            await self.page.wait_for_load_state("networkidle")

            self.is_initialized = True
            logger.success("✅ Playwright browser initialized successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to start new browser: {e}")
            await self.cleanup()
            return False

    async def get_page(self) -> Page | None:
        """Get current page instance"""
        if self.page:
            try:
                # Test if page is still valid
                await self.page.title()
                return self.page
            except Exception:
                logger.warning("Current page invalid, cleaning reference")
                self.page = None

        return self.page

    async def get_context(self) -> BrowserContext | None:
        """Get current browser context for tab management"""
        if self.context:
            try:
                # Test if context is still valid
                return self.context
            except Exception:
                logger.warning("Current context invalid, cleaning reference")
                self.context = None

        return self.context

    async def is_page_valid(self) -> bool:
        """Check if page is valid"""
        page = await self.get_page()
        if not page:
            return False

        try:
            _ = page.url  # page.url is a property, not a method
            return True
        except Exception:
            return False

    async def navigate_to(self, url: str) -> bool:
        """Navigate to URL"""
        page = await self.get_page()
        if not page:
            return False

        try:
            await page.goto(url)
            await page.wait_for_load_state("networkidle")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to navigate to {url}: {e}")
            return False

    async def url_starts_with(self, prefix: str) -> bool:
        """Check if current URL starts with prefix"""
        page = await self.get_page()
        if not page:
            return False

        try:
            current_url = page.url
            return current_url.startswith(prefix)
        except Exception:
            return False

    async def find_element(self, selector: str) -> Any | None:
        """Find element by selector"""
        page = await self.get_page()
        if not page:
            return None

        try:
            return await page.query_selector(selector)
        except Exception:
            return None

    async def find_elements(self, selector: str) -> list[Any]:
        """Find multiple elements by selector"""
        page = await self.get_page()
        if not page:
            return []

        try:
            return await page.query_selector_all(selector)
        except Exception:
            return []

    async def click_element(self, element_or_selector: Any | str, timeout: float = 5000) -> bool:
        """Click element"""
        page = await self.get_page()
        if not page:
            return False

        try:
            if isinstance(element_or_selector, str):
                # Wait for element and click
                await page.click(element_or_selector, timeout=timeout)
            else:
                # Element object
                await element_or_selector.click(timeout=timeout)

            return True
        except Exception as e:
            logger.debug(f"Failed to click element: {e}")
            return False

    def _get_selectors_for_text(self, text: str) -> list[str]:
        """Get appropriate selectors for the given text"""
        if "Take a step" in text:
            return [
                f'button:has-text("{text}")',
                f'a:has-text("{text}")',
                '[onclick*="step"]',
            ]
        else:
            return [
                f'button:has-text("{text}")',
                f'a:has-text("{text}")',
                f'input[value="{text}"]',
            ]

    async def _find_all_valid_elements(self, page: Page, selectors: list[str]) -> list[Any]:
        """Find all valid (visible and enabled) elements"""
        for selector in selectors:
            elements = await page.query_selector_all(selector)
            if elements:
                # Filter visible and enabled elements
                valid_elements = []
                for elem in elements[:3]:  # Limit to first 3 for performance
                    try:
                        if await elem.is_visible() and await elem.is_enabled():
                            valid_elements.append(elem)
                    except Exception:
                        continue
                if valid_elements:
                    return valid_elements
        return []

    async def _find_single_valid_element(self, page: Page, selectors: list[str]) -> Any | None:
        """Find single valid (visible and enabled) element"""
        for selector in selectors:
            element = await page.query_selector(selector)
            if element:
                try:
                    if await element.is_visible() and await element.is_enabled():
                        return element
                except Exception:
                    continue
        return None

    async def find_button_by_text(self, text: str, get_all: bool = False) -> Any | None | list[Any]:
        """Find button by text"""
        page = await self.get_page()
        if not page:
            return None if not get_all else []

        try:
            selectors = self._get_selectors_for_text(text)

            if get_all:
                valid_elements = await self._find_all_valid_elements(page, selectors)
                return valid_elements if valid_elements else []
            else:
                element = await self._find_single_valid_element(page, selectors)
                return element if element else None

        except Exception:
            return None if not get_all else []

    async def is_element_visible(self, selector: str) -> bool:
        """Check if element is visible"""
        page = await self.get_page()
        if not page:
            return False

        try:
            element = await page.query_selector(selector)
            if element:
                return await element.is_visible()
            return False
        except Exception:
            return False

    async def cleanup(self) -> None:
        """Cleanup resources"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            logger.debug(f"Error during cleanup: {e}")
        finally:
            self.page = None
            self.context = None
            self.browser = None
            self.playwright = None

    async def shutdown(self) -> None:
        """Shutdown browser"""
        logger.info("🌐 Shutting down Web Automation Engine...")
        await self.cleanup()
        self.is_initialized = False
        logger.success("✅ Web Automation Engine shutdown complete")


class WebEngineManager:
    """Singleton manager for web engine"""
    _instance: WebAutomationEngine | None = None

    @classmethod
    async def get_instance(cls) -> WebAutomationEngine:
        """Get or create web engine instance"""
        if cls._instance is None:
            config = {"browser_headless": False, "target_url": "https://web.simple-mmo.com/travel"}
            cls._instance = WebAutomationEngine(config)
            await cls._instance.initialize()
        return cls._instance

    @classmethod
    async def shutdown(cls) -> None:
        """Shutdown the web engine instance"""
        if cls._instance:
            await cls._instance.shutdown()
            cls._instance = None


async def get_web_engine() -> WebAutomationEngine:
    """Get or create global web engine instance"""
    return await WebEngineManager.get_instance()


async def get_page() -> Page | None:
    """Get current page"""
    engine = await get_web_engine()
    return await engine.get_page()


async def navigate_to_travel() -> bool:
    """Navigate to travel page"""
    engine = await get_web_engine()
    return await engine.navigate_to("https://web.simple-mmo.com/travel")


def open_brave_browser() -> bool:
    """Open Brave browser with debugging"""
    try:
        brave_path = Path(r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe")

        if not brave_path.exists():
            logger.error(f"Brave browser not found at: {brave_path}")
            return False

        command = [
            str(brave_path),
            "--remote-debugging-port=9222",
            "--user-data-dir=C:\\temp\\brave_profile",
            "https://web.simple-mmo.com/travel",
        ]

        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        time.sleep(3)
        logger.info("✅ Brave browser started with debugging enabled")
        return True

    except Exception as e:
        logger.error(f"❌ Error opening Brave browser: {e}")
        return False


async def shutdown_global_engine() -> None:
    """Shutdown global engine"""
    await WebEngineManager.shutdown()
