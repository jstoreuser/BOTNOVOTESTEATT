"""
🌐 Web Automation Engine for SimpleMMO Bot

Modern web automation using Playwright (replaces Selenium completely).
Simplified and clean implementation for better maintainability.
"""

import asyncio
import os
import platform
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
            logger.debug(f"🔧 Config: headless={self.browser_headless}, port={self.debugging_port}")

            # ALWAYS try to connect to existing browser first (Profile 1)
            logger.info("🔗 Prioritizing connection to existing browser with saved profile...")
            connect_result = await self._connect_to_existing_browser()

            if connect_result:
                logger.success("✅ Connected to existing browser with your saved profile!")
                # Verify connection is working
                page_check = await self.get_page()
                if page_check:
                    logger.debug(f"✅ Page validation successful: {page_check.url}")
                    self.is_initialized = True
                    return True
                else:
                    logger.warning("⚠️ Connected but page validation failed")

            logger.info("🚀 No existing browser found or connection failed, starting Chromium...")
            start_result = await self._start_chromium_with_profile()

            if start_result:
                # Wait for browser to be ready
                await self._wait_for_browser_ready()

                # Try to connect again
                connect_retry = await self._connect_to_existing_browser()
                if connect_retry:
                    # Final validation
                    page_check = await self.get_page()
                    if page_check:
                        logger.success("✅ Connected to newly started Chromium and validated!")
                        self.is_initialized = True
                        return True
                    else:
                        logger.error("❌ Connected but final page validation failed")
                        return False
                else:
                    logger.error("❌ Could not connect to newly started browser")
                    return False
            else:
                logger.error("❌ Could not start Chromium with persistent profile")
                return False

        except Exception as e:
            logger.error(f"❌ Failed to initialize browser: {e}")
            logger.exception("Full initialization error:")
            await self.cleanup()
            return False

    async def _connect_to_existing_browser(self) -> bool:
        """Try to connect to existing browser"""
        try:
            logger.info("🔗 Attempting to connect to existing browser on port 9222...")

            # Start playwright if not already started
            if not self.playwright:
                logger.debug("🎭 Starting Playwright...")
                self.playwright = await async_playwright().start()
                logger.debug("✅ Playwright started")

            # Attempt CDP connection
            logger.debug(f"🔌 Connecting to CDP endpoint: http://localhost:{self.debugging_port}")
            self.browser = await self.playwright.chromium.connect_over_cdp(
                f"http://localhost:{self.debugging_port}"
            )
            logger.debug("✅ CDP connection established")

            # Get existing context or create new one
            contexts = self.browser.contexts
            logger.debug(f"📑 Found {len(contexts)} existing contexts")

            if contexts:
                self.context = contexts[0]
                logger.debug(f"📄 Using existing context: {id(self.context)}")

                pages = self.context.pages
                logger.debug(f"📄 Found {len(pages)} pages in context")

                if pages:
                    self.page = pages[0]
                    logger.debug(f"📄 Using existing page: {id(self.page)}")
                else:
                    logger.debug("📄 No pages found, creating new page...")
                    self.page = await self.context.new_page()
                    logger.debug(f"📄 Created new page: {id(self.page)}")

                # Log current page info
                current_url = self.page.url
                page_title = await self.page.title()
                logger.success("✅ Connected to browser!")
                logger.info(f"📍 Current page: {page_title}")
                logger.info(f"🌐 Current URL: {current_url}")

                # Ensure we're on travel page
                if not current_url.endswith("/travel"):
                    logger.info("🧭 Navigating to travel page...")
                    await self.page.goto(self.target_url)
                    await self.page.wait_for_load_state("networkidle")
                    logger.success("✅ Navigation to travel page complete")

            else:
                logger.debug("📑 No existing contexts, creating new one...")
                self.context = await self.browser.new_context()
                logger.debug(f"📄 Created new context: {id(self.context)}")

                self.page = await self.context.new_page()
                logger.debug(f"📄 Created new page: {id(self.page)}")
                logger.info("📄 Created new context and page")

                # Navigate to travel page
                logger.info("🧭 Navigating to travel page...")
                await self.page.goto(self.target_url)
                await self.page.wait_for_load_state("networkidle")
                logger.success("✅ Navigation complete")

            # Test if connection works
            logger.debug("🧪 Testing page connection...")
            test_title = await self.page.title()
            logger.debug(f"✅ Page test successful: {test_title}")

            # Final state validation
            logger.debug(f"🔍 Final state - Page: {self.page is not None}, Context: {self.context is not None}")
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
                # Test if page is still valid with a very lightweight check
                # Use page.is_closed() if available, otherwise use evaluate
                if hasattr(self.page, 'is_closed') and self.page.is_closed():
                    # Only log when page actually becomes invalid
                    logger.debug("Page is closed, cleaning reference")
                    self.page = None
                    return None

                # Minimal operation to test connectivity
                _ = self.page.url  # This is a property, should be fast
                return self.page
            except Exception as e:
                # Only log when page actually becomes invalid
                logger.debug(f"Current page invalid, cleaning reference: {e}")
                self.page = None
                return None
        else:
            # Only log when there's genuinely no page available (rare case)
            if not hasattr(self, '_no_page_logged') or not self._no_page_logged:
                logger.warning("❌ No page available - page is None")
                self._no_page_logged = True
            return None

    async def get_context(self) -> BrowserContext | None:
        """Get current browser context for tab management"""
        if self.context:
            try:
                # Test if context is still valid with a lightweight check
                # Check if context is closed (if the method exists)
                if hasattr(self.context, 'pages'):
                    _ = self.context.pages  # Simple property access
                return self.context
            except Exception as e:
                logger.debug(f"Current context invalid, cleaning reference: {e}")
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
            # Check if event loop is running before cleanup
            import asyncio

            loop = asyncio.get_event_loop()
            if loop.is_closed():
                logger.debug("Event loop is closed, skipping async cleanup")
                return

            if self.page:
                try:
                    await self.page.close()
                except Exception as e:
                    logger.debug(f"Error closing page: {e}")

            if self.context:
                try:
                    await self.context.close()
                except Exception as e:
                    logger.debug(f"Error closing context: {e}")

            if self.browser:
                try:
                    await self.browser.close()
                except Exception as e:
                    logger.debug(f"Error closing browser: {e}")

            if self.playwright:
                try:
                    await self.playwright.stop()
                except Exception as e:
                    logger.debug(f"Error stopping playwright: {e}")

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

        try:
            await self.cleanup()
        except Exception as e:
            logger.debug(f"Error during shutdown cleanup: {e}")

        self.is_initialized = False
        logger.success("✅ Web Automation Engine shutdown complete")

    async def _start_chromium_with_profile(self) -> bool:
        """Start Chromium with persistent profile like demo_bot_completo.py"""
        try:
            logger.info("🔧 Starting Chromium with persistent profile...")

            # Get Chromium path from Playwright (Windows specific for now)
            system = platform.system().lower()
            if system != "windows":
                logger.error("❌ Currently only Windows is supported")
                return False

            # Try to find Playwright's Chromium
            username = os.getenv("USERNAME", "User")
            chromium_patterns = [
                rf"C:\Users\{username}\AppData\Local\ms-playwright\chromium-*\chrome-win\chrome.exe",
                rf"C:\Users\{username}\AppData\Local\ms-playwright\chromium-1179\chrome-win\chrome.exe",
            ]

            chromium_path = None
            for pattern in chromium_patterns:
                matches = list(Path().glob(pattern.replace("C:\\", "")))
                if matches:
                    chromium_path = f"C:\\{matches[0]}"
                    break

            # Fallback: try common paths
            if not chromium_path:
                common_paths = [
                    rf"C:\Users\{username}\AppData\Local\ms-playwright\chromium-1179\chrome-win\chrome.exe",
                ]
                for path in common_paths:
                    if Path(path).exists():
                        chromium_path = path
                        break

            if not chromium_path or not Path(chromium_path).exists():
                logger.error("❌ Could not find Playwright Chromium executable")
                logger.info("💡 Please run: python -m playwright install chromium")
                return False

            # Profile directory
            profile_dir = Path(chromium_path).parent / "User Data"
            profile_dir.mkdir(parents=True, exist_ok=True)

            # Command to start Chromium with debugging and profile (same as demo_bot_completo.py)
            command = [
                chromium_path,
                "--remote-debugging-port=9222",
                f"--user-data-dir={profile_dir}",
                "--profile-directory=perfilteste",
                # Stealth flags
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-extensions-except",
                "--disable-plugins-discovery",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-default-apps",
                "--disable-background-timer-throttling",
                "--disable-renderer-backgrounding",
                "--disable-backgrounding-occluded-windows",
                # Start at travel page
                "https://web.simple-mmo.com/travel",
            ]

            logger.info("🚀 Starting Chromium with perfilteste profile...")
            logger.info("📍 Opening directly at: https://web.simple-mmo.com/travel")

            # Start process in background
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
            )

            logger.success("✅ Chromium started with perfilteste profile!")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to start Chromium: {e}")
            return False

    async def _wait_for_browser_ready(self) -> None:
        """Wait for browser to be ready for connection"""
        logger.info("⏰ Waiting for browser to be ready...")
        for i in range(10):  # Wait up to 10 seconds
            try:
                # Try a quick connection test
                test_playwright = await async_playwright().start()
                try:
                    test_browser = await test_playwright.chromium.connect_over_cdp(
                        "http://localhost:9222"
                    )
                    await test_browser.close()
                    await test_playwright.stop()
                    logger.success("✅ Browser is ready!")
                    return
                except Exception:
                    await test_playwright.stop()

            except Exception:
                pass

            await asyncio.sleep(1)
            logger.debug(f"Still waiting... ({i + 1}/10)")

    async def ensure_on_travel_page(self) -> bool:
        """Ensure we're on the travel page, navigate if necessary"""
        page = await self.get_page()
        if not page:
            return False

        try:
            current_url = page.url

            # If not on travel page, navigate there
            if not current_url.endswith("/travel"):
                logger.info(f"🧭 Current page: {current_url} - navigating to travel...")
                await page.goto(self.target_url)
                await page.wait_for_load_state("networkidle")

                # Verify we're now on travel page
                new_url = page.url
                if new_url.endswith("/travel"):
                    logger.success("✅ Successfully navigated to travel page")
                    return True
                else:
                    logger.warning(f"⚠️ Navigation may have failed, current URL: {new_url}")
                    return False
            else:
                logger.debug("✅ Already on travel page")
                return True

        except Exception as e:
            logger.error(f"❌ Error ensuring travel page: {e}")
            return False

    async def navigate_to_travel(self) -> bool:
        """Navigate specifically to travel page and ensure we stay there"""
        return await self.ensure_on_travel_page()

    async def is_context_destroyed(self) -> bool:
        """Check if execution context was destroyed (navigation crash)"""
        try:
            # Wait a moment if page/context is temporarily None (might be initializing)
            if not self.page or not self.context:
                await asyncio.sleep(0.5)  # Give it a moment
                if not self.page or not self.context:
                    logger.warning("🚨 Page or context is None after wait - likely destroyed")
                    return True

            # Check if page is closed (avoid calling methods on invalid pages)
            try:
                if hasattr(self.page, 'is_closed') and self.page.is_closed():
                    logger.warning("🚨 Page is closed - destroyed")
                    return True
            except Exception:
                logger.warning("🚨 Cannot check if page is closed - likely destroyed")
                return True

            # Try to get current URL - this often fails when context is destroyed
            try:
                current_url = self.page.url
            except Exception as e:
                if "'NoneType' object has no attribute 'send'" in str(e):
                    logger.warning("� Page connection lost - context destroyed")
                    return True
                raise  # Re-raise other exceptions

            if not current_url or current_url == "about:blank":
                logger.warning("🚨 Page URL is blank or empty - likely destroyed")
                return True

            # Try a simple DOM operation to test if context is alive (with extra protection)
            try:
                await self.page.evaluate("() => document.readyState")
            except Exception as e:
                if "'NoneType' object has no attribute 'send'" in str(e):
                    logger.warning("🚨 DOM operation failed - context destroyed")
                    return True
                raise  # Re-raise other exceptions

            # Only consider it destroyed if we're on a completely different domain
            if "simple-mmo" not in current_url and "localhost" not in current_url and current_url != "about:blank":
                logger.warning(f"🚨 Page navigated away from SimpleMMO: {current_url}")
                return True

            return False

        except Exception as e:
            error_msg = str(e).lower()

            # Handle specific connection lost errors
            if "'nonetype' object has no attribute 'send'" in error_msg:
                logger.warning("🚨 Connection lost - context destroyed")
                return True

            # Only trigger on definitive context destruction errors
            if any(
                phrase in error_msg
                for phrase in [
                    "execution context was destroyed",
                    "target closed",
                    "page closed",
                    "browser closed",
                    "context was destroyed",
                ]
            ):
                logger.warning(f"🚨 Context destroyed detected: {e}")
                return True
            # For other errors (like network issues), don't consider context destroyed
            logger.debug(f"Context check error (assuming alive): {e}")
            return False

    async def handle_context_destruction(self):
        """Handle execution context destruction by cleaning up"""
        logger.warning("🔄 Handling context destruction...")
        self.page = None
        self.context = None
        # Don't cleanup browser completely, just invalidate page references


