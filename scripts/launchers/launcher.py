#!/usr/bin/env python3
"""
🚀 SimpleMMO Bot - Launcher Principal

Script de lançamento principal para o bot SimpleMMO.
Oferece menu para acessar facilmente todas as funcionalidades.
"""

import os
import subprocess
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from loguru import logger


def show_menu() -> None:
    """Mostra o menu principal"""
    logger.info("🤖 SimpleMMO Bot - Menu Principal")
    logger.info("=" * 50)
    logger.info("")
    logger.info("📋 OPÇÕES PRINCIPAIS:")
    logger.info("  1. 🌐 Abrir browser com perfil (login manual)")
    logger.info("  2. 🤖 Executar bot (conectar ao browser)")
    logger.info("  3. 📋 Ver instruções completas")
    logger.info("")
    logger.info("🧪 TESTES E DEBUGGING:")
    logger.info("  4. 🔬 Teste rápido (3 steps)")
    logger.info("  5. 🧪 Teste completo")
    logger.info("  6. 🔍 Verificar porta de debug")
    logger.info("")
    logger.info("🎮 DEMOS E EXEMPLOS:")
    logger.info("  7. 🎯 Demo bot completo")
    logger.info("  8. 👣 Bot simples (terminal)")
    logger.info("  9. 🌐 Demo browser")
    logger.info("")
    logger.info("  0. 🚪 Sair")
    logger.info("")


def run_script(script_path: str, description: str) -> bool:
    """Executa um script"""
    try:
        logger.info(f"🚀 {description}")
        logger.info(f"📁 Executando: {script_path}")

        if not os.path.exists(script_path):
            logger.error(f"❌ Arquivo não encontrado: {script_path}")
            return False

        # Executa o script
        result = subprocess.run([sys.executable, script_path],
                              check=False, capture_output=False,
                              text=True)

        if result.returncode == 0:
            logger.success("✅ Script executado com sucesso!")
        else:
            logger.warning(f"⚠️ Script terminou com código: {result.returncode}")

        return True

    except Exception as e:
        logger.error(f"❌ Erro ao executar script: {e}")
        return False


def main() -> None:
    """Função principal"""
    while True:
        try:
            show_menu()
            choice = input("👉 Digite sua escolha (0-9): ").strip()

            if choice == "1":
                run_script("scripts/launchers/manual_profile_launcher.py",
                          "Abrindo browser com perfil para login manual")

            elif choice == "2":
                run_script("scripts/launchers/start_bot_with_debugging.py",
                          "Executando bot principal")

            elif choice == "3":
                run_script("scripts/launchers/instructions.py",
                          "Mostrando instruções completas")

            elif choice == "4":
                run_script("scripts/tests/test_quick_steps.py",
                          "Executando teste rápido")

            elif choice == "5":
                run_script("scripts/tests/test_smart_steps.py",
                          "Executando teste completo")

            elif choice == "6":
                run_script("scripts/tests/test_debug_port.py",
                          "Verificando porta de debug")

            elif choice == "7":
                run_script("scripts/demos/demo_bot_completo.py",
                          "Executando demo do bot completo")

            elif choice == "8":
                run_script("scripts/demos/simple_step_bot.py",
                          "Executando bot simples")

            elif choice == "9":
                run_script("scripts/demos/browser_demo.py",
                          "Executando demo do browser")

            elif choice == "0":
                logger.info("👋 Saindo do bot...")
                break

            else:
                logger.warning("⚠️ Opção inválida! Digite um número de 0 a 9.")

            # Pausa antes de mostrar o menu novamente
            if choice != "0":
                input("\n🔄 Pressione Enter para voltar ao menu...")
                print("\n" * 2)  # Espaçamento

        except KeyboardInterrupt:
            logger.info("\n🛑 Interrompido pelo usuário")
            break
        except Exception as e:
            logger.error(f"❌ Erro inesperado: {e}")
            input("🔄 Pressione Enter para continuar...")


if __name__ == "__main__":
    main()
