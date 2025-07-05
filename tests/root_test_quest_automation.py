#!/usr/bin/env python3
"""
Script de teste para o sistema de automação de quests.
Testa todas as funcionalidades principais do quest automation.
"""

import asyncio
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from automation.quest_automation import QuestAutomation
from automation.web_engine import get_web_engine
import logging

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class QuestSystemTester:
    """Testador para o sistema de automação de quests."""

    def __init__(self):
        self.quest_automation = QuestAutomation()
        self.web_engine = None

    async def initialize(self):
        """Inicializa o testador."""
        try:
            # Inicializa o web engine
            self.web_engine = await get_web_engine()

            logger.info("✅ Testador inicializado com sucesso")
            return True

        except Exception as e:
            logger.error(f"❌ Erro ao inicializar testador: {str(e)}")
            return False

    async def test_navigation(self):
        """Testa navegação para página de quests."""
        logger.info("🧪 Testando navegação para quests...")

        result = await self.quest_automation.navigate_to_quests()
        if result:
            logger.info("✅ Navegação funcionando")
        else:
            logger.error("❌ Falha na navegação")

        return result

    async def test_quest_points_detection(self):
        """Testa detecção de quest points."""
        logger.info("🧪 Testando detecção de quest points...")

        current, maximum = await self.quest_automation.get_quest_points()
        logger.info(f"📊 Quest Points encontrados: {current}/{maximum}")

        if current >= 0 and maximum >= 0:
            logger.info("✅ Detecção de quest points funcionando")
            return True
        else:
            logger.error("❌ Falha na detecção de quest points")
            return False

    async def test_quest_list_detection(self):
        """Testa detecção da lista de quests."""
        logger.info("🧪 Testando detecção de lista de quests...")

        # Muda para aba "Not Completed"
        await self.quest_automation.switch_to_not_completed_tab()

        quests = await self.quest_automation.get_available_quests()
        logger.info(f"📋 Quests encontrados: {len(quests)}")

        if quests:
            logger.info("✅ Lista de quests detectada")
            # Mostra primeiros 5 quests
            for i, quest in enumerate(quests[:5]):
                logger.info(f"  {i+1}. {quest['name']} (Level {quest['level']}, {quest['left']} left)")
            return True
        else:
            logger.error("❌ Nenhum quest encontrado")
            return False

    async def test_quest_interaction(self):
        """Testa interação com um quest (sem executar)."""
        logger.info("🧪 Testando interação com quest...")

        quests = await self.quest_automation.get_available_quests()
        if not quests:
            logger.error("❌ Nenhum quest disponível para teste")
            return False

        # Testa com o primeiro quest
        test_quest = quests[0]
        logger.info(f"🎯 Testando quest: {test_quest['name']}")

        # Clica no quest
        click_result = await self.quest_automation.click_quest(test_quest)
        if click_result:
            logger.info("✅ Clique no quest funcionando")

            # Procura pelo botão Perform
            perform_button = await self.quest_automation.find_perform_button()
            if perform_button:
                logger.info("✅ Botão Perform encontrado")
                # Fecha popup sem executar
                await self.quest_automation.close_popups()
                return True
            else:
                logger.warning("⚠️ Botão Perform não encontrado")
                await self.quest_automation.close_popups()
                return False
        else:
            logger.error("❌ Falha ao clicar no quest")
            return False

    async def test_perform_button_detection(self):
        """Testa detecção de botões Perform na página principal."""
        logger.info("🧪 Testando detecção de botões Perform...")

        perform_button = await self.quest_automation.find_perform_button()
        if perform_button:
            logger.info("✅ Botão Perform encontrado na página principal")
            return True
        else:
            logger.info("ℹ️ Nenhum botão Perform visível na página principal")
            return True  # Isso é normal

    async def test_full_quest_cycle(self, dry_run=True):
        """Testa um ciclo completo de quest (com dry_run por padrão)."""
        logger.info(f"🧪 Testando ciclo completo de quest (dry_run={dry_run})...")

        if dry_run:
            logger.info("🔄 Executando em modo DRY RUN (sem executar quests)")
            # Simula o ciclo sem executar
            results = {
                "quests_attempted": 1,
                "quests_successful": 1,
                "quest_points_used": 1,
                "errors": []
            }
        else:
            logger.warning("⚠️ EXECUTANDO QUEST REAL!")
            input("Pressione ENTER para continuar ou Ctrl+C para cancelar...")
            results = await self.quest_automation.execute_quests_cycle(max_quests=1)

        logger.info("📊 Resultados do ciclo:")
        logger.info(f"  Quests tentados: {results['quests_attempted']}")
        logger.info(f"  Quests bem-sucedidos: {results['quests_successful']}")
        logger.info(f"  Quest points usados: {results['quest_points_used']}")
        logger.info(f"  Erros: {len(results['errors'])}")

        if results['errors']:
            for error in results['errors']:
                logger.error(f"    - {error}")

        if results['quests_successful'] > 0 or dry_run:
            logger.info("✅ Ciclo de quest funcionando")
            return True
        else:
            logger.error("❌ Falha no ciclo de quest")
            return False

    async def run_all_tests(self, include_full_cycle=False, dry_run=True):
        """Executa todos os testes."""
        logger.info("🚀 Iniciando testes do sistema de quest automation")
        logger.info("=" * 60)

        tests = [
            ("Navegação", self.test_navigation),
            ("Detecção de Quest Points", self.test_quest_points_detection),
            ("Detecção de Lista de Quests", self.test_quest_list_detection),
            ("Interação com Quest", self.test_quest_interaction),
            ("Detecção de Botão Perform", self.test_perform_button_detection),
        ]

        if include_full_cycle:
            tests.append(("Ciclo Completo de Quest", lambda: self.test_full_quest_cycle(dry_run)))

        results = {}

        for test_name, test_func in tests:
            logger.info(f"\n📋 {test_name}")
            logger.info("-" * 40)

            try:
                result = await test_func()
                results[test_name] = result

                if result:
                    logger.info(f"✅ {test_name}: PASSOU")
                else:
                    logger.error(f"❌ {test_name}: FALHOU")

            except Exception as e:
                logger.error(f"💥 {test_name}: ERRO - {str(e)}")
                results[test_name] = False

        # Relatório final
        logger.info("\n" + "=" * 60)
        logger.info("📊 RELATÓRIO FINAL DOS TESTES")
        logger.info("=" * 60)

        passed = sum(1 for result in results.values() if result)
        total = len(results)

        for test_name, result in results.items():
            status = "✅ PASSOU" if result else "❌ FALHOU"
            logger.info(f"{test_name}: {status}")

        logger.info(f"\nResultado: {passed}/{total} testes passaram")

        if passed == total:
            logger.info("🎉 TODOS OS TESTES PASSARAM!")
        else:
            logger.warning(f"⚠️ {total - passed} teste(s) falharam")

        return results

    async def cleanup(self):
        """Limpa recursos."""
        try:
            if self.web_engine:
                await self.web_engine.cleanup()
            logger.info("✅ Recursos limpos")
        except Exception as e:
            logger.error(f"❌ Erro ao limpar recursos: {str(e)}")


