"""
⚡ Teste Rápido de Performance - Sistemas Otimizados

Testa apenas a performance dos sistemas sem navegador.
Foca na responsividade e timings otimizados.
"""

import asyncio
import os
import sys
import time

# Adicionar o diretório raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from loguru import logger
from src.systems.combat import CombatSystem
from src.systems.gathering import GatheringSystem


async def test_performance_only():
    """Testa apenas performance dos sistemas"""
    logger.info("⚡ Starting performance-only test...")

    config = {"auto_gather": True, "auto_combat": True}

    # Initialize systems
    gathering = GatheringSystem(config)
    combat = CombatSystem(config)

    await gathering.initialize()
    await combat.initialize()

    logger.info("✅ Systems initialized, testing performance...")

    # Test 1: Timing consistency
    logger.info("\n🎯 TEST 1: Timing Consistency")
    logger.info(f"Gathering delay: {gathering.gather_delay}s")
    logger.info(f"Combat delay: {combat.attack_delay}s")
    logger.info(f"Button check interval: {gathering.button_check_interval}s")

    # Test 2: Rapid operation simulation
    logger.info("\n⚡ TEST 2: Rapid Operation Simulation")
    start_time = time.time()

    # Simulate 10 rapid button checks
    for i in range(10):
        await asyncio.sleep(gathering.button_check_interval)
        if i % 2 == 0:
            logger.debug(f"Button check {i+1} completed")

    end_time = time.time()
    total_time = end_time - start_time

    logger.info(f"⏱️ 10 button checks: {total_time:.3f}s")
    logger.info(f"⚡ Average: {total_time/10*1000:.1f}ms per check")

    # Test 3: Action rate calculation
    logger.info("\n📊 TEST 3: Action Rate Calculation")

    actions_per_second_gather = 1 / gathering.gather_delay
    actions_per_second_combat = 1 / combat.attack_delay
    checks_per_second = 1 / gathering.button_check_interval

    logger.info(f"🎯 Gathering rate: {actions_per_second_gather:.1f} actions/sec")
    logger.info(f"⚔️ Combat rate: {actions_per_second_combat:.1f} attacks/sec")
    logger.info(f"🔍 Check rate: {checks_per_second:.0f} checks/sec")

    # Test 4: System responsiveness grade
    logger.info("\n🏆 TEST 4: Performance Grade")

    # Calculate overall performance score
    if gathering.gather_delay <= 0.5 and combat.attack_delay <= 0.5:
        speed_score = 100
    elif gathering.gather_delay <= 0.8 and combat.attack_delay <= 0.8:
        speed_score = 80
    else:
        speed_score = 60

    if gathering.button_check_interval <= 0.05:
        responsiveness_score = 100
    elif gathering.button_check_interval <= 0.1:
        responsiveness_score = 80
    else:
        responsiveness_score = 60

    if gathering.max_wait_time <= 3.0:
        efficiency_score = 100
    elif gathering.max_wait_time <= 5.0:
        efficiency_score = 80
    else:
        efficiency_score = 60

    overall_score = (speed_score + responsiveness_score + efficiency_score) / 3

    logger.info(f"🎯 Speed Score: {speed_score}/100")
    logger.info(f"⚡ Responsiveness Score: {responsiveness_score}/100")
    logger.info(f"⏱️ Efficiency Score: {efficiency_score}/100")
    logger.info(f"🏆 Overall Score: {overall_score:.1f}/100")

    if overall_score >= 90:
        grade = "🏆 EXCELLENT"
        color = "success"
    elif overall_score >= 80:
        grade = "✅ GOOD"
        color = "success"
    elif overall_score >= 70:
        grade = "⚠️ ACCEPTABLE"
        color = "warning"
    else:
        grade = "❌ NEEDS IMPROVEMENT"
        color = "error"

    if color == "success":
        logger.success(f"Final Grade: {grade}")
    elif color == "warning":
        logger.warning(f"Final Grade: {grade}")
    else:
        logger.error(f"Final Grade: {grade}")

    # Test 5: Dynamic reconfiguration
    logger.info("\n⚙️ TEST 5: Dynamic Reconfiguration")
    logger.info("Testing dynamic timing adjustments...")

    # Test faster settings
    await gathering.set_timing_config(gather_delay=0.3, max_wait_time=2.0)
    await combat.set_timing_config(attack_delay=0.3, max_wait_time=2.0)

    logger.info(f"🚀 New gathering rate: {1/gathering.gather_delay:.1f} actions/sec")
    logger.info(f"🚀 New combat rate: {1/combat.attack_delay:.1f} attacks/sec")

    # Reset to optimized settings
    await gathering.set_timing_config(gather_delay=0.5, max_wait_time=3.0)
    await combat.set_timing_config(attack_delay=0.5, max_wait_time=3.0)

    logger.info("✅ Reset to optimized settings")

    logger.success("🎉 Performance test completed successfully!")

    return {
        "overall_score": overall_score,
        "grade": grade,
        "gathering_rate": actions_per_second_gather,
        "combat_rate": actions_per_second_combat,
        "check_rate": checks_per_second,
        "button_response_time": gathering.button_check_interval * 1000  # ms
    }

if __name__ == "__main__":
    result = asyncio.run(test_performance_only())
    print(f"\n🎯 Final Result: {result}")
