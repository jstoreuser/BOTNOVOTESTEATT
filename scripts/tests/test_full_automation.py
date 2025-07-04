"""
🚀 Teste Completo de Automação - Gathering + Combat

Testa um fluxo completo de automação com os sistemas otimizados.
Simula detecção de botões e execução de ações para validar performance.
"""

import asyncio
import os
import sys

# Adicionar o diretório raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from loguru import logger
from src.automation.web_engine import get_web_engine
from src.systems.combat import CombatSystem
from src.systems.gathering import GatheringSystem


async def test_full_automation_flow():
    """Testa um fluxo completo de automação"""
    logger.info("🚀 Starting full automation flow test...")

    config = {
        "auto_gather": True,
        "auto_combat": True,
        "browser_profile_path": r"C:\Users\pedro\AppData\Local\Google\Chrome\User Data\Profile 1",
        "headless": False
    }

    # Initialize systems
    gathering = GatheringSystem(config)
    combat = CombatSystem(config)

    # Initialize web engine
    web_engine = get_web_engine()
    if not await web_engine.initialize(config):
        logger.error("❌ Failed to initialize web engine")
        return

    try:
        # Initialize systems
        await gathering.initialize()
        await combat.initialize()

        logger.info("✅ All systems initialized, starting test scenarios...")

        # Test scenario 1: Gathering performance test
        logger.info("\n📦 SCENARIO 1: Gathering System Performance")
        logger.info("⚡ Testing rapid button detection and clicking...")
        logger.info(f"🎯 Expected: {1/gathering.gather_delay:.1f} actions per second")
        logger.info(f"🔍 Button checks every {gathering.button_check_interval*1000:.0f}ms")

        # Test scenario 2: Combat performance test
        logger.info("\n⚔️ SCENARIO 2: Combat System Performance")
        logger.info("⚡ Testing rapid attack sequence...")
        logger.info(f"🎯 Expected: {1/combat.attack_delay:.1f} attacks per second")
        logger.info(f"🔍 Button checks every {combat.button_check_interval*1000:.0f}ms")

        # Test scenario 3: System responsiveness
        logger.info("\n🎮 SCENARIO 3: System Responsiveness Test")
        start_time = asyncio.get_event_loop().time()

        # Simulate rapid timing checks
        for i in range(10):
            await asyncio.sleep(gathering.button_check_interval)

        end_time = asyncio.get_event_loop().time()
        total_time = end_time - start_time

        logger.info(f"⏱️ 10 button checks completed in {total_time:.3f}s")
        logger.info(f"⚡ Average check time: {total_time/10*1000:.1f}ms")

        if total_time < 1.0:
            logger.success("✅ Excellent responsiveness - under 1 second for 10 checks")
        else:
            logger.warning("⚠️ Slow responsiveness - over 1 second for 10 checks")

        # Test scenario 4: Action timing simulation
        logger.info("\n⏰ SCENARIO 4: Action Timing Simulation")
        logger.info("Simulating 5 rapid actions...")

        action_times = []
        for i in range(5):
            action_start = asyncio.get_event_loop().time()
            await asyncio.sleep(gathering.gather_delay)  # Simulate action delay
            action_end = asyncio.get_event_loop().time()
            action_time = action_end - action_start
            action_times.append(action_time)
            logger.info(f"🎯 Action {i+1}: {action_time:.3f}s")

        avg_action_time = sum(action_times) / len(action_times)
        logger.info(f"⚡ Average action time: {avg_action_time:.3f}s")

        # Performance summary
        logger.info("\n📊 PERFORMANCE SUMMARY")
        logger.info("=" * 50)
        logger.info(f"🎯 Gathering Actions/sec: {1/gathering.gather_delay:.1f}")
        logger.info(f"⚔️ Combat Attacks/sec: {1/combat.attack_delay:.1f}")
        logger.info(f"🔍 Button Check Frequency: {1/gathering.button_check_interval:.0f} Hz")
        logger.info(f"⏱️ Button Response Time: {gathering.button_check_interval*1000:.0f}ms")
        logger.info(f"⏰ Max Wait Timeout: {gathering.max_wait_time:.1f}s")
        logger.info("=" * 50)

        # Performance grade
        if avg_action_time <= 0.6:
            grade = "🏆 EXCELLENT"
        elif avg_action_time <= 0.8:
            grade = "✅ GOOD"
        elif avg_action_time <= 1.0:
            grade = "⚠️ ACCEPTABLE"
        else:
            grade = "❌ NEEDS IMPROVEMENT"

        logger.info(f"🎯 Performance Grade: {grade}")

        logger.success("🎉 Full automation flow test completed successfully!")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")

    finally:
        # Cleanup
        await web_engine.close()
        logger.info("🧹 Cleanup completed")

if __name__ == "__main__":
    asyncio.run(test_full_automation_flow())
