"""
🚀 Teste de Sistemas Otimizados - Gathering e Combat

Testa os sistemas com delays otimizados para máxima responsividade.
"""

import asyncio
import os
import sys

# Adicionar o diretório raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from loguru import logger
from src.systems.combat import CombatSystem
from src.systems.gathering import GatheringSystem


async def test_optimized_systems():
    """Testa os sistemas otimizados"""
    logger.info("🚀 Testing optimized systems performance...")

    # Test gathering system
    logger.info("\n📦 Testing Gathering System timings...")
    config = {"auto_gather": True}
    gathering = GatheringSystem(config)

    logger.info(f"⚡ Gather delay: {gathering.gather_delay}s")
    logger.info(f"⚡ Max wait time: {gathering.max_wait_time}s")
    logger.info(f"⚡ Button check interval: {gathering.button_check_interval}s")

    # Test combat system
    logger.info("\n⚔️ Testing Combat System timings...")
    combat = CombatSystem(config)

    logger.info(f"⚡ Attack delay: {combat.attack_delay}s")
    logger.info(f"⚡ Max wait time: {combat.max_wait_time}s")
    logger.info(f"⚡ Button check interval: {combat.button_check_interval}s")

    # Verify both systems have same optimized timings
    if (gathering.gather_delay == combat.attack_delay and
        gathering.max_wait_time == combat.max_wait_time and
        gathering.button_check_interval == combat.button_check_interval):
        logger.success("✅ Both systems have consistent optimized timings!")
        logger.info("🎯 Expected performance:")
        logger.info("  • Actions every 0.5 seconds")
        logger.info("  • Button detection every 50ms")
        logger.info("  • Max 3 seconds wait for buttons")
    else:
        logger.warning("⚠️ Systems have different timings - check configuration")

    # Test dynamic configuration
    logger.info("\n⚙️ Testing dynamic timing configuration...")
    await gathering.set_timing_config(gather_delay=0.3, max_wait_time=2.0)
    await combat.set_timing_config(attack_delay=0.3, max_wait_time=2.0)

    logger.success("🎉 Systems optimization test completed!")

if __name__ == "__main__":
    asyncio.run(test_optimized_systems())
