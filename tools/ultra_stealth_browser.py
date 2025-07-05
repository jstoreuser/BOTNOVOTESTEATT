"""
🥷 Ultra Stealth Browser para SimpleMMO

Este script abre o browser com configurações ultra-stealth
para maximizar as chances de passar pelo Cloudflare.
"""

import subprocess
import time

from loguru import logger


def start_ultra_stealth_browser():
    """Inicia browser com configurações ultra-stealth"""
    logger.info("🥷 Starting ULTRA stealth browser...")

    chromium_path = r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\chrome.exe"
    user_data_dir = r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\User Data"

    # Configurações ultra-stealth para máximo bypass
    command = [
        chromium_path,
        "--remote-debugging-port=9222",
        f"--user-data-dir={user_data_dir}",
        "--profile-directory=perfilteste",

        # Anti-detection (principais)
        "--disable-blink-features=AutomationControlled",
        "--exclude-switches=enable-automation",
        "--disable-extensions-except",
        "--disable-plugins-discovery",
        "--disable-dev-shm-usage",
        "--no-sandbox",

        # Stealth mode
        "--disable-features=VizDisplayCompositor",
        "--disable-ipc-flooding-protection",
        "--disable-background-timer-throttling",
        "--disable-renderer-backgrounding",
        "--disable-backgrounding-occluded-windows",
        "--disable-field-trial-config",

        # User experience
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-default-apps",
        "--disable-component-update",
        "--disable-background-networking",

        # Window settings
        "--window-size=1280,720",
        "--window-position=100,100",

        # User agent normal
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

        # Página inicial
        "https://web.simple-mmo.com"
    ]

    try:
        logger.info("🚀 Starting Chromium with ultra-stealth settings...")
        logger.info("🔑 Using perfilteste profile with saved login")

        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )

        logger.success("✅ Ultra-stealth browser started!")
        logger.info("👆 Browser window should have opened")
        logger.info("⏳ Waiting for page to load...")

        # Aguardar um tempo para o carregamento completo
        for i in range(15, 0, -1):
            logger.info(f"⏰ {i} seconds remaining...")
            time.sleep(1)

        logger.success("✅ Browser should be ready!")
        logger.info("💡 Now you can:")
        logger.info("   1. Check if you're logged in")
        logger.info("   2. Complete any Cloudflare challenge if needed")
        logger.info("   3. Navigate to travel page")
        logger.info("   4. Run the bot connection test")

        return True

    except Exception as e:
        logger.error(f"❌ Failed to start ultra-stealth browser: {e}")
        return False


def main():
    """Função principal"""
    logger.info("🥷 Ultra Stealth Browser Launcher")
    logger.info("=" * 50)

    logger.info("This will open Chromium with maximum stealth settings")
    logger.info("to bypass Cloudflare protection on SimpleMMO.")
    logger.info("")
    logger.info("Features:")
    logger.info("✅ Ultra-stealth anti-detection")
    logger.info("✅ Uses your perfilteste profile")
    logger.info("✅ Automatic login (if saved)")
    logger.info("✅ Cloudflare bypass optimized")
    logger.info("")

    answer = input("🤔 Start ultra-stealth browser? (y/n): ").lower().strip()

    if answer in ['y', 'yes']:
        if start_ultra_stealth_browser():
            logger.success("🎉 Ultra-stealth browser started successfully!")
            logger.info("🎯 Next steps:")
            logger.info("   1. ✅ Check if SimpleMMO loaded correctly")
            logger.info("   2. ✅ Complete Cloudflare challenge if needed")
            logger.info("   3. ✅ Verify you're logged in")
            logger.info("   4. ✅ Go to travel page")
            logger.info("   5. ✅ Run: python demo_bot_completo.py (option 2 or 3)")
        else:
            logger.error("❌ Failed to start browser")
    else:
        logger.info("👋 Operation cancelled")


if __name__ == "__main__":
    main()
