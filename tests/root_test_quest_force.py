#!/usr/bin/env python3
"""
🎯 TESTE FORÇADO DO SISTEMA DE QUEST AUTOMATION
===============================================

Script standalone para testar imediatamente o sistema de quest automation
sem precisar esperar o ciclo normal do bot ou modificar arquivos.

Uso:
    python test_quest_force.py

Funcionalidades:
- ✅ Inicialização rápida do sistema
- ✅ Teste de navegação para quests
- ✅ Detecção de quest points
- ✅ Listagem de quests disponíveis
- ✅ Teste de interação (opcional)
- ✅ Confirmação manual do usuário
- ✅ Relatório detalhado
"""

import asyncio
import sys
import os
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent / "src"))

from automation.web_engine import get_web_engine, WebAutomationEngine
from automation.quest_automation import QuestAutomation
from config.types import BotConfig
from typing import List, Dict, Any


class QuestTester:
    """Testador standalone para quest automation"""

    def __init__(self):
        self.web_engine: WebAutomationEngine | None = None
        self.quest_automation: QuestAutomation | None = None
        self.config = BotConfig()

    async def initialize(self):
        """Inicializa os sistemas necessários"""
        print("🚀 Inicializando sistemas de teste...")

        try:
            # Obter web engine singleton
            self.web_engine = await get_web_engine()
            print("✅ Web Engine obtido")

            # Inicializar quest automation
            self.quest_automation = QuestAutomation()
            print("✅ Quest Automation inicializado")

            return True

        except Exception as e:
            print(f"❌ Erro na inicialização: {e}")
            return False

    async def test_navigation(self):
        """Testa navegação para página de quests"""
        print("\n📍 Testando navegação para quests...")

        try:
            success = await self.quest_automation.navigate_to_quests()
            if success:
                print("✅ Navegação para quests bem-sucedida")
                return True
            else:
                print("❌ Falha na navegação para quests")
                return False

        except Exception as e:
            print(f"❌ Erro na navegação: {e}")
            return False

    async def test_quest_points(self):
        """Testa detecção de quest points"""
        print("\n🎯 Testando detecção de quest points...")

        try:
            current, maximum = await self.quest_automation.get_quest_points()

            if current is not None and maximum is not None:
                print(f"✅ Quest Points detectados: {current}/{maximum}")
                return current, maximum
            else:
                print("❌ Não foi possível detectar quest points")
                return None, None

        except Exception as e:
            print(f"❌ Erro na detecção de quest points: {e}")
            return None, None

    async def test_quest_list(self):
        """Testa listagem de quests disponíveis"""
        print("\n📝 Testando listagem de quests...")

        try:
            quests = await self.quest_automation.get_available_quests()

            if quests:
                print(f"✅ {len(quests)} quests encontrados")

                # Mostrar alguns exemplos
                print("\n📋 Primeiros 5 quests encontrados:")
                for i, quest in enumerate(quests[:5]):
                    level = quest.get('level', 'N/A')
                    name = quest.get('name', 'N/A')[:30]
                    print(f"  {i+1}. Level {level}: {name}")

                return quests
            else:
                print("❌ Nenhum quest encontrado")
                return []

        except Exception as e:
            print(f"❌ Erro na listagem de quests: {e}")
            return []

    async def test_interaction(self, quests):
        """Testa interação com um quest (opcional)"""
        if not quests:
            return False

        print("\n🎮 Teste de interação disponível...")
        response = input("Deseja testar clique em um quest? (s/n): ").lower().strip()

        if response == 's':
            try:
                # Pegar o primeiro quest
                first_quest = quests[0]
                print(f"🎯 Testando clique no quest: {first_quest.get('name', 'N/A')}")

                success = await self.quest_automation.click_quest(first_quest)

                if success:
                    print("✅ Clique no quest bem-sucedido")

                    # Aguardar um pouco para popup aparecer
                    await asyncio.sleep(2)

                    # Tentar encontrar botão perform
                    perform_button = await self.quest_automation.find_perform_button()

                    if perform_button:
                        print("✅ Botão 'Perform' encontrado")

                        response = input("Deseja executar o quest? (s/n): ").lower().strip()
                        if response == 's':
                            result = await self.quest_automation.perform_quest()
                            if result:
                                print("✅ Quest executado com sucesso!")
                            else:
                                print("❌ Falha na execução do quest")
                    else:
                        print("⚠️ Botão 'Perform' não encontrado")

                    # Fechar popups
                    await self.quest_automation.close_popups()
                    print("🧹 Popups fechados")

                    return True
                else:
                    print("❌ Falha no clique do quest")
                    return False

            except Exception as e:
                print(f"❌ Erro na interação: {e}")
                return False

        return True

    async def test_full_cycle(self):
        """Testa um ciclo completo (opcional)"""
        print("\n🔄 Teste de ciclo completo disponível...")
        response = input("Deseja testar um ciclo completo de quest automation? (s/n): ").lower().strip()

        if response == 's':
            try:
                print("🚀 Executando ciclo completo...")

                result = await self.quest_automation.execute_quests_cycle(max_quests=1)

                if result and result.get('quests_completed', 0) > 0:
                    print("✅ Ciclo completo executado com sucesso!")
                    print(f"📊 Resultado: {result}")
                    return True
                else:
                    print("⚠️ Ciclo completo executado, mas sem quests completados")
                    return False

            except Exception as e:
                print(f"❌ Erro no ciclo completo: {e}")
                return False

        return True

    async def cleanup(self):
        """Limpa recursos"""
        print("\n🧹 Limpando recursos...")

        try:
            if self.web_engine:
                await self.web_engine.cleanup()
                print("✅ Web Engine limpo")
        except Exception as e:
            print(f"⚠️ Erro na limpeza: {e}")

    async def run_tests(self):
        """Executa todos os testes"""
        print("=" * 60)
        print("🎯 TESTE FORÇADO DO SISTEMA DE QUEST AUTOMATION")
        print("=" * 60)

        # Inicialização
        if not await self.initialize():
            return False

        try:
            # Teste 1: Navegação
            nav_success = await self.test_navigation()

            if nav_success:
                # Teste 2: Quest Points
                current, maximum = await self.test_quest_points()

                # Teste 3: Listagem de Quests
                quests = await self.test_quest_list()

                # Teste 4: Interação (opcional)
                await self.test_interaction(quests)

                # Teste 5: Ciclo completo (opcional)
                await self.test_full_cycle()

                # Relatório final
                print("\n" + "=" * 60)
                print("📊 RELATÓRIO FINAL DO TESTE")
                print("=" * 60)
                print(f"✅ Navegação: {'OK' if nav_success else 'FALHOU'}")
                print(f"✅ Quest Points: {current}/{maximum}" if current is not None else "❌ Quest Points: FALHOU")
                print(f"✅ Quests Encontrados: {len(quests)}" if quests else "❌ Quests: NENHUM")

                # Confirmação do usuário
                print("\n🎯 CONFIRMAÇÃO MANUAL:")
                print("Por favor, confirme se o sistema funcionou corretamente:")
                print("1. O bot navegou para a página de quests?")
                print("2. Os quest points foram detectados corretamente?")
                print("3. A lista de quests foi carregada?")
                print("4. (Se testado) A interação com quests funcionou?")

                user_confirm = input("\nO teste foi bem-sucedido? (s/n): ").lower().strip()

                if user_confirm == 's':
                    print("🎉 TESTE CONFIRMADO COMO SUCESSO!")
                    print("✅ Sistema de Quest Automation está funcionando!")
                else:
                    print("⚠️ Teste relatado como falha pelo usuário")
                    print("🔧 Verifique os logs acima para identificar problemas")

                return user_confirm == 's'

            else:
                print("\n❌ TESTE FALHOU NA NAVEGAÇÃO")
                return False

        finally:
            await self.cleanup()


async def main():
    """Função principal"""
    tester = QuestTester()

    try:
        success = await tester.run_tests()

        if success:
            print("\n🎉 SISTEMA DE QUEST AUTOMATION: FUNCIONANDO!")
            return 0
        else:
            print("\n❌ SISTEMA DE QUEST AUTOMATION: PROBLEMAS DETECTADOS")
            return 1

    except KeyboardInterrupt:
        print("\n⚠️ Teste interrompido pelo usuário")
        return 1
    except Exception as e:
        print(f"\n❌ Erro fatal no teste: {e}")
        return 1


if __name__ == "__main__":
    print("🎯 Iniciando teste forçado do Quest Automation...")
    print("📋 Este script irá testar rapidamente se o sistema está funcionando")
    print("⏱️ Tempo estimado: 1-3 minutos")
    print()

    # Verificar se estamos no diretório correto
    if not os.path.exists("src/automation/quest_automation.py"):
        print("❌ Erro: Execute este script do diretório raiz do projeto (c:\\BOTNOVOTESTATT)")
        sys.exit(1)

    # Executar testes
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
