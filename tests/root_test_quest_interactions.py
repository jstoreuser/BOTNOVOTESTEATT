#!/usr/bin/env python3
"""
Quest Interaction Test Script

Este script testa interações específicas na página de quests:
1. Clica em diferentes abas/seções
2. Testa abertura de popups de quest
3. Analisa elementos de quest específicos
4. Testa botões de Perform

Execute após analyze_quest_page.py para testar funcionalidades.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_quest_interactions():
    """Testa interações na página de quests"""

    print("🧪 Testando interações na página de quests...")

    try:
        from automation.web_engine import WebEngineManager

        # Get web engine
        engine = await WebEngineManager.get_instance()
        page = await engine.get_page()

        if not page:
            print("❌ Não foi possível obter a página")
            return False

        # Ensure we're on quests page
        if "quests" not in page.url:
            print("📍 Navegando para página de quests...")
            await page.goto("https://web.simple-mmo.com/quests")
            await page.wait_for_load_state("networkidle")

        print(f"✅ Na página: {page.url}")

        # Aguardar um pouco para garantir que a página carregou
        await asyncio.sleep(2)

        print("\n" + "="*60)
        print("🧪 TESTANDO INTERAÇÕES")
        print("="*60)

        # 1. Procurar e testar clique em "Not Completed"
        print("\n📝 1. PROCURANDO SEÇÃO 'NOT COMPLETED'...")

        # Estratégias para encontrar "Not Completed"
        strategies = [
            "text=Not Completed",
            "text=not completed",
            "[data-tab='not-completed']",
            "[data-target='not-completed']",
            "a:has-text('Not Completed')",
            "button:has-text('Not Completed')",
            ".tab:has-text('Not Completed')",
            ".nav-link:has-text('Not Completed')"
        ]

        not_completed_element = None
        for strategy in strategies:
            try:
                element = await page.query_selector(strategy)
                if element:
                    text = await element.text_content()
                    print(f"✅ Encontrado com '{strategy}': '{text}'")
                    not_completed_element = element
                    break
            except Exception as e:
                print(f"   ❌ Estratégia '{strategy}' falhou: {e}")

        if not not_completed_element:
            print("⚠️ Não encontrou 'Not Completed', procurando manualmente...")

            # Busca manual por texto
            all_elements = await page.query_selector_all("a, button, div, span")
            for element in all_elements:
                try:
                    text = await element.text_content()
                    if text and "not completed" in text.lower():
                        print(f"✅ Encontrado manualmente: '{text}'")
                        not_completed_element = element
                        break
                except:
                    continue

        # 2. Testar clique em Not Completed
        if not_completed_element:
            print("\n🖱️ 2. TESTANDO CLIQUE EM 'NOT COMPLETED'...")
            try:
                await not_completed_element.click()
                await asyncio.sleep(2)  # Aguardar carregamento
                print("✅ Clique realizado com sucesso")
            except Exception as e:
                print(f"❌ Erro ao clicar: {e}")

        # 3. Analisar quests disponíveis
        print("\n🗒️ 3. ANALISANDO QUESTS DISPONÍVEIS...")

        # Procurar por elementos de quest
        quest_selectors = [
            ".quest-item",
            ".quest",
            "[data-quest]",
            ".list-group-item",
            ".card",
            "tr"  # Se for uma tabela
        ]

        quest_elements = []
        for selector in quest_selectors:
            try:
                elements = await page.query_selector_all(selector)
                if elements:
                    print(f"✅ Encontrados {len(elements)} elementos com '{selector}'")
                    quest_elements.extend(elements)
            except Exception as e:
                print(f"   ❌ Seletor '{selector}' falhou: {e}")

        # Analisar os primeiros quest elements
        print(f"\n📊 Analisando primeiros {min(5, len(quest_elements))} elementos de quest:")

        for i, element in enumerate(quest_elements[:5]):
            try:
                text = await element.text_content()
                if text and len(text.strip()) > 5:
                    print(f"\n   Quest {i+1}:")
                    print(f"      Texto: '{text.strip()[:100]}...'")

                    # Procurar por informações específicas no texto
                    text_lower = text.lower()
                    if "level" in text_lower:
                        print(f"      ✅ Contém informação de level")
                    if "left" in text_lower:
                        print(f"      ✅ Contém informação de 'left'")
                    if any(char.isdigit() for char in text):
                        print(f"      ✅ Contém números")
            except Exception as e:
                print(f"      ❌ Erro ao analisar elemento {i+1}: {e}")

        # 4. Testar clique em quest para abrir popup
        print("\n🔄 4. TESTANDO ABERTURA DE POPUP DE QUEST...")

        if quest_elements:
            try:
                # Tentar clicar na primeira quest
                first_quest = quest_elements[0]

                print("🖱️ Clicando na primeira quest...")
                await first_quest.click()
                await asyncio.sleep(3)  # Aguardar popup aparecer

                # Procurar por popup/modal
                popup_selectors = [
                    ".modal",
                    ".popup",
                    ".dialog",
                    "[role='dialog']",
                    ".overlay",
                    ".quest-modal"
                ]

                popup_found = False
                for selector in popup_selectors:
                    try:
                        popup = await page.query_selector(selector)
                        if popup:
                            # Verificar se está visível
                            is_visible = await popup.is_visible()
                            if is_visible:
                                print(f"✅ Popup encontrado com '{selector}'")

                                # Analisar conteúdo do popup
                                popup_text = await popup.text_content()
                                print(f"📄 Conteúdo do popup: '{popup_text[:200]}...'")

                                # Procurar por botão Perform
                                perform_button = await popup.query_selector("button:has-text('Perform'), [value='Perform'], input[type='submit']")
                                if perform_button:
                                    print("✅ Botão 'Perform' encontrado no popup!")

                                    perform_text = await perform_button.text_content()
                                    print(f"   Texto do botão: '{perform_text}'")
                                else:
                                    print("⚠️ Botão 'Perform' não encontrado")

                                popup_found = True
                                break
                    except Exception as e:
                        print(f"   ❌ Erro com seletor '{selector}': {e}")

                if not popup_found:
                    print("⚠️ Popup não encontrado, talvez o clique não funcionou")

            except Exception as e:
                print(f"❌ Erro ao testar popup: {e}")

        # 5. Procurar por Quest Points na página atual
        print("\n🎯 5. PROCURANDO QUEST POINTS...")

        # Procurar por elementos que podem conter quest points
        all_text_elements = await page.query_selector_all("span, div, p, strong, b")

        quest_points_candidates = []
        for element in all_text_elements:
            try:
                text = await element.text_content()
                if text and any(keyword in text.lower() for keyword in ['quest point', 'points', 'energy']):
                    quest_points_candidates.append(text.strip())
            except:
                continue

        print(f"🔍 Candidatos a Quest Points encontrados:")
        for i, candidate in enumerate(quest_points_candidates[:10]):
            print(f"   {i+1}. '{candidate}'")

        # 6. Salvar screenshot para análise visual
        print(f"\n📸 6. SALVANDO SCREENSHOT...")
        try:
            await page.screenshot(path="quest_page_screenshot.png", full_page=True)
            print("✅ Screenshot salvo: quest_page_screenshot.png")
        except Exception as e:
            print(f"❌ Erro ao salvar screenshot: {e}")

        print("\n" + "="*60)
        print("✅ TESTE DE INTERAÇÕES COMPLETO!")
        print("="*60)

        return True

    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Função principal"""
    try:
        success = await test_quest_interactions()
        if success:
            print("\n🎉 Teste de interações concluído!")
        else:
            print("\n❌ Teste falhou!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")

if __name__ == "__main__":
    asyncio.run(main())
