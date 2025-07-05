"""
⛏️ Gathering System for SimpleMMO Bot

Modern gathering system using Playwright.
Handles the complete gathering process: detecting gather opportunities (chop, mine, salvage, catch),
clicking gather buttons, waiting for cooldowns, and collecting all available materials.
"""

import asyncio
import time
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


class GatheringSystem:
    """Modern gathering system for SimpleMMO Bot"""

    def __init__(self, config: dict[str, Any]):
        """Initialize Gathering System"""
        self.config = config
        self.is_initialized = False
        self.auto_gather = config.get("auto_gather", True)
        self.gather_types = ["chop", "mine", "salvage", "catch"]
        self.last_gather_time = 0
        self.gather_cooldown = 2.0  # seconds
        self.gather_delay = 0.5  # delay between gather clicks (optimized)
        self.max_wait_time = 5.0  # increased timeout for better detection
        self.button_check_interval = 0.05  # intervalo para verificar botão (optimized)
        logger.info("⛏️ Gathering System created")

    async def initialize(self) -> bool:
        """Initialize gathering system"""
        try:
            self.is_initialized = True
            logger.success("✅ Gathering System initialized")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gathering System: {e}")
            return False

    async def is_gathering_available(self) -> bool:
        """Check if gathering is available on current page (travel page) - ULTRA FAST"""
        try:
            if not self.auto_gather:
                return False

            engine = await get_web_engine()
            page = await engine.get_page()

            if not page:
                return False

            # Ultra-fast checks for most common gathering types (no XPath for speed)
            quick_selectors = [
                'button:has-text("Mine")',
                'button:has-text("Chop")',
                'button:has-text("Salvage")',
                'button:has-text("Catch")',
            ]

            for selector in quick_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element and await element.is_visible() and await element.is_enabled():
                        return True
                except Exception:
                    continue

            return False

        except Exception as e:
            logger.debug(f"Error checking gathering availability: {e}")
            return False

    async def start_gathering(self) -> bool:
        """Start complete gathering process"""
        try:
            # Check cooldown
            current_time = time.time()
            if current_time - self.last_gather_time < self.gather_cooldown:
                logger.debug("Gathering on cooldown")
                return False

            logger.info("⛏️ Starting gathering process...")

            engine = await get_web_engine()
            page = await engine.get_page()

            if not page:
                return False

            # Step 1: Find and click gathering type button (chop, mine, salvage, catch)
            gather_type_button = await self._find_gather_type_button(page)

            if not gather_type_button:
                logger.debug("No gathering type button found")
                return False

            # Click the gather type button to enter gathering page
            await gather_type_button.click()
            logger.info("🎯 Clicked gathering type button")

            # Wait for page to load - otimizado
            await page.wait_for_load_state("domcontentloaded")  # Mais rápido que networkidle
            await asyncio.sleep(0.5)  # Reduzido para 0.5s

            # Step 2: Check if we're on the gathering page
            if not await self._is_on_gathering_page(page):
                logger.warning("Not on gathering page after clicking button")
                return False

            # Step 3: Get available amount
            available_amount = await self._get_available_amount(page)
            logger.info(f"🔢 Available materials: {available_amount}")

            if available_amount <= 0:
                logger.warning("No materials available to gather")
                await self._close_gathering_page(page)
                return False            # Step 4: Perform gathering clicks
            success_count = 0
            for i in range(available_amount):
                logger.info(f"⛏️ Gathering {i + 1}/{available_amount}...")

                if await self._perform_single_gather(page):
                    success_count += 1
                    if i < available_amount - 1:  # Não fazer delay após o último
                        logger.debug(f"✅ Gather {i + 1} completed, waiting {self.gather_delay}s...")
                        await asyncio.sleep(self.gather_delay)
                else:
                    logger.warning(f"Failed to gather item {i + 1}")
                    break

            # Step 5: Close gathering page
            logger.debug("🚪 Closing gathering page...")
            await self._close_gathering_page(page)

            self.last_gather_time = current_time
            logger.success(f"✅ Gathering completed: {success_count}/{available_amount}")

            return success_count > 0

        except Exception as e:
            logger.error(f"❌ Error during gathering: {e}")
            return False

    async def _find_gather_type_button(self, page) -> Any | None:
        """Find gathering type button on travel page (chop, mine, salvage, catch)."""
        try:
            gather_selectors = [
                'button:has-text("Chop")',
                'button:has-text("Mine")',
                'button:has-text("Salvage")',
                'button:has-text("Catch")',
                '//button[contains(text(), "Chop")]',
                '//button[contains(text(), "Mine")]',
                '//button[contains(text(), "Salvage")]',
                '//button[contains(text(), "Catch")]',
            ]

            for selector in gather_selectors:
                try:
                    if selector.startswith("//"):
                        element = await page.query_selector(f"xpath={selector}")
                    else:
                        element = await page.query_selector(selector)

                    if element and await element.is_visible() and await element.is_enabled():
                        button_text = await element.inner_text()
                        logger.debug(f"Found gathering button: {button_text}")
                        return element
                except Exception:
                    continue

            return None
        except Exception:
            return None

    async def _is_on_gathering_page(self, page) -> bool:
        """Check if we're on the gathering page (crafting/material/gather)."""
        try:
            url = page.url
            return "crafting/material/gather" in url
        except Exception:
            return False

    async def _get_available_amount(self, page) -> int:
        """Get available amount from gathering page."""
        try:
            # Look for the available amount element
            selectors = [
                '//div[@class="text-gray-500 font-semibold mr-4 text-xs sm:text-sm" and @x-text="available_amount"]',
                '//div[contains(@class, "text-gray-500") and contains(@x-text, "available_amount")]',
                'div[x-text="available_amount"]',
            ]

            for selector in selectors:
                try:
                    if selector.startswith("//"):
                        element = await page.query_selector(f"xpath={selector}")
                    else:
                        element = await page.query_selector(selector)

                    if element:
                        amount_text = await element.inner_text()
                        amount = int(amount_text.strip())
                        return amount
                except Exception:
                    continue

            return 0
        except Exception:
            return 0

    async def _perform_single_gather(self, page) -> bool:
        """Perform a single gather click and wait for completion."""
        try:
            # Find gather button
            gather_button = await self._find_gather_button_on_page(page)

            if not gather_button:
                logger.debug("Gather button not found")
                return False

            # Click the button
            await gather_button.click()
            logger.debug("Clicked gather button")

            # Wait for button to become disabled (loading state)
            await self._wait_for_gather_completion(page)

            return True

        except Exception as e:
            logger.debug(f"Error in single gather: {e}")
            return False

    async def _find_gather_button_on_page(self, page) -> Any | None:
        """Find the 'Press here to gather' button on gathering page."""
        try:
            gather_selectors = [
                '//button[@id="crafting_button" and .//span[text()="Press here to gather"]]',
                '//button[.//span[contains(text(),"Press here to gather")]]',
                'button:has-text("Press here to gather")',
                '#crafting_button',
            ]

            for selector in gather_selectors:
                try:
                    if selector.startswith("//"):
                        element = await page.query_selector(f"xpath={selector}")
                    else:
                        element = await page.query_selector(selector)

                    if element and await element.is_visible() and await element.is_enabled():
                        return element
                except Exception:
                    continue

            return None
        except Exception:
            return None

    async def _wait_for_gather_completion(self, page) -> bool:
        """Wait for gather button to complete its action (otimizado)."""
        try:
            max_wait = self.max_wait_time
            start_time = time.time()

            # Primeira verificação rápida para ver se o botão ficou disabled
            initial_disabled = False
            for _ in range(10):  # Verifica por 1 segundo
                try:
                    gather_button = await page.query_selector('#crafting_button')
                    if gather_button and await gather_button.is_disabled():
                        initial_disabled = True
                        break
                    await asyncio.sleep(0.1)
                except Exception:
                    await asyncio.sleep(0.1)

            if not initial_disabled:
                # Se não ficou disabled, assume que completou rapidamente
                await asyncio.sleep(0.2)
                return True

            # Aguarda o botão voltar a ficar enabled
            while time.time() - start_time < max_wait:
                try:
                    gather_button = await page.query_selector('#crafting_button')

                    if gather_button and not await gather_button.is_disabled():
                        # Botão voltou a ficar enabled
                        await asyncio.sleep(0.1)  # Pequena pausa para estabilidade
                        return True

                    await asyncio.sleep(self.button_check_interval)

                except Exception:
                    await asyncio.sleep(self.button_check_interval)

            return True  # Timeout, assume completed

        except Exception:
            return True

    async def _close_gathering_page(self, page) -> bool:
        """Close gathering page and return to travel."""
        try:
            await asyncio.sleep(0.3)  # Reduzido para 0.3s

            # Look for close button
            close_selectors = [
                '//button[.//span[text()="Press here to close"]]',
                'button:has-text("Press here to close")',
                '//button[@x-on:click="close()"]',
                '//button[contains(@class, "bg-gray-200") and .//span[text()="Press here to close"]]',
            ]

            for selector in close_selectors:
                try:
                    if selector.startswith("//"):
                        element = await page.query_selector(f"xpath={selector}")
                    else:
                        element = await page.query_selector(selector)

                    if element and await element.is_visible():
                        await element.click()
                        logger.debug("Clicked close button")
                        # Aguarda 2 segundos para o carregamento
                        await asyncio.sleep(2.0)
                        return True
                except Exception:
                    continue

            logger.debug("No close button found or already closed")
            return False

        except Exception as e:
            logger.debug(f"Error closing gathering page: {e}")
            return False

    async def get_gather_info(self) -> dict[str, Any]:
        """Get gathering information"""
        try:
            engine = await get_web_engine()
            page = await engine.get_page()

            if not page:
                return {}

            # Check if we're on gathering page or travel page
            is_on_gather_page = await self._is_on_gathering_page(page)
            available_amount = 0

            if is_on_gather_page:
                available_amount = await self._get_available_amount(page)

            info = {
                "available": await self.is_gathering_available(),
                "on_gather_page": is_on_gather_page,
                "available_amount": available_amount,
                "last_gather": self.last_gather_time,
                "cooldown_remaining": max(
                    0, self.gather_cooldown - (time.time() - self.last_gather_time)
                ),
            }

            return info

        except Exception as e:
            logger.debug(f"Error getting gather info: {e}")
            return {}

    async def get_available_amount(self) -> int:
        """Get available amount of materials"""
        try:
            engine = await get_web_engine()
            page = await engine.get_page()

            if not page:
                return 0

            if await self._is_on_gathering_page(page):
                return await self._get_available_amount(page)

            return 0

        except Exception:
            return 0

    async def set_timing_config(self, **kwargs) -> None:
        """Permite ajustar os timings do sistema dinamicamente."""
        if "gather_delay" in kwargs:
            self.gather_delay = kwargs["gather_delay"]
            logger.info(f"⚙️ Gather delay set to {self.gather_delay}s")

        if "max_wait_time" in kwargs:
            self.max_wait_time = kwargs["max_wait_time"]
            logger.info(f"⚙️ Max wait time set to {self.max_wait_time}s")

        if "button_check_interval" in kwargs:
            self.button_check_interval = kwargs["button_check_interval"]
            logger.info(f"⚙️ Button check interval set to {self.button_check_interval}s")
