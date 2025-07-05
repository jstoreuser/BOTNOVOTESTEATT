"""
🤖 Bot Launcher - Conecta ao Browser Já Logado

Este script inicia o bot que conecta ao browser que você
já abriu e fez login manualmente com manual_profile_launcher.py
"""

import asyncio
import subprocess
import sys
import time
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from loguru import logger


def start_debugging_session():
    """Inicia sessão de debugging no browser já aberto"""
    logger.info("🔧 Starting Debugging Session on Existing Browser")
    logger.info("=" * 60)

    chromium_path = r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\chrome.exe"
    user_data_dir = r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\User Data"

    # Comando para abrir NOVA INSTÂNCIA com debugging no mesmo perfil
    command = [
        chromium_path,
        "--remote-debugging-port=9222",
        f"--user-data-dir={user_data_dir}",
        "--profile-directory=perfilteste",
        "--no-first-run",
        "--no-default-browser-check",
        "--new-window"  # Abre nova janela na sessão existente
    ]

    try:
        logger.info("🚀 Adding debugging to existing browser session...")
        logger.info("📡 Debug port: 9222")
        logger.info("👥 Connecting to existing perfilteste session")

        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )

        logger.success("✅ Debugging enabled on existing session!")
        logger.info("⏳ Waiting 3 seconds for debugging to initialize...")
        time.sleep(3)

        return True

    except Exception as e:
        logger.error(f"❌ Failed to enable debugging: {e}")
        return False


async def test_bot_connection():
    """Testa se o bot consegue conectar ao browser logado"""
    logger.info("🔗 Testing bot connection to logged browser...")

    try:
        # Import using botlib for simplified imports
        import sys
        from pathlib import Path

        # Ensure botlib is available
        bot_root = Path(__file__).parent.parent.parent
        if str(bot_root) not in sys.path:
            sys.path.insert(0, str(bot_root))

        from botlib import get_web_engine

        # Tentar conectar
        web_engine = await get_web_engine()

        if web_engine and web_engine.is_initialized:
            page = await web_engine.get_page()
            if page:
                current_url = page.url
                page_title = await page.title()

                logger.success("✅ Bot connected to browser!")
                logger.info(f"📍 Current page: {page_title}")
                logger.info(f"🌐 Current URL: {current_url}")

                # Verificar se está logado no SimpleMMO
                if "simple-mmo.com" in current_url:
                    logger.success("🎮 Connected to SimpleMMO!")

                    # Verificar elementos do jogo
                    step_buttons = await page.query_selector_all('button:has-text("Take a step")')
                    if step_buttons:
                        logger.success(f"👣 Found {len(step_buttons)} step buttons!")
                        return True
                    else:
                        logger.info("ℹ️ No step buttons found, may need to navigate to travel")
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
        logger.error(f"❌ Bot connection test failed: {e}")
        return False


async def run_step_bot():
    """Executa o bot de steps"""
    logger.info("🤖 Starting Step Bot...")

    try:
        # Import using botlib for simplified imports
        import sys
        from pathlib import Path

        # Ensure botlib is available
        bot_root = Path(__file__).parent.parent.parent
        if str(bot_root) not in sys.path:
            sys.path.insert(0, str(bot_root))

        from botlib import StepSystem

        step_config = {
            "delays": {
                "between_steps_min": 2.0,
                "between_steps_max": 4.0,
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

        logger.success("✅ Step system initialized!")
        logger.info("🚀 Starting automated steps...")
        logger.info("Press Ctrl+C to stop the bot")

        step_count = 0
        max_steps = 10  # Limite para teste

        while step_count < max_steps:
            try:
                logger.info(f"👣 Attempting step #{step_count + 1}/{max_steps}")

                # Usar o novo método inteligente que aguarda o botão
                success = await step_system.take_step()

                if success:
                    step_count += 1
                    logger.success(f"✅ Step #{step_count} completed!")
                else:
                    logger.info("🗺️ No steps available, navigating to travel...")
                    await step_system.navigate_to_travel()
                    # Aguardar um pouco após navegar
                    await asyncio.sleep(2)

                # Delay humano entre tentativas
                await asyncio.sleep(3)

            except KeyboardInterrupt:
                logger.info("🛑 Bot stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Error during step: {e}")
                await asyncio.sleep(2)

        # Estatísticas finais
        stats = step_system.get_step_stats()
        logger.info("📊 Bot Statistics:")
        logger.info(f"   • Steps taken: {stats.get('steps_taken', 0)}")
        logger.info(f"   • Successful: {stats.get('successful_steps', 0)}")
        logger.info(f"   • Failed: {stats.get('failed_steps', 0)}")

        return True

    except Exception as e:
        logger.error(f"❌ Bot execution failed: {e}")
        return False


async def main():
    """Função principal async"""
    logger.info("🤖 Bot Launcher - Connect to Logged Browser")
    logger.info("=" * 60)

    # Testar conexão diretamente (sem tentar habilitar debugging)
    logger.info("Step 1: Testing bot connection...")
    if not await test_bot_connection():
        logger.error("❌ Failed to connect to browser")
        logger.info("💡 Make sure:")
        logger.info("   • Browser was opened with manual_profile_launcher.py")
        logger.info("   • You are logged into SimpleMMO")
        logger.info("   • Browser window is not closed")
        logger.info("   • Debug port 9222 is active")
        return

    # Perguntar se deve executar o bot
    logger.info("")
    answer = input("🤔 Start automated step bot? (y/n): ").lower().strip()

    if answer in ['y', 'yes']:
        # Executar bot
        logger.info("Step 2: Running step bot...")
        await run_step_bot()
    else:
        logger.info("👋 Bot execution cancelled")

    logger.success("✅ Session completed!")


def sync_main():
    """Wrapper síncrono"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Interrupted by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")


if __name__ == "__main__":
    sync_main()
