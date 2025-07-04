"""
🚀 Browser Launcher - SimpleMMO Bot

Script para abrir o navegador na configuração correta para o bot.
Baseado no demo_bot_completo.py que funciona perfeitamente.

Ideal para usar com interface gráfica (botão "Abrir Navegador").
"""

import os
import subprocess
import time

from loguru import logger


class BrowserLauncher:
    """Classe para gerenciar a abertura do navegador"""

    def __init__(self):
        # Caminhos baseados no demo que funciona
        self.chromium_path = (
            r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\chrome.exe"
        )
        self.profile_dir = (
            r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\User Data"
        )
        self.profile_name = "perfilteste"  # Mesmo perfil do demo

    def check_chromium_installed(self) -> bool:
        """Verifica se o Chromium está instalado"""
        if os.path.exists(self.chromium_path):
            logger.success(f"✅ Chromium found: {self.chromium_path}")
            return True
        else:
            logger.error(f"❌ Chromium not found at: {self.chromium_path}")
            logger.info("💡 Try running: python -m playwright install chromium")
            return False

    def setup_profile_directory(self) -> bool:
        """Configura o diretório do perfil"""
        try:
            os.makedirs(self.profile_dir, exist_ok=True)
            logger.success(f"📁 Profile directory ready: {self.profile_dir}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create profile directory: {e}")
            return False

    def launch_browser(self, url: str = "https://web.simple-mmo.com") -> bool:
        """
        🚀 Lança o navegador com a configuração correta

        Args:
            url: URL para abrir (padrão: SimpleMMO)

        Returns:
            True se sucesso, False se erro
        """
        try:
            logger.info("🔧 Preparing to launch browser...")

            # Verifica se Chromium está instalado
            if not self.check_chromium_installed():
                return False

            # Configura diretório do perfil
            if not self.setup_profile_directory():
                return False

            # Comando para abrir Chromium (mesmo do demo que funciona)
            command = [
                self.chromium_path,
                "--remote-debugging-port=9222",
                f"--user-data-dir={self.profile_dir}",
                f"--profile-directory={self.profile_name}",
                # Flags para evitar detecção (mesmo do demo)
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
                url,
            ]

            logger.info(f"🚀 Starting Chromium with {self.profile_name} profile...")
            logger.info(f"📍 URL: {url}")
            logger.info(f"✅ Using saved profile: {self.profile_name}")

            # Abre o processo em background (mesmo do demo)
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            )

            logger.success("✅ Browser launched successfully!")
            logger.info("👆 A Chromium window should have opened")
            logger.info("🔗 Browser is ready for bot connection on port 9222")

            return True

        except Exception as e:
            logger.error(f"❌ Error launching browser: {e}")
            return False

    def launch_for_bot(self) -> bool:
        """Lança o navegador especificamente para o bot"""
        logger.info("🤖 Launching browser for SimpleMMO Bot...")

        success = self.launch_browser("https://web.simple-mmo.com/travel")

        if success:
            logger.info("📋 Next steps:")
            logger.info("   1. ✅ Browser opened with saved login")
            logger.info("   2. ✅ Navigate to travel page if needed")
            logger.info("   3. ✅ Run the bot (it will connect automatically)")
            logger.info("   4. 🎮 Enjoy automated gameplay!")

        return success


async def test_browser_connection():
    """
    🔗 Testa se consegue conectar ao navegador aberto
    """
    try:
        logger.info("🔗 Testing connection to browser...")

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

                    if "simple-mmo.com" in url:
                        logger.success("🎮 Connected to SimpleMMO!")
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
        logger.info("   • Browser is running")
        logger.info("   • You are logged into SimpleMMO")
        return False


def quick_launch():
    """🚀 Lançamento rápido - abre browser e testa conexão"""
    logger.info("🚀 Quick Launch - Opening browser and testing connection...")

    # Lança o navegador
    launcher = BrowserLauncher()
    if not launcher.launch_for_bot():
        logger.error("❌ Failed to launch browser")
        return False

    # Aguarda um pouco para o browser carregar
    logger.info("⏳ Waiting for browser to load...")
    for i in range(5, 0, -1):
        logger.info(f"⏰ {i} seconds remaining...")
        time.sleep(1)

    # Testa conexão
    logger.info("🔗 Testing connection...")
    import asyncio

    if asyncio.run(test_browser_connection()):
        logger.success("🎉 Browser ready for bot!")
        return True
    else:
        logger.warning("⚠️ Browser may still be loading. Try again in a moment.")
        return False


def main():
    """Menu principal para o browser launcher"""
    logger.info("🚀 SimpleMMO Bot - Browser Launcher")
    logger.info("=" * 50)

    while True:
        logger.info("\n📋 Choose an option:")
        logger.info("1. 🚀 Launch browser for bot")
        logger.info("2. 🔗 Test connection to browser")
        logger.info("3. ⚡ Quick launch (launch + test)")
        logger.info("4. 🌐 Launch browser with custom URL")
        logger.info("5. ❌ Exit")

        try:
            choice = input("\n👉 Enter your choice (1-5): ").strip()

            if choice == "1":
                logger.info("\n" + "=" * 40)
                launcher = BrowserLauncher()
                launcher.launch_for_bot()

            elif choice == "2":
                logger.info("\n" + "=" * 40)
                import asyncio

                asyncio.run(test_browser_connection())

            elif choice == "3":
                logger.info("\n" + "=" * 40)
                quick_launch()

            elif choice == "4":
                logger.info("\n" + "=" * 40)
                url = input("🌐 Enter URL (or press Enter for SimpleMMO): ").strip()
                if not url:
                    url = "https://web.simple-mmo.com"

                launcher = BrowserLauncher()
                launcher.launch_browser(url)

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


# Função para integração com UI futura
def launch_browser_for_ui(callback=None):
    """
    🎯 Função específica para integração com interface gráfica

    Args:
        callback: Função para chamar quando browser estiver pronto

    Returns:
        True se sucesso, False se erro
    """
    try:
        logger.info("🚀 Launching browser from UI...")

        launcher = BrowserLauncher()
        success = launcher.launch_for_bot()

        if success and callback:
            # Aguarda um pouco e chama callback
            time.sleep(3)
            callback("Browser launched successfully!")

        return success

    except Exception as e:
        logger.error(f"❌ UI launch failed: {e}")
        if callback:
            callback(f"Error: {e}")
        return False


if __name__ == "__main__":
    main()
