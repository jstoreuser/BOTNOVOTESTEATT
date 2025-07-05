"""
🌐 Browser Launcher - SimpleMMO Bot

Script para abrir o navegador na configuração correta para o bot.
Útil para interface gráfica e inicialização manual.
"""

import asyncio
import subprocess
import sys
import time
from pathlib import Path

from loguru import logger

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Browser configuration
BROWSER_CONFIG = {
    "debug_port": 9222,
    "profile_dir": r"C:\temp\BOTNOVOTESTATT",
    "initial_url": "https://web.simple-mmo.com/travel",
    "window_size": "1200,800",
    "window_position": "100,100",
}


def get_chrome_path() -> str | None:
    """Get Chrome executable path"""
    possible_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        rf"C:\Users\{Path.home().name}\AppData\Local\Google\Chrome\Application\chrome.exe",
    ]

    for path in possible_paths:
        if Path(path).exists():
            logger.success(f"✅ Chrome found: {path}")
            return path

    logger.warning("⚠️ Chrome not found in standard locations")
    return None


def get_brave_path() -> str | None:
    """Get Brave executable path"""
    possible_paths = [
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
        rf"C:\Users\{Path.home().name}\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe",
    ]

    for path in possible_paths:
        if Path(path).exists():
            logger.success(f"✅ Brave found: {path}")
            return path

    logger.warning("⚠️ Brave not found in standard locations")
    return None


def create_profile_directory():
    """Create browser profile directory if it doesn't exist"""
    profile_path = Path(BROWSER_CONFIG["profile_dir"])

    if not profile_path.exists():
        logger.info(f"📁 Creating profile directory: {profile_path}")
        profile_path.mkdir(parents=True, exist_ok=True)
        logger.success("✅ Profile directory created")
    else:
        logger.info(f"📁 Profile directory exists: {profile_path}")


def launch_chrome() -> bool:
    """Launch Chrome with bot configuration"""
    chrome_path = get_chrome_path()
    if not chrome_path:
        return False

    create_profile_directory()

    # Chrome command line arguments
    args = [
        chrome_path,
        f"--remote-debugging-port={BROWSER_CONFIG['debug_port']}",
        f"--user-data-dir={BROWSER_CONFIG['profile_dir']}",
        f"--window-size={BROWSER_CONFIG['window_size']}",
        f"--window-position={BROWSER_CONFIG['window_position']}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-renderer-backgrounding",
        "--disable-features=TranslateUI",
        "--disable-extensions",
        "--disable-plugins",
        "--disable-images",  # Para performance
        BROWSER_CONFIG["initial_url"],
    ]

    try:
        logger.info("🚀 Launching Chrome with bot configuration...")
        logger.info(f"🌐 Debug port: {BROWSER_CONFIG['debug_port']}")
        logger.info(f"📁 Profile: {BROWSER_CONFIG['profile_dir']}")
        logger.info(f"🎯 Initial URL: {BROWSER_CONFIG['initial_url']}")

        subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_CONSOLE)

        # Wait a bit for browser to start
        logger.info("⏳ Waiting for Chrome to start...")
        time.sleep(3)

        logger.success("✅ Chrome launched successfully!")
        logger.info("🤖 You can now run the bot - it will connect to this browser")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to launch Chrome: {e}")
        return False