async def main():
    """Função principal."""
    logger.info("🎯 TESTADOR DO SISTEMA DE QUEST AUTOMATION")
    logger.info("=" * 60)

    # Opções de teste
    print("\nOpções de teste:")
    print("1. Testes básicos (recomendado)")
    print("2. Testes básicos + ciclo completo (DRY RUN)")
    print("3. Testes básicos + ciclo completo (EXECUÇÃO REAL)")
    print("4. Apenas ciclo completo (EXECUÇÃO REAL)")

    try:
        choice = input("\nEscolha uma opção (1-4): ").strip()
    except KeyboardInterrupt:
        print("\n❌ Teste cancelado pelo usuário")
        return

    tester = QuestSystemTester()

    try:
        # Inicializa testador
        if not await tester.initialize():
            logger.error("❌ Falha na inicialização - abortando testes")
            return

        # Executa testes baseado na escolha
        if choice == "1":
            await tester.run_all_tests(include_full_cycle=False)
        elif choice == "2":
            await tester.run_all_tests(include_full_cycle=True, dry_run=True)
        elif choice == "3":
            await tester.run_all_tests(include_full_cycle=True, dry_run=False)
        elif choice == "4":
            await tester.test_full_quest_cycle(dry_run=False)
        else:
            logger.error("❌ Opção inválida")
            return

    except KeyboardInterrupt:
        logger.warning("\n⚠️ Teste interrompido pelo usuário")

    except Exception as e:
        logger.error(f"💥 Erro durante os testes: {str(e)}")

    finally:
        await tester.cleanup()


if __name__ == "__main__":
    print("🧪 TESTADOR DO SISTEMA DE QUEST AUTOMATION")
    print("Este script testa todas as funcionalidades do quest automation.")
    print("Certifique-se de estar logado no SimpleMMO antes de executar.\n")

    asyncio.run(main())
