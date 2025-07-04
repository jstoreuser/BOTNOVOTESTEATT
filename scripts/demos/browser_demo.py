"""
🌐 Demo do Bot com Browser do Sistema

Este script abre o browser do sistema (Chrome/Edge) para você ver o bot funcionando.
Muito mais fácil de ver e debugar do que tentar dentro do VS Code.
"""

import time
import webbrowser

from loguru import logger


def open_browser_demo():
    """
    🚀 Abre o browser do sistema para demonstração
    """
    try:
        logger.info("🌐 Opening system browser for bot demo...")

        # URL do SimpleMMO
        url = "https://web.simple-mmo.com/travel"

        logger.info(f"📍 Opening: {url}")

        # Abre no browser padrão do sistema
        webbrowser.open(url)

        logger.success("✅ Browser opened!")
        logger.info("👀 You should see SimpleMMO opening in your default browser")
        logger.info("🎮 This is where the Playwright bot would work")
        logger.info("📝 To see the actual bot working:")
        logger.info("   1. Make sure you're logged into SimpleMMO")
        logger.info("   2. Navigate to the travel page")
        logger.info("   3. Run the Playwright bot scripts")

        # Aguarda um pouco
        time.sleep(2)

        logger.info("💡 Tips for bot development:")
        logger.info("   • Use browser developer tools (F12) to inspect elements")
        logger.info("   • Check for 'Take a step' buttons")
        logger.info("   • Look for attack, gather, and heal elements")
        logger.info("   • The bot will interact with these elements automatically")

        return True

    except Exception as e:
        logger.error(f"❌ Error opening browser: {e}")
        return False


def show_bot_architecture():
    """
    📋 Mostra a arquitetura do bot
    """
    logger.info("🏗️ Bot Architecture:")
    logger.info("   📁 src/core/")
    logger.info("      🌐 web_engine.py     - Playwright automation")
    logger.info("      👣 steps.py          - Step taking system")
    logger.info("      ⚔️ combat.py         - Combat system")
    logger.info("      ⛏️ gathering.py      - Resource gathering")
    logger.info("      💊 healing.py        - Health management")
    logger.info("      🔒 captcha.py        - Captcha detection")
    logger.info("      🎯 context.py        - Bot state management")
    logger.info("")
    logger.info("   📁 src/ui/")
    logger.info("      🖥️ gui.py           - Main interface")
    logger.info("      📱 simple_gui.py    - Simple interface")
    logger.info("")
    logger.info("   🎮 Main Scripts:")
    logger.info("      🚀 src/main.py       - Full bot")
    logger.info("      👣 simple_step_bot.py - Step-only bot")
    logger.info("      🧪 visual_test.py    - Browser test")


def main():
    """Main function"""
    logger.info("🎮 SimpleMMO Bot - Browser Demo")
    logger.info("=" * 50)

    # Show architecture
    show_bot_architecture()
    logger.info("=" * 50)

    # Open browser
    if open_browser_demo():
        logger.success("✅ Demo completed successfully!")
        logger.info("🔥 The bot is ready to work with Playwright!")
    else:
        logger.error("❌ Demo failed")


if __name__ == "__main__":
    main()
