"""
🎮 Browser Control Module - SimpleMMO Bot

Módulo simples para controle do navegador.
Baseado no demo_bot_completo.py que funciona perfeitamente.
Ideal para integração com interfaces gráficas.
"""

import os
import subprocess
import time

from loguru import logger


def open_browser_for_bot():
    """
    🚀 Abre o navegador configurado para o bot

    Função simples baseada no demo_bot_completo.py que funciona.
    Ideal para usar em botões de UI.

    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        logger.info("🚀 Opening browser for SimpleMMO Bot...")

        # Configuração exata do demo que funciona
        chromium_path = (
            r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\chrome.exe"
        )
        profile_dir = (
            r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\User Data"
        )
        profile_name = "perfilteste"  # Mesmo perfil do demo

        # Verifica se Chromium existe
        if not os.path.exists(chromium_path):
            logger.error("❌ Chromium not found!")
            logger.info("💡 Run: python -m playwright install chromium")
            return False

        # Cria diretório do perfil se necessário
        os.makedirs(profile_dir, exist_ok=True)

        # Comando exato do demo que funciona
        command = [
            chromium_path,
            "--remote-debugging-port=9222",
            f"--user-data-dir={profile_dir}",
            f"--profile-directory={profile_name}",
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
            "https://web.simple-mmo.com/travel",  # Página ideal para o bot
        ]

        # Executa em background (mesmo do demo)
        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )

        logger.success("✅ Browser opened successfully!")
        logger.info("🎮 Ready for bot connection on port 9222")
        logger.info("📍 Opening SimpleMMO travel page")

        return True

    except Exception as e:
        logger.error(f"❌ Failed to open browser: {e}")
        return False


def is_browser_running():
    """
    🔍 Verifica se o navegador está rodando na porta correta

    Returns:
        bool: True se rodando, False se não
    """
    try:
        import requests

        response = requests.get("http://localhost:9222/json", timeout=2)
        return response.status_code == 200
    except Exception:
        return False


def get_browser_status():
    """
    📊 Obtém status detalhado do navegador

    Returns:
        dict: Status do navegador
    """
    try:
        if is_browser_running():
            return {
                "running": True,
                "port": 9222,
                "profile": "perfilteste",
                "message": "Browser is running and ready for bot",
                "ready_for_bot": True,
            }
        else:
            return {
                "running": False,
                "port": None,
                "profile": None,
                "message": "Browser is not running",
                "ready_for_bot": False,
            }
    except Exception as e:
        return {
            "running": False,
            "port": None,
            "profile": None,
            "message": f"Error checking browser: {e}",
            "ready_for_bot": False,
        }


async def test_browser_connection():
    """
    🔗 Testa conexão com o navegador e verifica se está no SimpleMMO

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
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

                    # Verifica página atual
                    url = page.url
                    title = await page.title()

                    if "simple-mmo.com" in url:
                        return True, f"✅ Connected to SimpleMMO! Page: {title}"
                    else:
                        return False, f"⚠️ Connected but not on SimpleMMO. Current: {url}"
                else:
                    return False, "❌ No pages found in browser"
            else:
                return False, "❌ No browser contexts found"

        finally:
            await playwright.stop()

    except Exception as e:
        return False, f"❌ Connection failed: {e}"


# Função principal para UI (mais simples)
def launch_browser_for_ui():
    """
    🎯 Função específica para botões de interface gráfica

    Mais simples, sem logs excessivos.

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Verifica se já está rodando
        if is_browser_running():
            return True, "Browser is already running"

        # Abre o navegador
        success = open_browser_for_bot()

        if success:
            # Aguarda um pouco para carregar
            time.sleep(2)

            # Verifica se realmente abriu
            if is_browser_running():
                return True, "Browser opened successfully"
            else:
                return False, "Browser opened but not responding"
        else:
            return False, "Failed to open browser"

    except Exception as e:
        return False, f"Error: {e}"


# Para uso direto do script
if __name__ == "__main__":
    logger.info("🎮 SimpleMMO Browser Control")

    # Verifica status atual
    status = get_browser_status()
    logger.info(f"Status: {status['message']}")

    if not status["running"]:
        logger.info("🚀 Opening browser...")
        if open_browser_for_bot():
            logger.success("✅ Browser opened!")

            # Aguarda um pouco e testa conexão
            logger.info("⏳ Waiting for browser to load...")
            time.sleep(5)

            import asyncio

            connected, message = asyncio.run(test_browser_connection())
            if connected:
                logger.success(f"🔗 {message}")
                logger.info("🚀 You can now run the bot!")
            else:
                logger.warning(f"⚠️ {message}")
        else:
            logger.error("❌ Failed to open browser")
    else:
        logger.info("ℹ️ Browser already running")

        # Testa conexão
        import asyncio

        connected, message = asyncio.run(test_browser_connection())
        logger.info(f"🔗 {message}")