class WebEngineManager:
    """Singleton manager for web engine"""

    _instance: WebAutomationEngine | None = None

    @classmethod
    async def get_instance(cls) -> WebAutomationEngine:
        """Get or create web engine instance"""
        if cls._instance is None or not cls._instance.is_initialized:
            # Force cleanup of any existing instance
            if cls._instance:
                logger.debug("🔄 Cleaning up existing uninitialized instance")
                await cls._instance.cleanup()

            config: dict[str, Any] = {
                "browser_headless": False,
                "target_url": "https://web.simple-mmo.com/travel",
            }
            logger.debug("🔄 Creating new WebAutomationEngine instance")
            cls._instance = WebAutomationEngine(config)

            # Initialize with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                logger.debug(f"🔄 Initialization attempt {attempt + 1}/{max_retries}")
                try:
                    success = await cls._instance.initialize()
                    if success:
                        logger.debug("✅ WebEngine initialization successful")
                        break
                    else:
                        logger.warning(f"⚠️ Initialization attempt {attempt + 1} failed")
                        if attempt < max_retries - 1:
                            await asyncio.sleep(1)  # Wait before retry
                except Exception as e:
                    logger.warning(f"⚠️ Initialization attempt {attempt + 1} error: {e}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(1)  # Wait before retry

            # Final validation
            if not cls._instance.is_initialized:
                logger.error("❌ Failed to initialize WebEngine after retries")

        return cls._instance

    @classmethod
    async def shutdown(cls) -> None:
        """Shutdown the web engine instance"""
        if cls._instance:
            logger.debug("🔄 Shutting down WebEngineManager singleton")
            await cls._instance.shutdown()
            cls._instance = None
            logger.debug("✅ WebEngineManager singleton reset")

    @classmethod
    async def force_reset(cls) -> None:
        """Force complete reset of singleton"""
        logger.info("🔄 Force resetting WebEngineManager...")
        if cls._instance:
            try:
                await cls._instance.cleanup()
            except Exception as e:
                logger.debug(f"Cleanup error during force reset: {e}")
            cls._instance = None
        logger.success("✅ WebEngineManager force reset complete")


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
    return await engine.navigate_to_travel()


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