def launch_brave() -> bool:
    """Launch Brave with bot configuration"""
    brave_path = get_brave_path()
    if not brave_path:
        return False

    create_profile_directory()

    # Brave command line arguments (similar to Chrome)
    args = [
        brave_path,
        f"--remote-debugging-port={BROWSER_CONFIG['debug_port']}",
        f"--user-data-dir={BROWSER_CONFIG['profile_dir']}",
        f"--window-size={BROWSER_CONFIG['window_size']}",
        f"--window-position={BROWSER_CONFIG['window_position']}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-renderer-backgrounding",
        "--disable-features=TranslateUI",
        "--disable-extensions",
        "--disable-brave-rewards",  # Brave specific
        "--disable-brave-wallet",  # Brave specific
        BROWSER_CONFIG["initial_url"],
    ]

    try:
        logger.info("🚀 Launching Brave with bot configuration...")
        logger.info(f"🌐 Debug port: {BROWSER_CONFIG['debug_port']}")
        logger.info(f"📁 Profile: {BROWSER_CONFIG['profile_dir']}")
        logger.info(f"🎯 Initial URL: {BROWSER_CONFIG['initial_url']}")

        subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_CONSOLE)

        # Wait a bit for browser to start
        logger.info("⏳ Waiting for Brave to start...")
        time.sleep(3)

        logger.success("✅ Brave launched successfully!")
        logger.info("🤖 You can now run the bot - it will connect to this browser")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to launch Brave: {e}")
        return False


async def test_browser_connection() -> bool:
    """Test if browser is accessible for automation"""
    try:
        # Import web engine to test connection
        from automation.web_engine import get_web_engine

        logger.info("🔗 Testing browser connection...")
        web_engine = await get_web_engine()

        if web_engine:
            page = await web_engine.get_page()
            if page:
                url = page.url
                title = await page.title()
                logger.success("✅ Browser connection successful!")
                logger.info(f"📍 Current URL: {url}")
                logger.info(f"📄 Page title: {title}")
                return True

        logger.error("❌ Browser connection failed")
        return False

    except Exception as e:
        logger.error(f"❌ Browser connection test failed: {e}")
        return False


def launch_browser(browser_type: str = "auto") -> bool:
    """
    Launch browser with bot configuration

    Args:
        browser_type: "chrome", "brave", or "auto" (try both)

    Returns:
        bool: True if browser launched successfully
    """
    logger.info("🌐 Starting Browser Launcher for SimpleMMO Bot")

    if browser_type.lower() == "chrome":
        return launch_chrome()
    elif browser_type.lower() == "brave":
        return launch_brave()
    else:  # auto
        logger.info("🔍 Auto-detecting browser...")

        # Try Chrome first
        if launch_chrome():
            return True

        # Fallback to Brave
        logger.info("🔄 Chrome failed, trying Brave...")
        return launch_brave()


async def launch_and_test(browser_type: str = "auto") -> bool:
    """Launch browser and test connection"""
    if not launch_browser(browser_type):
        return False

    # Wait a bit more for browser to fully load
    logger.info("⏳ Waiting for browser to fully load...")
    await asyncio.sleep(5)

    # Test connection
    return await test_browser_connection()


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Launch browser for SimpleMMO Bot")
    parser.add_argument(
        "--browser",
        choices=["chrome", "brave", "auto"],
        default="auto",
        help="Browser to launch (default: auto)",
    )
    parser.add_argument("--test", action="store_true", help="Test browser connection after launch")
    parser.add_argument("--port", type=int, default=9222, help="Debug port (default: 9222)")
    parser.add_argument(
        "--profile", type=str, default=r"C:\temp\BOTNOVOTESTATT", help="Profile directory path"
    )

    args = parser.parse_args()

    # Update configuration
    BROWSER_CONFIG["debug_port"] = args.port
    BROWSER_CONFIG["profile_dir"] = args.profile

    logger.info("🚀 SimpleMMO Bot - Browser Launcher")
    logger.info(f"⚙️ Browser: {args.browser}")
    logger.info(f"🌐 Port: {args.port}")
    logger.info(f"📁 Profile: {args.profile}")

    try:
        if args.test:
            # Launch and test
            success = asyncio.run(launch_and_test(args.browser))
        else:
            # Just launch
            success = launch_browser(args.browser)

        if success:
            logger.success("🎉 Browser launcher completed successfully!")
            logger.info("💡 Next steps:")
            logger.info("   1. Login to SimpleMMO in the browser")
            logger.info("   2. Navigate to the travel page")
            logger.info("   3. Run the bot: python src/main.py")
        else:
            logger.error("❌ Browser launcher failed")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("🛑 Browser launcher stopped by user")
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
