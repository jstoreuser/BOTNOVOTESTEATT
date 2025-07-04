"""
🔓 Bot Demo Completo - Solução Cloudflare

Este script resolve o problema do Cloudflare:
1. Abre Chromium com perfil persistente
2. Permite login manual primeiro
3. Conecta o bot ao browser já logado
"""

import asyncio
import os
import subprocess
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from loguru import logger


def setup_chromium_with_profile():
    """
    🚀 Configura Chromium com perfil persistente para evitar Cloudflare
    """
    try:
        logger.info("🔧 Setting up Chromium with persistent profile...")

        # Caminhos
        chromium_path = (
            r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\chrome.exe"
        )
        # Usando o perfil "Profile 1" criado no Chromium do Playwright
        profile_dir = r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\User Data"

        # Verifica se o Chromium existe
        if not os.path.exists(chromium_path):
            logger.error(f"❌ Chromium not found at: {chromium_path}")
            logger.info("💡 Try running: python -m playwright install chromium")
            return False

        # Cria diretório do perfil se não existir
        os.makedirs(profile_dir, exist_ok=True)
        logger.info(f"📁 Profile directory: {profile_dir}")

        # Comando para abrir Chromium com perfilteste (stealth mode)
        command = [
            chromium_path,
            "--remote-debugging-port=9222",
            f"--user-data-dir={profile_dir}",
            "--profile-directory=perfilteste",
            # Flags mais discretos para evitar detecção do Cloudflare
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
            "https://web.simple-mmo.com",
        ]

        logger.info("🚀 Starting Chromium with perfilteste profile...")
        logger.info("📍 URL: https://web.simple-mmo.com")
        logger.info("✅ Using perfilteste profile from Chromium (with saved login)")

        # Abre o processo em background
        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )

        logger.success("✅ Chromium started with perfilteste profile!")
        logger.info("👆 A Chromium window should have opened with your saved login")
        logger.info("📋 Next steps:")
        logger.info("   1. ✅ Browser should auto-login with saved credentials")
        logger.info("   2. ✅ Navigate to travel page if needed")
        logger.info("   3. ✅ Run option 2 to test connection or option 3 to run bot")

        return True

    except Exception as e:
        logger.error(f"❌ Error setting up Chromium: {e}")
        return False


async def test_connection_to_browser():
    """
    🔗 Testa conexão com o browser já aberto
    """
    try:
        logger.info("🔗 Testing connection to running browser...")

        from playwright.async_api import async_playwright

        playwright = await async_playwright().start()
        try:
            # Conecta ao browser na porta 9222
            browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")

            # Pega a primeira aba
            contexts = browser.contexts
            if contexts:
                context = contexts[0]
                pages = context.pages
                if pages:
                    page = pages[0]

                    # Testa a página
                    url = page.url
                    title = await page.title()

                    logger.success("✅ Successfully connected to browser!")
                    logger.info(f"📍 Current URL: {url}")
                    logger.info(f"📄 Page title: {title}")

                    # Verifica se está logado
                    if "simple-mmo.com" in url:
                        logger.success("🎮 Connected to SimpleMMO!")

                        # Testa procurar botões
                        step_buttons = await page.query_selector_all(
                            'button:has-text("Take a step")'
                        )
                        logger.info(f"👣 Found {len(step_buttons)} step buttons")

                        attack_elements = await page.query_selector_all(
                            'button:has-text("Attack"), a:has-text("Attack")'
                        )
                        logger.info(f"⚔️ Found {len(attack_elements)} attack elements")

                        return True
                    else:
                        logger.warning("⚠️ Not on SimpleMMO page")
                        return False
                else:
                    logger.error("❌ No pages found in browser")
                    return False
            else:
                logger.error("❌ No contexts found in browser")
                return False

        finally:
            await playwright.stop()

    except Exception as e:
        logger.error(f"❌ Connection test failed: {e}")
        logger.info("💡 Make sure:")
        logger.info("   • Chromium is running with debugging port 9222")
        logger.info("   • You are logged into SimpleMMO")
        logger.info("   • Cloudflare challenge is completed")
        return False


async def run_step_bot_connected():
    """
    🤖 Executa o bot conectando ao browser já aberto
    """
    try:
        logger.info("🤖 Starting bot connected to existing browser...")

        from playwright.async_api import async_playwright

        playwright = await async_playwright().start()
        try:
            # Conecta ao browser
            browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = context.pages[0]

            logger.info("🎮 Bot connected! Starting automation...")

            # Loop simples do bot
            for step_num in range(10):  # 10 steps de teste
                try:
                    logger.info(f"👣 Attempting step {step_num + 1}/10")

                    # Procura botão de step
                    step_buttons = await page.query_selector_all('button:has-text("Take a step")')

                    if step_buttons:
                        # Clica no primeiro botão
                        await step_buttons[0].click()
                        logger.success(f"✅ Step {step_num + 1} completed!")

                        # Aguarda um pouco (delay humano)
                        await asyncio.sleep(4)
                    else:
                        logger.warning(f"⚠️ No step buttons found on step {step_num + 1}")

                        # Tenta navegar para travel
                        await page.goto("https://web.simple-mmo.com/travel")
                        await page.wait_for_load_state("networkidle")
                        await asyncio.sleep(2)

                except Exception as e:
                    logger.error(f"❌ Error on step {step_num + 1}: {e}")
                    await asyncio.sleep(2)

            logger.success("🎉 Bot test completed!")

        finally:
            await playwright.stop()

        return True

    except Exception as e:
        logger.error(f"❌ Bot execution failed: {e}")
        return False


