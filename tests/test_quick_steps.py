"""
🔬 Test Quick Steps - Teste rápido do sistema de steps melhorado

Execute este script após fazer login manual com manual_profile_launcher.py
para testar se o bot aguarda corretamente o botão ficar disponível.
"""

import asyncio
import sys
from pathlib import Path

# Add bot root directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from loguru import logger


async def quick_test():
    """Teste rápido e simples"""
    logger.info("🔬 Quick Steps Test")
    logger.info("=" * 40)

    try:
        from botlib import StepSystem, get_web_engine

        # Conectar
        web_engine = await get_web_engine()
        if not web_engine:
            logger.error("❌ No web engine")
            return

        logger.success("✅ Connected to browser")

        # Inicializar steps
        step_system = StepSystem({"step_delay_min": 0.5, "step_delay_max": 1.0})
        await step_system.initialize()

        # Tentar 3 steps consecutivos
        for i in range(3):
            logger.info(f"\n👣 Step {i+1}/3")

            success = await step_system.take_step()

            if success:
                logger.success(f"✅ Step {i+1} OK!")
            else:
                logger.warning(f"⚠️ Step {i+1} failed - may need navigation")
                break

            # Pausa entre steps
            await asyncio.sleep(2)

        # Stats
        stats = step_system.get_step_stats()
        logger.info(f"\n📊 Results: {stats['successful_steps']}/{stats['steps_taken']} successful")

    except Exception as e:
        logger.error(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(quick_test())
