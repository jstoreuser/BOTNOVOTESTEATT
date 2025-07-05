#!/usr/bin/env python3
"""
Quest System Complete Analysis Script

Este script faz uma análise completa do sistema de quests:
1. Analisa Quest Points (atual/máximo)
2. Testa cliques em quests individuais
3. Captura estrutura completa dos popups
4. Analisa botões Perform, Success chance, Quest Progress
5. Testa botão Show Result
6. Salva todas as informações em arquivos detalhados

Execute este script para obter TODAS as informações necessárias para implementar o sistema de quests.
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def complete_quest_analysis():
    """Análise completa do sistema de quests"""

    print("🔍 Iniciando análise completa do sistema de quests...")

    try:
        from automation.web_engine import WebEngineManager

        # Get web engine
        engine = await WebEngineManager.get_instance()
        page = await engine.get_page()

        if not page:
            print("❌ Não foi possível obter a página")
            return False

        # Navigate to quests page
        print("📍 Navegando para a página de quests...")
        await page.goto("https://web.simple-mmo.com/quests")
        await page.wait_for_load_state("networkidle")
        print(f"✅ Página carregada: {page.url}")

        # Create comprehensive report
        report = []
        report.append("COMPLETE QUEST SYSTEM ANALYSIS")
        report.append("=" * 80)
        report.append(f"Timestamp: {datetime.now()}")
        report.append(f"URL: {page.url}")
        report.append("")

        # PHASE 1: Quest Points Analysis
        print("🎯 FASE 1: Analisando Quest Points...")
        report.append("🎯 PHASE 1: QUEST POINTS DETAILED ANALYSIS")
        report.append("-" * 60)

        await analyze_quest_points(page, report)

        # PHASE 2: Quest Tabs Analysis
        print("📑 FASE 2: Analisando abas de quest...")
        report.append("\n📑 PHASE 2: QUEST TABS ANALYSIS")
        report.append("-" * 60)

        await analyze_quest_tabs(page, report)

        # PHASE 3: Quest List Analysis
        print("📋 FASE 3: Analisando lista de quests...")
        report.append("\n📋 PHASE 3: QUEST LIST ANALYSIS")
        report.append("-" * 60)

        quest_buttons = await analyze_quest_list(page, report)

        # PHASE 4: Quest Popup Analysis (THE MOST IMPORTANT)
        print("🔄 FASE 4: Analisando popups de quest...")
        report.append("\n🔄 PHASE 4: QUEST POPUP DETAILED ANALYSIS")
        report.append("-" * 60)

        await analyze_quest_popups(page, report, quest_buttons)

        # PHASE 5: Perform Button Testing
        print("⚡ FASE 5: Testando botões Perform...")
        report.append("\n⚡ PHASE 5: PERFORM BUTTON TESTING")
        report.append("-" * 60)

        await test_perform_buttons(page, report)

        # Save comprehensive report
        print(f"\n💾 Salvando relatório completo...")

        with open("quest_system_complete_analysis.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(report))

        print("✅ Relatório completo salvo em: quest_system_complete_analysis.txt")

        # Also save raw HTML for reference
        html_content = await page.content()
        with open("quest_system_raw_html.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        print("✅ HTML raw salvo em: quest_system_raw_html.html")

        print(f"\n🎉 Análise completa do sistema de quests finalizada!")

        return True

    except Exception as e:
        error_msg = f"❌ Erro durante análise: {e}\n"
        import traceback
        error_msg += traceback.format_exc()

        print(error_msg)

        # Save error to file
        with open("quest_analysis_complete_error.txt", "w", encoding="utf-8") as f:
            f.write(error_msg)

        return False

async def analyze_quest_points(page, report):
    """Analisa Quest Points em detalhes"""

    try:
        # Look for quest points in multiple ways
        quest_point_selectors = [
            "[x-text*='quest_points']",
            ".text-indigo-600",
            "*:has-text('Quest Points')",
            "*:has-text('/5')",
            "*:has-text('/4')",
            "*:has-text('/3')",
            ".font-semibold",
        ]

        report.append("Quest Points Detection Strategies:")

        for selector in quest_point_selectors:
            try:
                elements = await page.query_selector_all(selector)
                report.append(f"  Selector '{selector}': Found {len(elements)} elements")

                for i, elem in enumerate(elements[:5]):  # First 5 of each type
                    try:
                        text = await elem.text_content()
                        tag_name = await elem.evaluate("el => el.tagName")
                        classes = await elem.get_attribute("class") or ""
                        x_text = await elem.get_attribute("x-text") or ""

                        report.append(f"    Element {i+1}: {tag_name} '{text.strip() if text else '[no text]'}'")
                        report.append(f"      Classes: {classes}")
                        if x_text:
                            report.append(f"      x-text: {x_text}")

                    except Exception as e:
                        report.append(f"    Element {i+1}: Error reading - {e}")

            except Exception as e:
                report.append(f"  Selector '{selector}': Error - {e}")

        # Try to extract current/max quest points values
        report.append("\nQuest Points Value Extraction:")

        # Look for patterns like "2/5", "3/5", etc.
        all_text_elements = await page.query_selector_all("span, div, p")

        quest_point_patterns = []
        for element in all_text_elements:
            try:
                text = await element.text_content()
                if text and "/" in text and any(char.isdigit() for char in text):
                    # Check if it looks like quest points (small text with numbers)
                    if len(text.strip()) < 10 and text.count("/") == 1:
                        quest_point_patterns.append(text.strip())
            except:
                continue

        # Remove duplicates and sort
        quest_point_patterns = list(set(quest_point_patterns))
        quest_point_patterns.sort()

        report.append(f"Found {len(quest_point_patterns)} potential quest point patterns:")
        for pattern in quest_point_patterns[:10]:  # First 10
            report.append(f"  Pattern: '{pattern}'")

    except Exception as e:
        report.append(f"Error in quest points analysis: {e}")

async def analyze_quest_tabs(page, report):
    """Analisa as abas de quest (All, Not Completed, Completed)"""

    try:
        # Look for tab-like buttons
        tab_buttons = await page.query_selector_all("button")

        quest_tabs = []
        for button in tab_buttons:
            try:
                text = await button.text_content()
                if text and any(keyword in text.lower() for keyword in ['completed', 'all', 'not']):
                    classes = await button.get_attribute("class") or ""
                    quest_tabs.append({
                        'text': text.strip(),
                        'classes': classes,
                        'element': button
                    })
            except:
                continue

        report.append(f"Found {len(quest_tabs)} quest tab buttons:")

        for i, tab in enumerate(quest_tabs):
            report.append(f"  Tab {i+1}: '{tab['text']}'")
            report.append(f"    Classes: {tab['classes']}")

            # Check if this tab is currently active
            if "bg-gray-200" in tab['classes'] or "active" in tab['classes']:
                report.append(f"    Status: ACTIVE")
            else:
                report.append(f"    Status: Inactive")

        # Test clicking on "Not Completed" tab if not already active
        not_completed_tab = None
        for tab in quest_tabs:
            if "not completed" in tab['text'].lower():
                not_completed_tab = tab
                break

        if not_completed_tab:
            report.append(f"\nTesting 'Not Completed' tab click...")
            try:
                await not_completed_tab['element'].click()
                await page.wait_for_timeout(2000)  # Wait 2 seconds
                report.append("✅ Successfully clicked 'Not Completed' tab")
            except Exception as e:
                report.append(f"❌ Error clicking 'Not Completed' tab: {e}")

    except Exception as e:
        report.append(f"Error in quest tabs analysis: {e}")

async def analyze_quest_list(page, report):
    """Analisa a lista de quests disponíveis"""

    try:
        # Look for quest buttons
        quest_button_selectors = [
            "button.bg-white.rounded-lg",
            "button[onclick]",
            ".bg-white.rounded-lg",
            "*:has-text('Level')",
            "*:has-text('left')"
        ]

        all_quest_buttons = []

        for selector in quest_button_selectors:
            try:
                buttons = await page.query_selector_all(selector)
                report.append(f"Selector '{selector}': Found {len(buttons)} elements")

                for button in buttons:
                    try:
                        text = await button.text_content()
                        if text and "level" in text.lower() and "left" in text.lower():
                            all_quest_buttons.append(button)
                    except:
                        continue

            except Exception as e:
                report.append(f"Selector '{selector}': Error - {e}")

        # Remove duplicates
        unique_quest_buttons = []
        for button in all_quest_buttons:
            if button not in unique_quest_buttons:
                unique_quest_buttons.append(button)

        report.append(f"\nFound {len(unique_quest_buttons)} unique quest buttons:")

        quest_list = []
        for i, button in enumerate(unique_quest_buttons[:20]):  # Analyze first 20
            try:
                text = await button.text_content()
                onclick = await button.get_attribute("onclick") or ""
                classes = await button.get_attribute("class") or ""

                # Extract quest info
                lines = text.strip().split('\n')
                quest_name = lines[0].strip() if lines else "Unknown"

                level_info = ""
                left_info = ""
                for line in lines:
                    line = line.strip()
                    if "level" in line.lower():
                        level_info = line
                    if "left" in line.lower():
                        left_info = line

                quest_info = {
                    'name': quest_name,
                    'level': level_info,
                    'left': left_info,
                    'classes': classes,
                    'onclick': onclick,
                    'element': button
                }

                quest_list.append(quest_info)

                report.append(f"  Quest {i+1}: {quest_name}")
                report.append(f"    Level: {level_info}")
                report.append(f"    Left: {left_info}")
                report.append(f"    onClick: {onclick[:50]}..." if onclick else "    onClick: None")

            except Exception as e:
                report.append(f"  Quest {i+1}: Error reading - {e}")

        return unique_quest_buttons[:10]  # Return first 10 for popup testing

    except Exception as e:
        report.append(f"Error in quest list analysis: {e}")
        return []

async def analyze_quest_popups(page, report, quest_buttons):
    """Analisa os popups de quest em detalhes"""

    if not quest_buttons:
        report.append("No quest buttons available for popup testing")
        return

    report.append(f"Testing popups for {len(quest_buttons)} quests...")

    for i, quest_button in enumerate(quest_buttons[:3]):  # Test first 3 quests
        try:
            report.append(f"\n--- QUEST {i+1} POPUP ANALYSIS ---")

            # Get quest name first
            quest_text = await quest_button.text_content()
            quest_name = quest_text.split('\n')[0].strip() if quest_text else f"Quest {i+1}"
            report.append(f"Quest Name: {quest_name}")

            # Click the quest button
            report.append("Clicking quest button...")
            await quest_button.click()
            await page.wait_for_timeout(3000)  # Wait 3 seconds for popup

            # Look for popup/modal
            popup_selectors = [
                ".modal",
                ".popup",
                ".dialog",
                "[role='dialog']",
                ".swal2-popup",
                ".sweet-alert",
                ".overlay",
                "*[style*='z-index']"
            ]

            popup_found = False
            popup_element = None

            for selector in popup_selectors:
                try:
                    popups = await page.query_selector_all(selector)
                    for popup in popups:
                        is_visible = await popup.is_visible()
                        if is_visible:
                            popup_element = popup
                            popup_found = True
                            report.append(f"✅ Popup found with selector: {selector}")
                            break
                    if popup_found:
                        break
                except:
                    continue

            if popup_found and popup_element:
                # Analyze popup content in detail
                await analyze_popup_content(page, report, popup_element, i+1)

                # Close popup before next iteration
                await close_popup(page, report, popup_element)

            else:
                report.append("❌ No popup detected after clicking quest")

                # Try to capture what might be a popup by looking for new elements
                report.append("Searching for any new visible elements...")
                all_visible = await page.query_selector_all("*")
                new_elements = []

                for element in all_visible[-20:]:  # Check last 20 elements
                    try:
                        is_visible = await element.is_visible()
                        if is_visible:
                            tag_name = await element.evaluate("el => el.tagName")
                            text = await element.text_content()
                            if text and len(text.strip()) > 10:
                                new_elements.append(f"{tag_name}: {text.strip()[:100]}")
                    except:
                        continue

                if new_elements:
                    report.append("Possible popup content found:")
                    for elem in new_elements[:5]:
                        report.append(f"  {elem}")

            # Wait a bit before next quest
            await page.wait_for_timeout(1000)

        except Exception as e:
            report.append(f"Error testing quest {i+1}: {e}")

async def analyze_popup_content(page, report, popup_element, quest_number):
    """Analisa o conteúdo detalhado do popup"""

    try:
        report.append(f"\n=== POPUP CONTENT ANALYSIS FOR QUEST {quest_number} ===")

        # Get full popup text
        popup_text = await popup_element.text_content()
        report.append(f"Full popup text: '{popup_text[:500]}...'")

        # Look for specific elements within popup

        # 1. Quest Progress (0/126 format)
        report.append("\n1. QUEST PROGRESS ANALYSIS:")
        progress_patterns = []
        lines = popup_text.split('\n')
        for line in lines:
            line = line.strip()
            if "/" in line and any(char.isdigit() for char in line):
                if "progress" in line.lower() or line.count("/") == 1:
                    progress_patterns.append(line)

        if progress_patterns:
            report.append(f"Found {len(progress_patterns)} progress patterns:")
            for pattern in progress_patterns:
                report.append(f"  Progress: '{pattern}'")
        else:
            report.append("No quest progress patterns found")

        # 2. Success Chance (X% format)
        report.append("\n2. SUCCESS CHANCE ANALYSIS:")
        success_patterns = []
        for line in lines:
            line = line.strip()
            if "%" in line and ("success" in line.lower() or "chance" in line.lower()):
                success_patterns.append(line)

        if success_patterns:
            report.append(f"Found {len(success_patterns)} success chance patterns:")
            for pattern in success_patterns:
                report.append(f"  Success chance: '{pattern}'")
        else:
            report.append("No success chance patterns found")

        # 3. Perform Button
        report.append("\n3. PERFORM BUTTON ANALYSIS:")
        perform_buttons = await popup_element.query_selector_all("button")

        perform_found = []
        for button in perform_buttons:
            try:
                text = await button.text_content()
                if text and "perform" in text.lower():
                    classes = await button.get_attribute("class") or ""
                    disabled = await button.get_attribute("disabled")

                    perform_found.append({
                        'text': text.strip(),
                        'classes': classes,
                        'disabled': disabled,
                        'element': button
                    })
            except:
                continue

        if perform_found:
            report.append(f"Found {len(perform_found)} 'Perform' buttons:")
            for j, btn in enumerate(perform_found):
                report.append(f"  Perform Button {j+1}: '{btn['text']}'")
                report.append(f"    Classes: {btn['classes']}")
                report.append(f"    Disabled: {btn['disabled']}")
        else:
            report.append("No 'Perform' buttons found")

            # List all buttons in popup
            all_buttons = await popup_element.query_selector_all("button")
            report.append(f"All buttons in popup ({len(all_buttons)}):")
            for j, btn in enumerate(all_buttons):
                try:
                    text = await btn.text_content()
                    report.append(f"  Button {j+1}: '{text.strip() if text else '[no text]'}'")
                except:
                    report.append(f"  Button {j+1}: [error reading]")

        # 4. Test Perform button if available and not disabled
        if perform_found:
            await test_perform_in_popup(page, report, perform_found[0], popup_element)

        # 5. Look for other important elements
        report.append("\n4. OTHER POPUP ELEMENTS:")

        # Look for close buttons
        close_buttons = await popup_element.query_selector_all("*")
        close_found = []

        for element in close_buttons:
            try:
                text = await element.text_content()
                if text and any(keyword in text.lower() for keyword in ['close', 'cancel', 'x', '×']):
                    close_found.append(text.strip())
            except:
                continue

        if close_found:
            report.append(f"Close elements found: {close_found}")

    except Exception as e:
        report.append(f"Error analyzing popup content: {e}")

async def test_perform_in_popup(page, report, perform_button_info, popup_element):
    """Testa o botão Perform dentro do popup"""

    try:
        report.append("\n--- TESTING PERFORM BUTTON ---")

        perform_button = perform_button_info['element']

        # Check if button is disabled
        if perform_button_info['disabled']:
            report.append("❌ Perform button is disabled")
            return

        report.append("🖱️ Clicking Perform button...")
        await perform_button.click()
        await page.wait_for_timeout(3000)  # Wait for result

        # Look for "Show Result" button or similar
        report.append("Looking for 'Show Result' button...")

        result_buttons = await popup_element.query_selector_all("button")
        show_result_found = []

        for button in result_buttons:
            try:
                text = await button.text_content()
                if text and any(keyword in text.lower() for keyword in ['result', 'show', 'success', 'failure']):
                    show_result_found.append({
                        'text': text.strip(),
                        'element': button
                    })
            except:
                continue

        if show_result_found:
            report.append(f"✅ Found {len(show_result_found)} result-related buttons:")
            for result_btn in show_result_found:
                report.append(f"  Result button: '{result_btn['text']}'")

                # Test clicking the first result button
                if result_btn == show_result_found[0]:
                    try:
                        report.append(f"🖱️ Clicking '{result_btn['text']}' button...")
                        await result_btn['element'].click()
                        await page.wait_for_timeout(2000)

                        # Check what changed in popup
                        new_popup_text = await popup_element.text_content()
                        report.append(f"Popup text after result: '{new_popup_text[:300]}...'")

                    except Exception as e:
                        report.append(f"❌ Error clicking result button: {e}")
        else:
            report.append("❌ No 'Show Result' button found")

            # Check if popup content changed
            new_popup_text = await popup_element.text_content()
            report.append(f"Popup text after perform: '{new_popup_text[:300]}...'")

    except Exception as e:
        report.append(f"Error testing perform button: {e}")

async def close_popup(page, report, popup_element):
    """Fecha o popup atual"""

    try:
        # Try different ways to close popup
        close_strategies = [
            ("Close button", "button:has-text('Close')"),
            ("X button", "button:has-text('×')"),
            ("Cancel button", "button:has-text('Cancel')"),
            ("ESC key", None),
            ("Click outside", None)
        ]

        for strategy_name, selector in close_strategies:
            try:
                if selector:
                    close_btn = await popup_element.query_selector(selector)
                    if close_btn:
                        await close_btn.click()
                        await page.wait_for_timeout(1000)
                        report.append(f"✅ Closed popup using {strategy_name}")
                        return
                elif strategy_name == "ESC key":
                    await page.keyboard.press('Escape')
                    await page.wait_for_timeout(1000)

                    # Check if popup is still visible
                    is_visible = await popup_element.is_visible()
                    if not is_visible:
                        report.append(f"✅ Closed popup using {strategy_name}")
                        return

            except Exception as e:
                report.append(f"❌ {strategy_name} failed: {e}")
                continue

        report.append("⚠️ Could not close popup, continuing anyway...")

    except Exception as e:
        report.append(f"Error closing popup: {e}")

async def test_perform_buttons(page, report):
    """Testa botões Perform adicionais fora dos popups"""

    try:
        # Look for any Perform buttons on main page
        all_buttons = await page.query_selector_all("button")

        perform_buttons_main = []
        for button in all_buttons:
            try:
                text = await button.text_content()
                if text and "perform" in text.lower():
                    perform_buttons_main.append(button)
            except:
                continue

        report.append(f"Found {len(perform_buttons_main)} Perform buttons on main page:")

        for i, button in enumerate(perform_buttons_main):
            try:
                text = await button.text_content()
                classes = await button.get_attribute("class") or ""
                disabled = await button.get_attribute("disabled")

                report.append(f"  Main Perform {i+1}: '{text.strip()}'")
                report.append(f"    Classes: {classes}")
                report.append(f"    Disabled: {disabled}")

            except Exception as e:
                report.append(f"  Main Perform {i+1}: Error reading - {e}")

    except Exception as e:
        report.append(f"Error in perform buttons test: {e}")

async def main():
    """Função principal"""
    try:
        success = await complete_quest_analysis()
        if success:
            print("\n✅ Análise completa do sistema de quests concluída com sucesso!")
            print("\n📋 Arquivos gerados:")
            print("   📄 quest_system_complete_analysis.txt")
            print("   🌐 quest_system_raw_html.html")
        else:
            print("\n❌ Análise falhou!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    finally:
        print("\n💡 Página mantida aberta para inspeção manual")

if __name__ == "__main__":
    asyncio.run(main())
