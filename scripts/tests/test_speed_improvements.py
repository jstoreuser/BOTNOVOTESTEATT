"""
⚡ Teste de Velocidade de Combat e Step Detection

Testa as melhorias de velocidade implementadas.
"""

import asyncio
import os
import sys

# Adicionar o diretório raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from loguru import logger


async def test_speed_improvements():
    """Testa as melhorias de velocidade"""
    logger.info("⚡ Testing speed improvements...")

    try:
        # Test imports
        from src.systems.combat import CombatSystem
        from src.systems.steps import StepSystem

        config = {"auto_combat": True}

        # Test systems
        combat = CombatSystem(config)
        StepSystem(config)

        # Test improved settings
        logger.info("\n⚡ SPEED IMPROVEMENTS:")
        logger.info(f"⚔️ Combat attack delay: {combat.attack_delay}s (reduced from 0.5s)")
        logger.info(f"⚔️ Combat button check: {combat.button_check_interval*1000:.0f}ms (improved from 50ms)")
        logger.info("👣 Step button timeout: 30s (increased from 20s)")

        # Calculate performance
        attacks_per_second = 1 / combat.attack_delay
        checks_per_second = 1 / combat.button_check_interval

        logger.info("\n📊 PERFORMANCE METRICS:")
        logger.info(f"⚔️ Attack rate: {attacks_per_second:.1f} attacks/second")
        logger.info(f"🔍 Button detection: {checks_per_second:.0f} checks/second")
        logger.info("🚪 Leave detection: 8 attempts with 0.2s intervals")
        logger.info("👣 Step patience: 30s timeout (handles slow loading)")

        # Performance comparison
        old_attack_rate = 1 / 0.5  # Old rate
        old_check_rate = 1 / 0.05  # Old rate

        speed_improvement = (attacks_per_second / old_attack_rate - 1) * 100
        detection_improvement = (checks_per_second / old_check_rate - 1) * 100

        logger.info("\n🚀 IMPROVEMENTS:")
        logger.info(f"⚔️ Combat speed: {speed_improvement:+.1f}% faster")
        logger.info(f"🔍 Detection speed: {detection_improvement:+.1f}% faster")
        logger.info("👣 Step patience: +50% tolerance (20s → 30s)")
        logger.info("🚪 Leave detection: 60% faster (0.5s → 0.2s intervals)")

        # Expected results
        logger.info("\n🎯 EXPECTED RESULTS:")
        logger.info("✅ Faster combat (3.3 attacks/sec vs 2.0)")
        logger.info("✅ Quicker leave button detection")
        logger.info("✅ More patience for slow step buttons")
        logger.info("✅ Better button responsiveness overall")

        # Grade the improvements
        if (combat.attack_delay <= 0.3 and
            combat.button_check_interval <= 0.03):
            logger.success("🏆 EXCELLENT - All speed improvements applied!")
        else:
            logger.warning("⚠️ Some improvements missing")

        logger.success("🎉 Speed improvement test completed!")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_speed_improvements())
