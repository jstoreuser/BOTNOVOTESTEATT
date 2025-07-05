"""
🛡️ Teste de Cloudflare - Verificação de bypass

Este script testa se conseguimos passar pelo Cloudflare de forma mais discreta.
"""

import asyncio
import subprocess
import sys
import time
from pathlib import Path

# Add bot root directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from loguru import logger


def start_stealth_browser():
    """Inicia browser com configurações stealth máximas"""
    logger.info("🥷 Starting stealth browser for Cloudflare bypass...")

    chromium_path = r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\chrome.exe"
    user_data_dir = r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\User Data"

    # Configurações ultra-stealth
    command = [
        chromium_path,
        "--remote-debugging-port=9222",
        f"--user-data-dir={user_data_dir}",
        "--profile-directory=perfilteste",

        # Anti-detection flags
        "--disable-blink-features=AutomationControlled",
        "--exclude-switches=enable-automation",
        "--disable-extensions-except",
        "--disable-plugins-discovery",
        "--disable-dev-shm-usage",
        "--no-sandbox",

        # Performance and stealth
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-default-apps",
        "--disable-background-timer-throttling",
        "--disable-renderer-backgrounding",
        "--disable-backgrounding-occluded-windows",

        # User agent and window settings
        "--window-size=1280,720",
        "--start-maximized",

        # Target URL
        "https://web.simple-mmo.com"
    ]

    try:
        logger.info("🚀 Starting Chromium with stealth settings...")
        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )

        logger.success("✅ Stealth browser started!")
        logger.info("⏳ Waiting 5 seconds for page to load...")
        time.sleep(5)
        return True

    except Exception as e:
        logger.error(f"❌ Failed to start stealth browser: {e}")
        return False


async def test_cloudflare_bypass():
    """Testa se conseguimos acessar o SimpleMMO sem ser bloqueados"""
    logger.info("🛡️ Testing Cloudflare bypass...")

    try:
        from playwright.async_api import async_playwright

        playwright = await async_playwright().start()
        try:
            # Conecta ao browser
            browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")
            contexts = browser.contexts

            if not contexts:
                logger.error("❌ No browser contexts found")
                return False

            context = contexts[0]
            pages = context.pages

            if not pages:
                logger.error("❌ No pages found")
                return False

            page = pages[0]

            # Verifica página atual
            current_url = page.url
            page_title = await page.title()

            logger.info(f"📍 Current URL: {current_url}")
            logger.info(f"📄 Page title: {page_title}")

            # Verifica se há indicadores de Cloudflare
            cloudflare_indicators = [
                "Just a moment...",
                "Checking your browser",
                "DDoS protection",
                "Please wait",
                "Security check"
            ]

            page_content = await page.content()

            cloudflare_detected = False
            for indicator in cloudflare_indicators:
                if indicator.lower() in page_title.lower() or indicator.lower() in page_content.lower():
                    logger.warning(f"⚠️ Cloudflare indicator found: {indicator}")
                    cloudflare_detected = True

            if cloudflare_detected:
                logger.error("❌ Cloudflare challenge detected!")
                logger.info("💡 Possible solutions:")
                logger.info("   1. Wait longer for automatic bypass")
                logger.info("   2. Complete challenge manually")
                logger.info("   3. Try different browser settings")
                return False

            # Verifica se conseguimos acessar SimpleMMO
            if "simple-mmo.com" in current_url:
                logger.success("✅ Successfully accessing SimpleMMO!")

                # Verifica se está logado
                login_indicators = await page.query_selector_all('a[href*="logout"], button:has-text("Logout")')
                if login_indicators:
                    logger.success("🔑 User appears to be logged in!")
                else:
                    logger.warning("⚠️ User might not be logged in")

                # Verifica se há elementos do jogo
                step_buttons = await page.query_selector_all('button:has-text("Take a step")')
                travel_links = await page.query_selector_all('a[href*="travel"]')

                if step_buttons:
                    logger.success(f"👣 Found {len(step_buttons)} step buttons!")
                elif travel_links:
                    logger.info(f"🗺️ Found {len(travel_links)} travel links")
                    logger.info("💡 Try navigating to travel page")
                else:
                    logger.warning("⚠️ No game elements found")

                return True
            else:
                logger.warning(f"⚠️ Not on SimpleMMO page: {current_url}")
                return False

        finally:
            await playwright.stop()

    except Exception as e:
        logger.error(f"❌ Cloudflare test failed: {e}")
        return False


async def test_manual_navigation():
    """Testa navegação manual para a página de travel"""
    logger.info("🗺️ Testing manual navigation to travel page...")

    try:
        from playwright.async_api import async_playwright

        playwright = await async_playwright().start()
        try:
            browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = context.pages[0]

            # Navegar para travel
            logger.info("🚀 Navigating to travel page...")
            await page.goto("https://web.simple-mmo.com/travel")
            await page.wait_for_load_state("networkidle", timeout=15000)

            # Verificar se chegou na página correta
            current_url = page.url
            page_title = await page.title()

            logger.info(f"📍 After navigation: {current_url}")
            logger.info(f"📄 Page title: {page_title}")

            if "travel" in current_url:
                logger.success("✅ Successfully navigated to travel page!")

                # Verificar steps
                step_buttons = await page.query_selector_all('button:has-text("Take a step")')
                if step_buttons:
                    logger.success(f"👣 Found {len(step_buttons)} step buttons on travel page!")
                    return True
                else:
                    logger.warning("⚠️ No step buttons found on travel page")

                    # Verificar se precisa fazer login
                    login_form = await page.query_selector('form[action*="login"]')
                    if login_form:
                        logger.warning("🔑 Login form detected - user not logged in")

                    return False
            else:
                logger.warning(f"⚠️ Failed to reach travel page: {current_url}")
                return False

        finally:
            await playwright.stop()

    except Exception as e:
        logger.error(f"❌ Navigation test failed: {e}")
        return False


def main():
    """Executa testes completos de Cloudflare"""
    logger.info("🛡️ Cloudflare Bypass Testing Suite")
    logger.info("=" * 50)

    # Teste 1: Iniciar browser stealth
    logger.info("Test 1: Starting stealth browser...")
    if not start_stealth_browser():
        logger.error("❌ Failed to start browser")
        return

    # Aguardar um pouco mais
    logger.info("⏳ Waiting 10 seconds for full page load...")
    time.sleep(10)

    # Teste 2: Verificar bypass do Cloudflare
    logger.info("Test 2: Testing Cloudflare bypass...")
    cloudflare_ok = asyncio.run(test_cloudflare_bypass())

    if not cloudflare_ok:
        logger.warning("⚠️ Cloudflare test failed, but continuing...")

    # Teste 3: Navegação manual
    logger.info("Test 3: Testing manual navigation...")
    navigation_ok = asyncio.run(test_manual_navigation())

    # Resultados finais
    logger.info("=" * 50)
    logger.info("📊 Test Results:")
    logger.info(f"   🛡️ Cloudflare bypass: {'✅ PASS' if cloudflare_ok else '❌ FAIL'}")
    logger.info(f"   🗺️ Navigation: {'✅ PASS' if navigation_ok else '❌ FAIL'}")

    if cloudflare_ok and navigation_ok:
        logger.success("🎉 All tests passed! Bot should work!")
        logger.info("💡 You can now run: python demo_bot_completo.py")
    else:
        logger.warning("⚠️ Some tests failed. Manual intervention may be needed.")
        logger.info("💡 Try completing Cloudflare challenge manually in the browser")


if __name__ == "__main__":
    main()
