"""
🧪 Test Combat System - Testa o novo sistema de combate completo

Este script testa o sistema de combate que:
1. Detecta botões de attack na página de travel
2. Clica no botão e entra na página de combate
3. Verifica o HP do inimigo
4. Executa múltiplos ataques até o HP zerar
5. Clica em "Leave" e volta para travel
"""

import asyncio
import sys
from pathlib import Path

# Add bot root directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from loguru import logger


async def test_combat_system():
    """Testa o sistema completo de combate"""
    logger.info("🧪 Testing Combat System")
    logger.info("=" * 50)

    try:
        from botlib import CombatSystem, get_web_engine

        # Conectar ao browser
        logger.info("🔗 Connecting to browser...")
        web_engine = await get_web_engine()

        if not web_engine:
            logger.error("❌ No web engine available")
            return

        logger.success("✅ Connected to browser")

        # Configuração do sistema de combate
        config = {
            "auto_combat": True,
            "attack_delay": 0.8,
            "max_wait_time": 5.0,
        }

        # Inicializar sistema de combate
        logger.info("⚔️ Initializing combat system...")
        combat_system = CombatSystem(config)
        await combat_system.initialize()

        logger.success("✅ Combat system initialized")

        # Verificar se estamos na página de travel
        page = await web_engine.get_page()
        current_url = page.url
        logger.info(f"📍 Current URL: {current_url}")

        # Verificar se há oportunidades de combate
        logger.info("🔍 Checking for combat opportunities...")
        is_available = await combat_system.is_combat_available()
        logger.info(f"⚔️ Combat available: {is_available}")

        if is_available:
            logger.info("🎯 Found combat opportunity!")

            # Obter informações de combate
            combat_info = await combat_system.get_combat_info()
            logger.info(f"📊 Combat info: {combat_info}")

            # Confirmar se o usuário quer executar o combate
            logger.info("🤔 Ready to start combat process...")
            logger.info("   This will:")
            logger.info("   1. Click an attack button")
            logger.info("   2. Enter combat page")
            logger.info("   3. Attack until enemy HP reaches 0%")
            logger.info("   4. Leave and return to travel page")

            # Executar combate
            logger.info("🚀 Starting combat process...")
            success = await combat_system.start_combat()

            if success:
                logger.success("✅ Combat completed successfully!")

                # Mostrar estatísticas
                stats = combat_system.get_combat_stats()
                logger.info(f"📊 Combat stats: {stats}")
            else:
                logger.warning("⚠️ Combat failed or enemy already defeated")

        else:
            logger.info("📝 No combat opportunities available on this page")
            logger.info("   Try navigating to a travel page with attack buttons")

        # Obter informações finais
        final_info = await combat_system.get_combat_info()
        logger.info(f"📊 Final combat info: {final_info}")

        logger.success("✅ Combat system test completed")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        logger.exception("Full error traceback:")


def main():
    """Função principal"""
    try:
        logger.info("🧪 Combat System Test")
        logger.info("=" * 30)

        logger.info("This test will:")
        logger.info("1. 🔗 Connect to existing browser")
        logger.info("2. ⚔️ Initialize combat system")
        logger.info("3. 🔍 Check for combat opportunities")
        logger.info("4. 🚀 Execute combat if available")
        logger.info("")

        asyncio.run(test_combat_system())

    except KeyboardInterrupt:
        logger.info("🛑 Test stopped by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        logger.exception("Full error traceback:")


if __name__ == "__main__":
    main()
