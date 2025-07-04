"""
🔧 Manual Profile Launcher - Sem Bot        logger.success("✅ Chromium opened with perfilteste profile!")
        logger.info("👆 A Chromium window should have opened")
        logger.info("📡 Debugging port 9222 is active")
        logger.info("")
        logger.info("📋 Steps to complete:")
        logger.info("   1. ✅ Complete Cloudflare challenge manually")
        logger.info("   2. ✅ Login to your SimpleMMO account")
        logger.info("   3. ✅ Navigate to the travel page (or stay there)")
        logger.info("   4. ✅ Make sure you see 'Take a step' buttons")
        logger.info("   5. ✅ Keep this browser window open")
        logger.info("")
        logger.info("💡 After completing login, run:")
        logger.info("   python start_bot_with_debugging.py")
        logger.info("")
        logger.warning("⚠️ DO NOT CLOSE this browser window!")
        logger.warning("⚠️ The bot will connect to this same window later")apenas abre o Chromium com o perfil perfilteste
para você fazer login manualmente SEM interferência do bot.
"""

import subprocess

from loguru import logger


def start_manual_profile():
    """Inicia o perfil manualmente para login sem bot"""
    logger.info("🔧 Starting Manual Profile Session")
    logger.info("=" * 50)

    chromium_path = r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\chrome.exe"
    user_data_dir = r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\User Data"

    # Comando com debugging habilitado desde o início
    command = [
        chromium_path,
        "--remote-debugging-port=9222",  # Debugging habilitado
        f"--user-data-dir={user_data_dir}",
        "--profile-directory=perfilteste",
        "--no-first-run",
        "--no-default-browser-check",
        "https://web.simple-mmo.com/travel"  # Ir direto para travel
    ]

    try:
        logger.info("🚀 Opening Chromium with perfilteste profile...")
        logger.info("📍 URL: https://web.simple-mmo.com/travel")
        logger.info("🔑 You can now login manually - debugging already enabled")
        logger.info("📡 Debug port 9222 active for bot connection later")

        subprocess.Popen(
            command,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )

        logger.success("✅ Chromium opened with perfilteste profile!")
        logger.info("👆 A clean Chromium window should have opened")
        logger.info("")
        logger.info("📋 Steps to complete:")
        logger.info("   1. ✅ Complete Cloudflare challenge manually")
        logger.info("   2. ✅ Login to your SimpleMMO account")
        logger.info("   3. ✅ Navigate to the travel page")
        logger.info("   4. ✅ Make sure you see 'Take a step' buttons")
        logger.info("   5. ✅ Keep this browser window open")
        logger.info("")
        logger.info("💡 After completing login, run:")
        logger.info("   python start_bot_with_debugging.py")
        logger.info("")
        logger.warning("⚠️ DO NOT CLOSE this browser window!")
        logger.warning("⚠️ The bot will connect to this same window later")

        return True

    except Exception as e:
        logger.error(f"❌ Failed to start manual profile: {e}")
        return False


def main():
    """Função principal"""
    logger.info("🔧 Manual Profile Launcher")
    logger.info("=" * 40)

    logger.info("This script opens a CLEAN browser window with your")
    logger.info("perfilteste profile for manual login WITHOUT any bot.")
    logger.info("")
    logger.info("✅ No debugging ports")
    logger.info("✅ No automation flags")
    logger.info("✅ No bot interference")
    logger.info("✅ Clean manual login experience")
    logger.info("")

    answer = input("🤔 Open clean browser for manual login? (y/n): ").lower().strip()

    if answer in ['y', 'yes']:
        if start_manual_profile():
            logger.success("🎉 Browser opened successfully!")
            logger.info("")
            logger.info("🎯 Next steps:")
            logger.info("   1. Complete login in the browser that opened")
            logger.info("   2. Navigate to travel page")
            logger.info("   3. Keep browser open")
            logger.info("   4. Run: python start_bot_with_debugging.py")
            logger.info("")
            logger.info("⏰ Take your time - no rush!")
        else:
            logger.error("❌ Failed to open browser")
    else:
        logger.info("👋 Operation cancelled")


if __name__ == "__main__":
    main()
