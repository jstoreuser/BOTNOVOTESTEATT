"""
🧪 Teste do Quick Start com perfil BOTNOVOTESTATT

Este script testa se o bot consegue se conectar ao perfil
BOTNOVOTESTATT e executar steps automaticamente.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add bot root directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from loguru import logger


def test_profile_exists():
    """Verifica se o perfil BOTNOVOTESTATT existe"""
    profile_dir = r"C:\temp\BOTNOVOTESTATT"

    if os.path.exists(profile_dir):
        logger.success(f"✅ Profile found: {profile_dir}")

        # Check if there are some browser files
        files = os.listdir(profile_dir)
        if files:
            logger.info(f"📁 Profile has {len(files)} files/folders")
            return True
        else:
            logger.warning("⚠️ Profile directory is empty")
            return False
    else:
        logger.error(f"❌ Profile not found: {profile_dir}")
        logger.info("💡 Run demo_bot_completo.py option 1 to create profile")
        return False


def test_chromium_path():
    """Verifica se o Chromium está disponível"""
    chromium_path = r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\chrome.exe"

    if os.path.exists(chromium_path):
        logger.success(f"✅ Chromium found: {chromium_path}")
        return True
    else:
        logger.error(f"❌ Chromium not found: {chromium_path}")
        logger.info("💡 Run: python -m playwright install chromium")
        return False


async def test_connection():
    """Testa conexão com browser"""
    try:
        from playwright.async_api import async_playwright

        logger.info("🔗 Testing browser connection...")

        playwright = await async_playwright().start()
        try:
            browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")
            contexts = browser.contexts

            if contexts:
                page = contexts[0].pages[0] if contexts[0].pages else None
                if page:
                    title = await page.title()
                    url = page.url
                    logger.success(f"✅ Connected! Page: {title}")
                    logger.info(f"🌐 URL: {url}")
                    return True
                else:
                    logger.warning("⚠️ No pages found")
                    return False
            else:
                logger.warning("⚠️ No browser contexts found")
                return False

        finally:
            await playwright.stop()

    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")
        return False


def main():
    """Executa testes do sistema"""
    logger.info("🧪 Testing BOTNOVOTESTATT Setup")
    logger.info("=" * 50)

    # Test 1: Profile exists
    logger.info("🔍 Test 1: Checking profile...")
    profile_ok = test_profile_exists()

    # Test 2: Chromium available
    logger.info("🔍 Test 2: Checking Chromium...")
    chromium_ok = test_chromium_path()

    if not profile_ok or not chromium_ok:
        logger.error("❌ Prerequisites not met!")
        logger.info("💡 Run demo_bot_completo.py first to setup")
        return

    # Test 3: Check if browser is running
    logger.info("🔍 Test 3: Checking if browser is running...")
    connection_ok = asyncio.run(test_connection())

    if connection_ok:
        logger.success("🎉 All tests passed! Bot is ready to use!")
        logger.info("🚀 You can now run: python demo_bot_completo.py")
        logger.info("💡 Use option 3 to run the bot, or option 4 for quick start")
    else:
        logger.warning("⚠️ Browser not running or not accessible")
        logger.info("💡 Run demo_bot_completo.py option 1 to start browser")
        logger.info("💡 Or use option 4 for automatic start + run")

    logger.info("=" * 50)
    logger.info("✅ Test completed!")


if __name__ == "__main__":
    main()
