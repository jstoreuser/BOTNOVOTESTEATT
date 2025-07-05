"""
🧪 Test Smart Steps - Testa o novo sistema de steps com espera inteligente

Este script testa se o novo método wait_for_step_button consegue
aguardar o botão "Take a step" ficar disponível antes de navegar para travel.
"""

import asyncio
import sys
from pathlib import Path

# Add bot root directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from loguru import logger


async def test_smart_steps():
    """Testa o sistema de steps com espera inteligente"""
    logger.info("🧪 Testing Smart Steps System")
    logger.info("=" * 50)

    try:
        from botlib import StepSystem, get_web_engine

        # Conectar ao browser
        logger.info("🔗 Connecting to browser...")
        web_engine = await get_web_engine()

        if not web_engine or not web_engine.is_initialized:
            logger.error("❌ Failed to connect to browser")
            logger.info("💡 Make sure browser is open with manual_profile_launcher.py")
            return False

        page = await web_engine.get_page()
        current_url = page.url
        logger.success(f"✅ Connected! Current URL: {current_url}")

        # Inicializar sistema de steps
        step_config = {
            "step_delay_min": 1.0,
            "step_delay_max": 2.0,
            "travel_url": "https://web.simple-mmo.com/travel"
        }

        step_system = StepSystem(step_config)
        await step_system.initialize()
        logger.success("✅ Step system initialized!")

        # Test 1: Verificar detecção de botão
        logger.info("\n🧪 Test 1: Step button detection")
        is_available = await step_system.is_step_available()
        logger.info(f"   Step available: {is_available}")

        # Test 2: Aguardar botão (se não disponível)
        if not is_available:
            logger.info("\n🧪 Test 2: Waiting for step button")
            if await step_system.wait_for_step_button(timeout=10.0):
                logger.success("   ✅ Button became available!")
            else:
                logger.warning("   ⏰ Button didn't become available")

        # Test 3: Tentar dar um step
        logger.info("\n🧪 Test 3: Taking a step with smart waiting")
        success = await step_system.take_step(fast_mode=True)

        if success:
            logger.success("   ✅ Step taken successfully!")
        else:
            logger.warning("   ⚠️ Step failed or not available")

        # Test 4: Aguardar próximo step ficar disponível
        logger.info("\n🧪 Test 4: Waiting for next step button")
        if await step_system.wait_for_step_button(timeout=20.0):
            logger.success("   ✅ Next step button is ready!")

            # Tentar mais um step
            success2 = await step_system.take_step(fast_mode=True)
            if success2:
                logger.success("   ✅ Second step taken!")
            else:
                logger.warning("   ⚠️ Second step failed")
        else:
            logger.warning("   ⏰ Next step button didn't become available")

        # Estatísticas
        stats = step_system.get_step_stats()
        logger.info("\n📊 Test Results:")
        logger.info(f"   • Steps attempted: {stats.get('steps_taken', 0)}")
        logger.info(f"   • Successful: {stats.get('successful_steps', 0)}")
        logger.info(f"   • Failed: {stats.get('failed_steps', 0)}")

        return True

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        return False


async def main():
    """Função principal"""
    logger.info("🧪 Smart Steps Test")
    logger.info("=" * 50)

    success = await test_smart_steps()

    if success:
        logger.success("\n✅ All tests completed!")
    else:
        logger.error("\n❌ Tests failed!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Test interrupted by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
