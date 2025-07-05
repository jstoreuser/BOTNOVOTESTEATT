"""
🤖 Teste do Sistema Unificado - Step-Based Automation

Testa o fluxo unificado:
1. Step → Evento
2. Verificar gathering/combat
3. Executar ação
4. Repetir

Deve conectar ao navegador existente.
"""

import asyncio
import os
import sys

# Adicionar o diretório raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import builtins
import contextlib

from loguru import logger
from src.automation.web_engine import get_web_engine
from src.systems.captcha import CaptchaSystem
from src.systems.combat import CombatSystem
from src.systems.gathering import GatheringSystem
from src.systems.steps import StepSystem


async def test_unified_system():
    """Testa o sistema unificado step-based"""
    logger.info("🤖 Testing Unified Step-Based System")
    logger.info("=" * 50)

    config = {
        "auto_gather": True,
        "auto_combat": True,
        "auto_step": True
    }

    try:
        # Initialize web engine (connect to existing browser)
        logger.info("🔗 Connecting to existing browser...")
        web_engine = await get_web_engine()
        if not await web_engine.initialize():
            logger.error("❌ Failed to connect to browser")
            return

        logger.success("✅ Connected to browser")

        # Initialize systems
        logger.info("🔧 Initializing systems...")
        steps = StepSystem(config)
        gathering = GatheringSystem(config)
        combat = CombatSystem(config)
        captcha = CaptchaSystem(config)

        await steps.initialize()
        await gathering.initialize()
        await combat.initialize()
        await captcha.initialize()

        logger.success("✅ All systems initialized")

        # Get current page info
        page = await web_engine.get_page()
        if page:
            current_url = page.url
            logger.info(f"📍 Current URL: {current_url}")

        # Test the unified flow for a few cycles
        logger.info("\n🚀 Starting unified automation test (5 cycles)...")

        for cycle in range(1, 6):
            logger.info(f"\n🔄 === CYCLE {cycle} ===")

            # Check captcha first
            captcha_present = await captcha.is_captcha_present()
            logger.info(f"🔒 Captcha present: {captcha_present}")

            if captcha_present:
                logger.warning("🔒 Captcha detected - skipping this cycle")
                continue

            # Check gathering
            gathering_available = await gathering.is_gathering_available()
            logger.info(f"⛏️ Gathering available: {gathering_available}")

            if gathering_available:
                logger.info("🎯 EXECUTING: Gathering")
                success = await gathering.start_gathering()
                logger.info(f"✅ Gathering result: {success}")
                if success:
                    logger.info("💡 After gathering = like taking a step, checking for new events...")
                    await asyncio.sleep(1)
                    continue

            # Check combat
            combat_available = await combat.is_combat_available()
            logger.info(f"⚔️ Combat available: {combat_available}")

            if combat_available:
                logger.info("🎯 EXECUTING: Combat")
                success = await combat.start_combat()
                logger.info(f"✅ Combat result: {success}")
                if success:
                    logger.info("💡 After combat = like taking a step, checking for new events...")
                    await asyncio.sleep(1)
                    continue

            # If no events, take a step
            step_available = await steps.is_step_available()
            logger.info(f"👣 Step available: {step_available}")

            if step_available:
                logger.info("🎯 EXECUTING: Take Step (no events found)")
                success = await steps.take_step()
                logger.info(f"✅ Step result: {success}")
                if success:
                    logger.info("💡 Step taken, waiting for new event to appear...")
                    await asyncio.sleep(2)
                else:
                    logger.warning("⚠️ Step failed")
            else:
                logger.info("🎯 EXECUTING: Navigate to travel")
                await steps.navigate_to_travel()
                await asyncio.sleep(2)

            # Small delay between cycles
            await asyncio.sleep(1)

        logger.success("\n🎉 Unified system test completed!")

        # Get final stats
        logger.info("\n📊 FINAL STATS:")
        gathering_stats = gathering.get_gathering_stats()
        combat_stats = combat.get_combat_stats()

        logger.info(f"⛏️ Gathering stats: {gathering_stats}")
        logger.info(f"⚔️ Combat stats: {combat_stats}")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        logger.exception("Full traceback:")

    finally:
        logger.info("🧹 Cleaning up...")
        with contextlib.suppress(builtins.BaseException):
            await web_engine.close()

if __name__ == "__main__":
    asyncio.run(test_unified_system())
