"""
🧪 Test Gathering System - Testa o novo sistema de coleta completo

Este script testa o sistema de gathering que:
1. Detecta botões de coleta (chop, mine, salvage, catch) na página de travel
2. Clica no botão e entra na página de gathering
3. Verifica o available_amount
4. Executa múltiplos cliques no "Press here to gather"
5. Fecha a página e volta para travel
"""

import asyncio
import sys
from pathlib import Path

# Add bot root directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from loguru import logger


async def test_gathering_system():
    """Testa o sistema completo de gathering"""
    logger.info("🧪 Testing Gathering System")
    logger.info("=" * 50)

    try:
        from botlib import GatheringSystem, get_web_engine

        # Conectar ao browser
        logger.info("🔗 Connecting to browser...")
        web_engine = await get_web_engine()

        if not web_engine:
            logger.error("❌ No web engine available")
            return

        logger.success("✅ Connected to browser")

        # Configuração do sistema de gathering
        config = {
            "auto_gather": True,
            "gather_delay": 1.5,
            "max_wait_time": 10.0,
        }

        # Inicializar sistema de gathering
        logger.info("⛏️ Initializing gathering system...")
        gathering_system = GatheringSystem(config)
        await gathering_system.initialize()

        logger.success("✅ Gathering system initialized")

        # Verificar se estamos na página de travel
        page = await web_engine.get_page()
        current_url = page.url
        logger.info(f"📍 Current URL: {current_url}")

        # Verificar se há oportunidades de gathering
        logger.info("🔍 Checking for gathering opportunities...")
        is_available = await gathering_system.is_gathering_available()
        logger.info(f"⛏️ Gathering available: {is_available}")

        if is_available:
            logger.info("🎯 Found gathering opportunity!")

            # Obter informações de gathering
            gather_info = await gathering_system.get_gather_info()
            logger.info(f"📊 Gather info: {gather_info}")

            # Confirmar se o usuário quer executar o gathering
            logger.info("🤔 Ready to start gathering process...")
            logger.info("   This will:")
            logger.info("   1. Click a gathering button (chop/mine/salvage/catch)")
            logger.info("   2. Enter gathering page")
            logger.info("   3. Collect all available materials")
            logger.info("   4. Return to travel page")

            # Executar gathering
            logger.info("🚀 Starting gathering process...")
            success = await gathering_system.start_gathering()

            if success:
                logger.success("✅ Gathering completed successfully!")
            else:
                logger.warning("⚠️ Gathering failed or no materials available")

        else:
            logger.info("📝 No gathering opportunities available on this page")
            logger.info("   Try navigating to a travel page with gather buttons")

        # Obter informações finais
        final_info = await gathering_system.get_gather_info()
        logger.info(f"📊 Final gather info: {final_info}")

        logger.success("✅ Gathering system test completed")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        logger.exception("Full error traceback:")


def main():
    """Função principal"""
    try:
        logger.info("🧪 Gathering System Test")
        logger.info("=" * 30)

        logger.info("This test will:")
        logger.info("1. 🔗 Connect to existing browser")
        logger.info("2. ⛏️ Initialize gathering system")
        logger.info("3. 🔍 Check for gathering opportunities")
        logger.info("4. 🚀 Execute gathering if available")
        logger.info("")

        asyncio.run(test_gathering_system())

    except KeyboardInterrupt:
        logger.info("🛑 Test stopped by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        logger.exception("Full error traceback:")


if __name__ == "__main__":
    main()
