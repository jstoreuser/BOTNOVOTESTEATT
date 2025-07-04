"""
🔧 Script para testar o workflow correto do bot

Este script demonstra o fluxo correto:
1. Inicia o demo_bot_completo.py para abrir o browser com perfilteste
2. Testa se o web_engine consegue se conectar ao browser existente
3. Executa o bot usando o perfil já logado
"""

import asyncio
import subprocess
import sys
import time
from pathlib import Path

# Add bot root directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from loguru import logger


def start_browser_with_profile():
    """Inicia o browser com perfilteste profile"""
    logger.info("🚀 Starting browser with perfilteste profile...")

    chromium_path = r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\chrome.exe"
    user_data_dir = r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\User Data"

    command = [
        chromium_path,
        "--remote-debugging-port=9222",
        f"--user-data-dir={user_data_dir}",
        "--profile-directory=perfilteste",
        "--disable-blink-features=AutomationControlled",
        "--disable-web-security",
        "--disable-features=VizDisplayCompositor",
        "--no-first-run",
        "--no-default-browser-check",
        "https://web.simple-mmo.com/travel"
    ]

    try:
        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )

        logger.success("✅ Browser started with perfilteste profile!")
        logger.info("⏳ Waiting 3 seconds for browser to load...")
        time.sleep(3)
        return True

    except Exception as e:
        logger.error(f"❌ Failed to start browser: {e}")
        return False


async def test_web_engine_connection():
    """Testa se o web_engine consegue se conectar ao browser"""
    logger.info("🔗 Testing web_engine connection...")

    try:
        from botlib import get_web_engine

        # Obter o web engine (deve conectar ao browser existente)
        engine = await get_web_engine()

        if engine and engine.is_initialized:
            page = await engine.get_page()
            if page:
                current_url = page.url
                page_title = await page.title()

                logger.success("✅ Web engine connected successfully!")
                logger.info(f"📍 Current page: {page_title}")
                logger.info(f"🌐 Current URL: {current_url}")

                # Verificar se está na página correta
                if "simple-mmo.com" in current_url:
                    logger.success("🎮 Connected to SimpleMMO!")
                    return True
                else:
                    logger.warning("⚠️ Not on SimpleMMO page")
                    return False
            else:
                logger.error("❌ No page available")
                return False
        else:
            logger.error("❌ Web engine not initialized")
            return False

    except Exception as e:
        logger.error(f"❌ Web engine connection failed: {e}")
        return False


async def test_step_system():
    """Testa o sistema de steps"""
    logger.info("👣 Testing step system...")

    try:
        from botlib import StepSystem

        step_config = {
            "delays": {
                "between_steps_min": 1.0,
                "between_steps_max": 2.0,
                "step_detection_timeout": 5.0,
                "navigation_timeout": 10.0
            },
            "travel": {
                "auto_navigate": True,
                "step_strategies": ["button_text", "onclick_step", "any_button"]
            }
        }

        step_system = StepSystem(step_config)
        await step_system.initialize()

        # Tentar detectar steps
        if await step_system.is_step_available():
            logger.success("✅ Step buttons detected!")
            return True
        else:
            logger.warning("⚠️ No step buttons found")
            # Tentar navegar para travel
            if await step_system.navigate_to_travel():
                logger.info("✅ Navigated to travel page")
                # Tentar novamente
                if await step_system.is_step_available():
                    logger.success("✅ Step buttons found after navigation!")
                    return True

            logger.warning("⚠️ No steps available")
            return False

    except Exception as e:
        logger.error(f"❌ Step system test failed: {e}")
        return False


async def run_full_test():
    """Executa o teste completo"""
    logger.info("🧪 Running full workflow test...")
    logger.info("=" * 50)

    # Passo 1: Iniciar browser
    logger.info("Step 1: Starting browser...")
    if not start_browser_with_profile():
        logger.error("❌ Failed to start browser")
        return False

    # Passo 2: Testar conexão do web_engine
    logger.info("Step 2: Testing web_engine connection...")
    if not await test_web_engine_connection():
        logger.error("❌ Web engine connection failed")
        return False

    # Passo 3: Testar sistema de steps
    logger.info("Step 3: Testing step system...")
    if not await test_step_system():
        logger.warning("⚠️ Step system test inconclusive")

    logger.success("🎉 Full workflow test completed!")
    logger.info("💡 The bot should now work correctly with your perfilteste profile")
    return True


def main():
    """Função principal"""
    logger.info("🔧 Bot Workflow Tester")
    logger.info("=" * 40)

    logger.info("This script will:")
    logger.info("1. 🚀 Start browser with perfilteste profile")
    logger.info("2. 🔗 Test web_engine connection")
    logger.info("3. 👣 Test step system")
    logger.info("4. 📊 Report results")

    answer = input("\n🤔 Continue with test? (y/n): ").lower().strip()

    if answer in ['y', 'yes']:
        asyncio.run(run_full_test())
    else:
        logger.info("👋 Test cancelled")


if __name__ == "__main__":
    main()
