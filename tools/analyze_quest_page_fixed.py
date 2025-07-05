#!/usr/bin/env python3
"""
Quest Page Analysis Script - Fixed Version

Este script analisa a página de quests do SimpleMMO e salva todas as informações em arquivos
para facilitar a análise e desenvolvimento do sistema de quests.
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def analyze_quest_page():
    """Analisa a página de quests e salva informações em arquivos"""

    print("🔍 Iniciando análise da página de quests...")

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

        # Create analysis report
        report = []
        report.append("QUEST PAGE ANALYSIS REPORT")
        report.append("=" * 80)
        report.append(f"Timestamp: {datetime.now()}")
        report.append(f"URL: {page.url}")
        report.append(f"Title: {await page.title()}")
        report.append("")

        # 1. Analyze Quest Points
        print("🎯 Analisando Quest Points...")
        report.append("🎯 QUEST POINTS ANALYSIS")
        report.append("-" * 40)

        html_content = await page.content()

        # Find lines with "quest" and "point"
        lines = html_content.split('\n')
        quest_point_lines = [line.strip() for line in lines if 'quest' in line.lower() and 'point' in line.lower()]

        report.append(f"Found {len(quest_point_lines)} lines containing 'quest' and 'point':")
        for i, line in enumerate(quest_point_lines[:15]):  # First 15 lines
            report.append(f"  {i+1}. {line}")

        # 2. Find numbers (possible quest points)
        print("🔢 Procurando elementos com números...")
        report.append("\n🔢 ELEMENTS WITH NUMBERS")
        report.append("-" * 40)

        number_elements = await page.query_selector_all("span, div, p")
        numbers_found = []

        for element in number_elements[:50]:
            try:
                text = await element.text_content()
                if text and any(char.isdigit() for char in text) and len(text.strip()) < 30:
                    numbers_found.append(text.strip())
            except:
                continue

        report.append(f"Found {len(numbers_found)} elements with numbers:")
        for i, number in enumerate(numbers_found[:20]):  # First 20
            report.append(f"  {i+1}. '{number}'")

        # 3. Find buttons
        print("🔲 Analisando botões...")
        report.append("\n🔲 BUTTONS ANALYSIS")
        report.append("-" * 40)

        buttons = await page.query_selector_all("button, input[type='button'], input[type='submit']")

        report.append(f"Found {len(buttons)} buttons:")
        for i, button in enumerate(buttons):
            try:
                text = await button.text_content()
                classes = await button.get_attribute("class") or ""
                onclick = await button.get_attribute("onclick") or ""
                report.append(f"  Button {i+1}: '{text.strip() if text else '[no text]'}' (class: {classes}) (onclick: {onclick[:50]})")
            except:
                report.append(f"  Button {i+1}: [error reading button]")

        # 4. Find links
        print("🔗 Analisando links...")
        report.append("\n🔗 LINKS ANALYSIS")
        report.append("-" * 40)

        links = await page.query_selector_all("a")

        report.append(f"Found {len(links)} links:")
        for i, link in enumerate(links[:25]):  # First 25 links
            try:
                text = await link.text_content()
                href = await link.get_attribute("href") or ""
                classes = await link.get_attribute("class") or ""
                report.append(f"  Link {i+1}: '{text.strip() if text else '[no text]'}' -> {href} (class: {classes})")
            except:
                report.append(f"  Link {i+1}: [error reading link]")

        # 5. Find quest-related elements
        print("📋 Procurando elementos relacionados a quests...")
        report.append("\n📋 QUEST-RELATED ELEMENTS")
        report.append("-" * 40)

        all_elements = await page.query_selector_all("div, span, p, li, td")
        quest_elements = []

        for element in all_elements:
            try:
                text = await element.text_content()
                if text and any(keyword in text.lower() for keyword in ['quest', 'level', 'left', 'perform', 'success', 'chance']):
                    if len(text.strip()) > 5 and len(text.strip()) < 200:
                        quest_elements.append(text.strip())
            except:
                continue

        # Remove duplicates and sort
        quest_elements = list(set(quest_elements))
        quest_elements.sort()

        report.append(f"Found {len(quest_elements)} quest-related elements:")
        for i, element in enumerate(quest_elements[:30]):  # First 30
            report.append(f"  {i+1}. '{element}'")

        # Save all files
        print("\n💾 Salvando arquivos...")

        # Save analysis report
        with open("quest_page_analysis.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(report))
        print("✅ Relatório salvo em: quest_page_analysis.txt")

        # Save HTML
        with open("quest_page_structure.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("✅ HTML salvo em: quest_page_structure.html")

        # Save simplified structure
        with open("quest_page_elements.txt", "w", encoding="utf-8") as f:
            f.write("QUEST PAGE ELEMENTS SUMMARY\n")
            f.write("=" * 50 + "\n\n")

            f.write("ALL BUTTONS:\n")
            for i, button in enumerate(buttons):
                try:
                    text = await button.text_content()
                    f.write(f"Button {i+1}: {text.strip() if text else '[no text]'}\n")
                except:
                    f.write(f"Button {i+1}: [error]\n")

            f.write("\nCLICKABLE ELEMENTS:\n")
            clickable = await page.query_selector_all("[onclick], [role='button']")
            for i, elem in enumerate(clickable):
                try:
                    text = await elem.text_content()
                    onclick = await elem.get_attribute("onclick") or ""
                    f.write(f"Clickable {i+1}: {text.strip() if text else '[no text]'} (onclick: {onclick[:50]})\n")
                except:
                    f.write(f"Clickable {i+1}: [error]\n")

        print("✅ Elementos salvos em: quest_page_elements.txt")

        print("\n🎉 Análise completa! Arquivos gerados:")
        print("   📄 quest_page_analysis.txt")
        print("   🌐 quest_page_structure.html")
        print("   🔍 quest_page_elements.txt")

        return True

    except Exception as e:
        error_msg = f"❌ Erro durante análise: {e}\n"
        import traceback
        error_msg += traceback.format_exc()

        print(error_msg)

        # Save error to file
        with open("quest_analysis_error.txt", "w", encoding="utf-8") as f:
            f.write(error_msg)

        return False

async def main():
    """Função principal"""
    try:
        success = await analyze_quest_page()
        if success:
            print("\n✅ Análise concluída com sucesso!")
        else:
            print("\n❌ Análise falhou!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    finally:
        print("\n💡 Página mantida aberta para inspeção manual")

if __name__ == "__main__":
    asyncio.run(main())
