#!/usr/bin/env python3
"""
Quest Interactions Test Script - Fixed Version

Este script testa interações específicas na página de quests:
1. Clica em abas/seções
2. Testa popups de quest
3. Verifica botões de perform
4. Analisa resultados

Execute depois do analyze_quest_page_fixed.py
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_quest_interactions():
    """Testa interações na página de quests"""

    print("🧪 Iniciando teste de interações na página de quests...")

    try:
        from automation.web_engine import WebEngineManager

        # Get web engine
        engine = await WebEngineManager.get_instance()
        page = await engine.get_page()

        if not page:
            print("❌ Não foi possível obter a página")
            return False

        # Ensure we're on the quests page
        if "quests" not in page.url:
            print("📍 Navegando para a página de quests...")
            await page.goto("https://web.simple-mmo.com/quests")
            await page.wait_for_load_state("networkidle")

        print(f"✅ Página atual: {page.url}")

        # Create test report
        test_report = []
        test_report.append("QUEST INTERACTIONS TEST REPORT")
        test_report.append("=" * 80)
        test_report.append(f"Timestamp: {datetime.now()}")
        test_report.append(f"URL: {page.url}")
        test_report.append("")

        # 1. Test tabs/sections
        print("📑 Testando abas e seções...")
        test_report.append("📑 TABS AND SECTIONS TEST")
        test_report.append("-" * 40)

        # Look for tab-like elements
        possible_tabs = await page.query_selector_all("a, button, [role='tab'], .tab, .nav-link")

        test_report.append(f"Found {len(possible_tabs)} possible tab elements:")

        for i, tab in enumerate(possible_tabs[:10]):  # Test first 10
            try:
                text = await tab.text_content()
                tag_name = await tab.evaluate("el => el.tagName")
                classes = await tab.get_attribute("class") or ""
                href = await tab.get_attribute("href") or ""

                test_info = f"  Tab {i+1}: {tag_name} '{text.strip() if text else '[no text]'}' (class: {classes}) (href: {href})"
                print(test_info)
                test_report.append(test_info)

                # Try to click if it looks like a quest-related tab
                if text and any(keyword in text.lower() for keyword in ['completed', 'available', 'not completed', 'quest']):
                    try:
                        print(f"    🖱️ Clicking on: {text.strip()}")
                        await tab.click()
                        await page.wait_for_timeout(2000)  # Wait 2 seconds

                        # Check what changed
                        new_url = page.url
                        test_report.append(f"    ✅ Click successful, URL: {new_url}")

                    except Exception as click_error:
                        error_msg = f"    ❌ Click failed: {click_error}"
                        print(error_msg)
                        test_report.append(error_msg)

            except Exception as e:
                error_msg = f"  Tab {i+1}: Error reading - {e}"
                print(error_msg)
                test_report.append(error_msg)

        # 2. Look for quest items
        print("\n📋 Procurando itens de quest clicáveis...")
        test_report.append("\n📋 QUEST ITEMS TEST")
        test_report.append("-" * 40)

        # Look for quest-like clickable elements
        quest_elements = await page.query_selector_all("div[onclick], tr[onclick], .quest, [data-quest], .clickable")

        if not quest_elements:
            # Broaden search
            all_clickable = await page.query_selector_all("[onclick]")
            quest_elements = []
            for elem in all_clickable:
                try:
                    text = await elem.text_content()
                    if text and any(keyword in text.lower() for keyword in ['level', 'quest', 'left']):
                        quest_elements.append(elem)
                except:
                    continue

        test_report.append(f"Found {len(quest_elements)} potential quest items:")

        for i, quest in enumerate(quest_elements[:5]):  # Test first 5
            try:
                text = await quest.text_content()
                onclick = await quest.get_attribute("onclick") or ""

                quest_info = f"  Quest {i+1}: '{text.strip()[:100] if text else '[no text]'}...'"
                print(quest_info)
                test_report.append(quest_info)
                test_report.append(f"    onclick: {onclick[:100]}...")

                # Try to click and see what happens
                try:
                    print(f"    🖱️ Clicking quest item...")
                    await quest.click()
                    await page.wait_for_timeout(3000)  # Wait 3 seconds

                    # Check for popup or modal
                    popups = await page.query_selector_all(".modal, .popup, .dialog, [role='dialog']")
                    if popups:
                        test_report.append(f"    ✅ Popup appeared! Found {len(popups)} popup elements")

                        # Analyze popup content
                        for j, popup in enumerate(popups):
                            try:
                                popup_text = await popup.text_content()
                                test_report.append(f"      Popup {j+1}: {popup_text[:200]}...")

                                # Look for buttons in popup
                                popup_buttons = await popup.query_selector_all("button")
                                test_report.append(f"      Found {len(popup_buttons)} buttons in popup:")

                                for k, btn in enumerate(popup_buttons):
                                    btn_text = await btn.text_content()
                                    test_report.append(f"        Button {k+1}: '{btn_text.strip() if btn_text else '[no text]'}'")

                            except Exception as popup_error:
                                test_report.append(f"      Error reading popup: {popup_error}")

                        # Try to close popup (look for close button or click outside)
                        close_buttons = await page.query_selector_all(".close, [aria-label='close'], .modal-close")
                        if close_buttons:
                            await close_buttons[0].click()
                            await page.wait_for_timeout(1000)

                    else:
                        test_report.append(f"    ℹ️ No popup detected after click")

                except Exception as click_error:
                    error_msg = f"    ❌ Click failed: {click_error}"
                    print(error_msg)
                    test_report.append(error_msg)

            except Exception as e:
                error_msg = f"  Quest {i+1}: Error - {e}"
                print(error_msg)
                test_report.append(error_msg)

        # Save test report
        print(f"\n💾 Salvando relatório de testes...")

        with open("quest_interactions_test.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(test_report))

        print("✅ Relatório de interações salvo em: quest_interactions_test.txt")

        print(f"\n🎉 Teste de interações completo!")

        return True

    except Exception as e:
        error_msg = f"❌ Erro durante teste: {e}\n"
        import traceback
        error_msg += traceback.format_exc()

        print(error_msg)

        # Save error to file
        with open("quest_interactions_error.txt", "w", encoding="utf-8") as f:
            f.write(error_msg)

        return False

async def main():
    """Função principal"""
    try:
        success = await test_quest_interactions()
        if success:
            print("\n✅ Teste de interações concluído com sucesso!")
        else:
            print("\n❌ Teste de interações falhou!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    finally:
        print("\n💡 Página mantida aberta para inspeção manual")

if __name__ == "__main__":
    asyncio.run(main())
