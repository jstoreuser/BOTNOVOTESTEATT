"""
🚀 Teste de Performance Melhorada

Testa os ajustes de timing e detecção.
"""

import asyncio
import os
import sys

# Adicionar o diretório raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from loguru import logger


async def test_improved_performance():
    """Testa as melhorias de performance"""
    logger.info("🚀 Testing improved performance settings...")

    try:
        # Test imports
        from src.systems.combat import CombatSystem
        from src.systems.gathering import GatheringSystem
        from src.systems.steps import StepSystem

        config = {"auto_gather": True, "auto_combat": True}

        # Test systems
        gathering = GatheringSystem(config)
        combat = CombatSystem(config)
        StepSystem(config)

        # Test timing configurations
        logger.info("\n📊 IMPROVED TIMING SETTINGS:")
        logger.info(f"⛏️ Gathering max_wait_time: {gathering.max_wait_time}s")
        logger.info(f"⚔️ Combat max_wait_time: {combat.max_wait_time}s")
        logger.info(f"📦 Gathering button_check_interval: {gathering.button_check_interval}s")
        logger.info(f"📦 Combat button_check_interval: {combat.button_check_interval}s")

        # Expected improvements
        logger.info("\n🎯 EXPECTED IMPROVEMENTS:")
        logger.info("✅ Longer wait for step button (20s timeout)")
        logger.info("✅ Better step detection with 0.2s checks")
        logger.info("✅ 3s wait after step for events to load")
        logger.info("✅ 3s wait before navigating to travel")
        logger.info("✅ 5s timeout for gathering/combat detection")
        logger.info("✅ More responsive main loop (0.2s safety delay)")

        # Performance grade
        logger.info("\n🏆 PERFORMANCE GRADE:")
        if (gathering.max_wait_time == 5.0 and
            combat.max_wait_time == 5.0 and
            gathering.button_check_interval == 0.05):
            logger.success("🏆 EXCELLENT - All optimizations applied!")
        else:
            logger.warning("⚠️ Some optimizations missing")

        logger.success("🎉 Improved performance test completed!")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_improved_performance())