async def demo_bot_completo():
    """
    🚀 Demonstração completa do bot funcionando
    """
    try:
        logger.info("🎯 Starting Complete Bot Demo")
        logger.info("📌 Browser will open and you'll see the bot working!")

        # Import systems
        from core.steps import StepSystem
        from core.web_engine import WebAutomationEngine

        # Configuration for visible browser (simplified)
        config = {
            "browser_headless": False,  # Browser visível
            "target_url": "https://web.simple-mmo.com/travel",
        }

        logger.info("🌐 Creating web engine...")
        engine = WebAutomationEngine(config)

        logger.info("🚀 Opening browser (visible)...")
        if not await engine.initialize():
            logger.error("❌ Failed to open browser")
            return

        logger.success("✅ Browser opened! You should see it on your screen.")

        # Initialize step system
        step_config = {
            "delays": {
                "between_steps_min": 2.0,
                "between_steps_max": 4.0,
                "step_detection_timeout": 5.0,
                "navigation_timeout": 10.0,
            },
            "travel": {
                "auto_navigate": True,
                "step_strategies": ["button_text", "onclick_step", "any_button"],
            },
        }

        logger.info("👣 Initializing step system...")
        step_system = StepSystem(step_config)
        await step_system.initialize()

        # Demo loop
        logger.info("🎮 Starting bot demo loop...")
        logger.info("📺 Watch the browser - you'll see the bot taking actions!")

        for cycle in range(5):  # 5 cycles for demo
            try:
                logger.info(f"🔄 Demo cycle {cycle + 1}/5")

                # Get current page info
                page = await engine.get_page()
                if page:
                    current_url = page.url
                    page_title = await page.title()
                    logger.info(f"📍 Current page: {page_title}")
                    logger.info(f"🌐 URL: {current_url}")

                # Try to take a step
                logger.info("👣 Attempting to take a step...")
                if await step_system.is_step_available():
                    logger.info("✅ Step button found! Taking step...")
                    success = await step_system.take_step()
                    if success:
                        logger.success("🎯 Step taken successfully!")
                    else:
                        logger.warning("⚠️ Step failed")
                else:
                    logger.info("ℹ️ No steps available, navigating to travel...")
                    await step_system.navigate_to_travel()

                # Wait between cycles
                logger.info("⏰ Waiting 3 seconds before next cycle...")
                await asyncio.sleep(3)

            except Exception as e:
                logger.error(f"❌ Error in cycle {cycle + 1}: {e}")
                await asyncio.sleep(2)

        # Show final stats
        stats = step_system.get_step_stats()
        logger.info("📊 Demo Statistics:")
        logger.info(f"   • Steps taken: {stats.get('steps_taken', 0)}")
        logger.info(f"   • Successful steps: {stats.get('successful_steps', 0)}")
        logger.info(f"   • Failed steps: {stats.get('failed_steps', 0)}")

        logger.info("⏰ Keeping browser open for 10 more seconds...")
        logger.info("🎮 You can see the final state of the game!")
        await asyncio.sleep(10)

        # Cleanup
        logger.info("🧹 Cleaning up...")
        await engine.shutdown()

        logger.success("✅ Complete bot demo finished!")
        logger.info("🚀 The bot is fully functional and ready for use!")

    except Exception as e:
        logger.error(f"💥 Error in demo: {e}")
        logger.exception("Full traceback:")


def main():
    """
    🚀 Menu principal - Agora usando perfil BOTNOVOTESTATT automaticamente
    """
    logger.info("🔓 SimpleMMO Bot - Ready with perfilteste Profile")
    logger.info("=" * 60)
    logger.info("✅ Using Chromium perfilteste profile (already logged in)")

    while True:
        logger.info("\n📋 Choose an option:")
        logger.info("1. 🚀 Start browser with perfilteste profile")
        logger.info("2. 🔗 Test connection to running browser")
        logger.info("3. 🤖 Run bot connected to browser")
        logger.info("4. 🏃 Quick start (start browser + run bot)")
        logger.info("5. ❌ Exit")

        try:
            choice = input("\n👉 Enter your choice (1-5): ").strip()

            if choice == "1":
                logger.info("\n" + "=" * 50)
                logger.info("🔧 Starting Chromium with perfilteste profile...")
                if setup_chromium_with_profile():
                    logger.info("✅ Browser started with your saved login!")
                    logger.info("🎯 Choose option 2 to test connection or 3 to run bot")
                else:
                    logger.error("❌ Failed to start browser")

            elif choice == "2":
                logger.info("\n" + "=" * 50)
                if asyncio.run(test_connection_to_browser()):
                    logger.info("🎯 Connection successful! Choose option 3 to run the bot")
                else:
                    logger.info("🎯 Connection failed. Make sure browser is running")

            elif choice == "3":
                logger.info("\n" + "=" * 50)
                asyncio.run(run_step_bot_connected())

            elif choice == "4":
                logger.info("\n" + "=" * 50)
                logger.info("🚀 Quick start with perfilteste profile...")

                if setup_chromium_with_profile():
                    logger.info("⏳ Waiting 5 seconds for browser to load...")

                    import time
                    for i in range(5, 0, -1):
                        logger.info(f"⏰ {i} seconds remaining...")
                        time.sleep(1)

                    logger.info("🔗 Testing connection...")
                    if asyncio.run(test_connection_to_browser()):
                        logger.success("✅ Connected! Starting bot...")
                        time.sleep(1)
                        asyncio.run(run_step_bot_connected())
                    else:
                        logger.warning("⚠️ Could not connect. Browser may still be loading.")
                        logger.info("💡 Try option 2 to test connection manually")
                else:
                    logger.error("❌ Failed to start browser")

            elif choice == "5":
                logger.info("👋 Goodbye!")
                break

            else:
                logger.warning("⚠️ Invalid choice. Please enter 1-5")

        except KeyboardInterrupt:
            logger.info("\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            logger.error(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
