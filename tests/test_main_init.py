"""
🧪 Teste Rápido do Main.py

Testa se o main.py consegue inicializar todos os sistemas
sem conectar ao navegador.
"""

import asyncio
import os
import sys

# Adicionar o diretório raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from loguru import logger


async def test_main_initialization():
    """Testa se o main consegue inicializar os sistemas"""
    logger.info("🧪 Testing main.py initialization...")

    try:
        # Import systems (test imports)
        logger.info("📦 Testing imports...")
        from src.config.context import ContextSystem
        from src.systems.captcha import CaptchaSystem
        from src.systems.combat import CombatSystem
        from src.systems.gathering import GatheringSystem
        from src.systems.healing import HealingSystem
        from src.systems.steps import StepSystem
        logger.success("✅ All imports successful")

        # Test configuration
        logger.info("⚙️ Testing configuration...")
        config = {
            "bot_name": "SimpleMMO Bot Modern",
            "log_level": "INFO",
            "browser_headless": False,
            "auto_heal": True,
            "auto_gather": True,
            "auto_combat": True,
        }
        logger.success("✅ Configuration created")

        # Test system initialization
        logger.info("🔧 Testing system initialization...")
        ContextSystem(config)
        gathering = GatheringSystem(config)
        healing = HealingSystem(config)
        steps = StepSystem(config)
        combat = CombatSystem(config)
        captcha = CaptchaSystem(config)
        logger.success("✅ All systems created")

        # Test system initialization (without web engine)
        logger.info("🔧 Testing system initialization methods...")
        await gathering.initialize()
        await healing.initialize()
        await steps.initialize()
        await combat.initialize()
        await captcha.initialize()
        logger.success("✅ All systems initialized")

        # Test system methods (basic calls)
        logger.info("🧪 Testing system methods...")

        # These should work without web engine
        combat_stats = combat.get_combat_stats()
        logger.info(f"📊 Combat stats: {combat_stats}")

        # Test gather info (async method)
        try:
            gather_info = await gathering.get_gather_info()
            logger.info(f"📊 Gather info: {gather_info}")
        except Exception as e:
            logger.debug(f"Gather info failed (expected without web engine): {e}")

        logger.success("🎉 Main.py initialization test passed!")
        return True

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        logger.exception("Full error:")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_main_initialization())
    if success:
        print("\n✅ Main.py is ready to run!")
    else:
        print("\n❌ Main.py has issues!")
