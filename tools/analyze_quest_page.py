#!/usr/bin/env python3
"""
Quest System Analysis Script

Este script analisa a página de quests do SimpleMMO para extrair:
1. Estrutura HTML da página
2. Elementos dos Quest Points
3. Lista de quests disponíveis
4. Estrutura dos popups de quest
5. Botões e elementos de interação

Execute este script para coletar informações antes de implementar o sistema de quests.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def analyze_quest_page():
    """Analisa a página de quests do SimpleMMO"""

    print("🔍 Analisando página de quests do SimpleMMO...")

    try:
        from automation.web_engine import WebEngineManager

        # Get web engine
        engine = await WebEngineManager.get_instance()
        page = await engine.get_page()

        if not page:
            print("❌ Não foi possível obter a página")
            return False

        print(f"✅ Página atual: {page.url}")

        # Navigate to quests page
        print("\n📍 Navegando para a página de quests...")
        await page.goto("https://web.simple-mmo.com/quests")
        await page.wait_for_load_state("networkidle")
        print(f"✅ Navegação completa: {page.url}")

        print("\n" + "="*80)
        print("📋 ANÁLISE DA PÁGINA DE QUESTS")
        print("="*80)

        # Criar lista para armazenar todas as informações
        analysis_report = []
        analysis_report.append("QUEST PAGE ANALYSIS REPORT")
        analysis_report.append("="*80)
        analysis_report.append(f"Timestamp: {asyncio.get_event_loop().time()}")
        analysis_report.append(f"URL: {page.url}")
        analysis_report.append("")

        # 1. Análise dos Quest Points
        print("\n🎯 1. ANALISANDO QUEST POINTS...")
        analysis_report.append("🎯 1. QUEST POINTS ANALYSIS")
        analysis_report.append("-" * 40)

        # Procurar por elementos que contenham "Quest Points" ou similar
        quest_points_elements = await page.query_selector_all("*")

        # Salvar HTML completo da página
        html_content = await page.content()

        # Procurar por Quest Points no HTML
        lines = html_content.split('\n')
        quest_points_lines = [line.strip() for line in lines if 'quest' in line.lower() and 'point' in line.lower()]

        if quest_points_lines:
            print("📊 Linhas HTML relacionadas a Quest Points:")
            analysis_report.append("📊 HTML lines related to Quest Points:")
            for i, line in enumerate(quest_points_lines[:10]):  # Salvar mais linhas no arquivo
                print(f"   {i+1}. {line}")
                analysis_report.append(f"   {i+1}. {line}")

        # Procurar por números que podem ser quest points
        try:
            # Tentar encontrar elementos com números que podem ser quest points
            possible_quest_elements = await page.query_selector_all("span, div, p")

            print("\n🔢 Procurando por elementos com números (possíveis Quest Points):")
            analysis_report.append("\n🔢 Elements with numbers (possible Quest Points):")
            number_elements_found = 0
            for element in possible_quest_elements[:30]:  # Aumentar limite no arquivo
                try:
                    text = await element.text_content()
                    if text and any(char.isdigit() for char in text) and len(text.strip()) < 20:
                        element_info = f"   - '{text.strip()}'"
                        print(element_info)
                        analysis_report.append(element_info)
                        number_elements_found += 1
                except:
                    continue
            analysis_report.append(f"Total number elements found: {number_elements_found}")
        except Exception as e:
            error_msg = f"⚠️ Erro ao procurar elementos: {e}"
            print(error_msg)
            analysis_report.append(error_msg)

        # 2. Análise da seção "Not Completed"
        print("\n📝 2. ANALISANDO SEÇÃO 'NOT COMPLETED'...")
        analysis_report.append("\n📝 2. 'NOT COMPLETED' SECTION ANALYSIS")
        analysis_report.append("-" * 40)

        # Procurar por texto "Not Completed" ou similar
        not_completed_text = await page.query_selector_all("text=Not Completed, text=not completed, text=Not completed")

        if not not_completed_text:
            # Procurar por outros termos relacionados
            tabs_or_sections = await page.query_selector_all("a, button, div, span")

            print("🔍 Procurando por abas ou seções relacionadas a quests:")
            analysis_report.append("🔍 Tabs or sections related to quests:")
            for element in tabs_or_sections[:50]:  # Aumentar limite no arquivo
                try:
                    text = await element.text_content()
                    if text and any(keyword in text.lower() for keyword in ['completed', 'available', 'quest', 'tab']):
                        tag_name = await element.evaluate("el => el.tagName")
                        class_name = await element.get_attribute("class") or ""
                        element_info = f"   - {tag_name}: '{text.strip()}' (class: {class_name})"
                        print(element_info)
                        analysis_report.append(element_info)
                except:
                    continue

        # 3. Análise da lista de quests
        print("\n🗒️ 3. ANALISANDO LISTA DE QUESTS...")
        analysis_report.append("\n🗒️ 3. QUEST LIST ANALYSIS")
        analysis_report.append("-" * 40)

        # Procurar por elementos que podem ser quests
        quest_items = await page.query_selector_all("div, li, tr")

        print("🔍 Procurando por itens de quest (elementos com informações estruturadas):")
        analysis_report.append("🔍 Quest items (structured information elements):")
        quest_count = 0
        for element in quest_items[:100]:  # Aumentar limite no arquivo
            try:
                text = await element.text_content()
                if text and len(text.strip()) > 10 and len(text.strip()) < 200:
                    # Verificar se contém palavras relacionadas a quest
                    if any(keyword in text.lower() for keyword in ['level', 'left', 'quest', 'perform']):
                        quest_info = f"   Quest {quest_count + 1}: '{text.strip()[:150]}...'"
                        print(quest_info)
                        analysis_report.append(quest_info)
                        quest_count += 1
                        if quest_count >= 10:  # Salvar mais exemplos no arquivo
                            break
            except:
                continue

        analysis_report.append(f"Total quest items found: {quest_count}")

        # 4. Salvar todos os arquivos de análise
        print(f"\n💾 4. SALVANDO ARQUIVOS DE ANÁLISE...")

        # Salvar relatório de análise
        analysis_text = "\n".join(analysis_report)
        with open("quest_page_analysis.txt", "w", encoding="utf-8") as f:
            f.write(analysis_text)
        print(f"✅ Relatório de análise salvo em: quest_page_analysis.txt")

        # Salvar HTML da página
        with open("quest_page_structure.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"✅ HTML completo salvo em: quest_page_structure.html")

        # Salvar estrutura simplificada com mais detalhes
        with open("quest_page_elements.txt", "w", encoding="utf-8") as f:
            f.write("=== ANÁLISE DETALHADA DOS ELEMENTOS ===\n\n")
            f.write(f"URL: {page.url}\n")
            f.write(f"Título: {await page.title()}\n\n")

            f.write("=== TODOS OS BOTÕES ===\n")
            buttons = await page.query_selector_all("button, input[type='button'], input[type='submit']")
            for i, button in enumerate(buttons):
                try:
                    text = await button.text_content()
                    classes = await button.get_attribute("class") or ""
                    f.write(f"Button {i+1}: '{text.strip()}' (class: {classes})\n")
                except:
                    f.write(f"Button {i+1}: [erro ao ler]\n")

            f.write("\n=== TODOS OS LINKS ===\n")
            links = await page.query_selector_all("a")
            for i, link in enumerate(links[:20]):  # Limitar a 20 links
                try:
                    text = await link.text_content()
                    href = await link.get_attribute("href") or ""
                    classes = await link.get_attribute("class") or ""
                    f.write(f"Link {i+1}: '{text.strip()}' -> {href} (class: {classes})\n")
                except:
                    f.write(f"Link {i+1}: [erro ao ler]\n")

            f.write("\n=== ELEMENTOS COM NÚMEROS ===\n")
            all_elements = await page.query_selector_all("span, div, p, td")
            number_count = 0
            for element in all_elements:
                try:
                    text = await element.text_content()
                    if text and any(char.isdigit() for char in text) and len(text.strip()) < 50:
                        tag_name = await element.evaluate("el => el.tagName")
                        classes = await element.get_attribute("class") or ""
                        f.write(f"Número {number_count+1}: {tag_name} '{text.strip()}' (class: {classes})\n")
                        number_count += 1
                        if number_count >= 50:  # Limitar output
                            break
                except:
                    continue

        print(f"✅ Elementos detalhados salvos em: quest_page_elements.txt")
                    if text and text.strip():
                        f.write(f"{tag_name}: {text.strip()}\n")
                except:
                    continue

        print(f"✅ Estrutura salva em: quest_page_structure.txt")

        # 5. Testar cliques em elementos
        print(f"\n🖱️ 5. TESTANDO ELEMENTOS CLICÁVEIS...")

        # Procurar por botões e links
        clickable_elements = await page.query_selector_all("button, a, [role='button'], [onclick]")

        print(f"🔍 Encontrados {len(clickable_elements)} elementos clicáveis:")
        for i, element in enumerate(clickable_elements[:10]):  # Mostrar apenas 10
            try:
                text = await element.text_content()
                tag_name = await element.evaluate("el => el.tagName")
                if text and text.strip():
                    print(f"   {i+1}. {tag_name}: '{text.strip()}'")
            except:
                continue

        print("\n" + "="*80)
        print("✅ ANÁLISE COMPLETA!")
        print("="*80)
        print("📋 Arquivos gerados:")
        print("   - quest_page_analysis.html (HTML completo)")
        print("   - quest_page_structure.txt (estrutura resumida)")
        print("\n💡 Próximos passos:")
        print("   1. Revisar os arquivos gerados")
        print("   2. Identificar seletores CSS específicos")
        print("   3. Testar interações com elementos")

        return True

    except Exception as e:
        print(f"❌ Erro durante análise: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Função principal"""
    try:
        success = await analyze_quest_page()
        if success:
            print("\n🎉 Análise concluída com sucesso!")
        else:
            print("\n❌ Análise falhou!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    finally:
        try:
            from automation.web_engine import WebEngineManager
            # Não fazer force_reset para manter a página aberta para inspeção manual
            print("\n💡 Página mantida aberta para inspeção manual")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(main())
