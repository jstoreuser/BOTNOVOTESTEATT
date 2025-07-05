"""
Quest automation module for SimpleMMO bot.
Handles quest detection, execution, and management.
"""

from typing import Dict, List, Optional, Tuple, Any
from automation.web_engine import get_page, get_web_engine
import asyncio
import re
import logging

logger = logging.getLogger(__name__)


class QuestAutomation:
    """Handles quest automation for SimpleMMO."""

    # Seletores extraídos da análise
    SELECTORS = {
        "quest_points": [
            "[x-text*='quest_points']",
            ".text-indigo-600",
            "span[x-text='number_format(quest_points)']"
        ],
        "quest_tabs": [
            "px-3 py-2 font-medium text-sm rounded-md",
            "button:has-text('All')",
            "button:has-text('Not Completed')",
            "button:has-text('Completed')"
        ],
        "quest_items": [
            "button.bg-white.rounded-lg",
            ".bg-white.rounded-lg",
            "button[onclick*='quest']"
        ],
        "quest_level": [
            "*:has-text('Level')",
            ".font-medium:has-text('Level')"
        ],
        "quest_left": [
            "*:has-text('left')",
            ".text-gray-500:has-text('left')"
        ],
        "perform_buttons": [
            "button:has-text('Perform')",
            ".bg-indigo-600:has-text('Perform')",
            "button[onclick*='perform']"
        ],
        "popup_elements": [
            "*[style*='z-index']",
            ".modal",
            ".popup",
            "[aria-modal='true']"
        ],
        "close_buttons": [
            "button:has-text('Close')",
            "button:has-text('Cancel')",
            ".close",
            "[aria-label='Close']"
        ]
    }

    def __init__(self):
        self.web_engine = None  # Will be set when needed
        self.current_quest_points = 0
        self.max_quest_points = 0
        self.available_quests: List[Dict[str, Any]] = []

    async def navigate_to_quests(self) -> bool:
        """Navega para a página de quests."""
        try:
            logger.info("🎯 Navegando para página de quests...")

            page = await get_page()
            if not page:
                logger.error("❌ Página não disponível")
                return False

            await page.goto('https://web.simple-mmo.com/quests', wait_until='networkidle')
            await page.wait_for_timeout(2000)

            # Verifica se chegou na página correta
            current_url = page.url
            if "quests" not in current_url.lower():
                logger.error(f"❌ Falha ao navegar - URL atual: {current_url}")
                return False

            logger.info("✅ Navegação para quests concluída")
            return True

        except Exception as e:
            logger.error(f"❌ Erro ao navegar para quests: {str(e)}")
            return False

    async def get_quest_points(self) -> Tuple[int, int]:
        """Obtém os quest points atuais e máximos."""
        try:
            page = await get_page()
            if not page:
                return 0, 0

            # Tenta diferentes seletores para quest points
            for selector in self.SELECTORS["quest_points"]:
                try:
                    elements = await page.query_selector_all(selector)
                    for element in elements:
                        text = await element.text_content()
                        if text and text.strip():
                            # Procura por padrão X/Y
                            match = re.search(r'(\d+)/(\d+)', text)
                            if match:
                                current = int(match.group(1))
                                maximum = int(match.group(2))
                                self.current_quest_points = current
                                self.max_quest_points = maximum
                                logger.info(f"🎯 Quest Points: {current}/{maximum}")
                                return current, maximum

                            # Procura por número isolado
                            match = re.search(r'(\d+)', text)
                            if match:
                                points = int(match.group(1))
                                if points > 0:
                                    self.current_quest_points = points
                                    logger.info(f"🎯 Quest Points encontrados: {points}")
                                    return points, points
                except:
                    continue

            logger.warning("⚠️ Quest points não encontrados")
            return 0, 0

        except Exception as e:
            logger.error(f"❌ Erro ao obter quest points: {str(e)}")
            return 0, 0

    async def switch_to_not_completed_tab(self) -> bool:
        """Muda para a aba 'Not Completed'."""
        try:
            page = await get_page()
            if not page:
                return False

            # Procura pelo botão "Not Completed"
            selectors_to_try = [
                "button:has-text('Not Completed')",
                ".px-3.py-2:has-text('Not Completed')",
                "*:has-text('Not Completed')"
            ]

            for selector in selectors_to_try:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        await element.click()
                        await page.wait_for_timeout(1000)
                        logger.info("✅ Mudou para aba 'Not Completed'")
                        return True
                except:
                    continue

            logger.warning("⚠️ Aba 'Not Completed' não encontrada")
            return False

        except Exception as e:
            logger.error(f"❌ Erro ao mudar para aba Not Completed: {str(e)}")
            return False

    async def get_available_quests(self) -> List[Dict[str, Any]]:
        """Obtém lista de quests disponíveis."""
        try:
            page = await get_page()
            if not page:
                return []

            quests = []

            # Procura por elementos que contêm quests
            for selector in self.SELECTORS["quest_items"]:
                try:
                    elements = await page.query_selector_all(selector)

                    for i, element in enumerate(elements):
                        try:
                            text = await element.text_content()
                            if not text or len(text.strip()) < 10:
                                continue

                            # Extrai informações do quest
                            quest_info = {
                                "index": i,
                                "selector": selector,
                                "element": element,
                                "text": text.strip(),
                                "name": "",
                                "level": 0,
                                "left": 0,
                                "clickable": True
                            }

                            # Extrai nome do quest (primeira linha)
                            lines = text.strip().split('\n')
                            if lines:
                                quest_info["name"] = lines[0].strip()

                            # Extrai level
                            level_match = re.search(r'Level (\d+)', text)
                            if level_match:
                                quest_info["level"] = int(level_match.group(1))

                            # Extrai quantidade restante
                            left_match = re.search(r'(\d+) left', text)
                            if left_match:
                                quest_info["left"] = int(left_match.group(1))

                            # Só adiciona se parece ser um quest válido
                            if quest_info["name"] and quest_info["level"] > 0:
                                quests.append(quest_info)

                        except:
                            continue

                except:
                    continue

            # Remove duplicatas baseado no nome
            unique_quests = []
            seen_names = set()

            for quest in quests:
                if quest["name"] not in seen_names:
                    seen_names.add(quest["name"])
                    unique_quests.append(quest)

            # Ordena por level (do menor para o maior)
            unique_quests.sort(key=lambda x: x["level"])

            self.available_quests = unique_quests
            logger.info(f"📋 Encontrados {len(unique_quests)} quests disponíveis")

            return unique_quests

        except Exception as e:
            logger.error(f"❌ Erro ao obter quests disponíveis: {str(e)}")
            return []

    async def click_quest(self, quest: Dict[str, Any]) -> bool:
        """Clica em um quest específico."""
        try:
            element = quest.get("element")
            if not element:
                logger.error("❌ Elemento do quest não encontrado")
                return False

            logger.info(f"🎯 Clicando no quest: {quest['name']}")

            # Scroll para o elemento e clica
            await element.scroll_into_view_if_needed()
            await element.click()
            await asyncio.sleep(1)

            return True

        except Exception as e:
            logger.error(f"❌ Erro ao clicar no quest: {str(e)}")
            return False

    async def find_perform_button(self) -> Optional[Any]:
        """Procura pelo botão Perform no popup ou na página."""
        try:
            page = await get_page()
            if not page:
                return None

            # Tenta diferentes seletores para o botão Perform
            perform_selectors = [
                "button:has-text('Perform')",
                ".bg-indigo-600:has-text('Perform')",
                "button[onclick*='perform']",
                "*:has-text('1x Perform')",
                ".bg-indigo-600.text-white:has-text('Perform')"
            ]

            for selector in perform_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    for element in elements:
                        is_visible = await element.is_visible()
                        if is_visible:
                            text = await element.text_content()
                            if text and 'perform' in text.lower():
                                logger.info(f"✅ Botão Perform encontrado: {text.strip()}")
                                return element
                except:
                    continue

            logger.warning("⚠️ Botão Perform não encontrado")
            return None

        except Exception as e:
            logger.error(f"❌ Erro ao procurar botão Perform: {str(e)}")
            return None

    async def perform_quest(self) -> bool:
        """Executa um quest (clica no botão Perform)."""
        try:
            # Procura pelo botão Perform
            perform_button = await self.find_perform_button()
            if not perform_button:
                return False

            logger.info("⚡ Executando quest...")
            await perform_button.click()
            await asyncio.sleep(2)

            # Verifica se houve mudança na página ou popup de resultado
            page = await get_page()
            if page:
                # Procura por indicadores de sucesso/resultado
                result_selectors = [
                    "*:has-text('Success')",
                    "*:has-text('Failed')",
                    "*:has-text('Completed')",
                    "*:has-text('Experience')",
                    "*:has-text('Gold')",
                    ".modal",
                    ".popup"
                ]

                for selector in result_selectors:
                    try:
                        elements = await page.query_selector_all(selector)
                        if elements:
                            element = elements[0]
                            is_visible = await element.is_visible()
                            if is_visible:
                                text = await element.text_content()
                                if text:
                                    logger.info(f"📊 Resultado: {text[:100]}...")
                                break
                    except:
                        continue

            logger.info("✅ Quest executado")
            return True

        except Exception as e:
            logger.error(f"❌ Erro ao executar quest: {str(e)}")
            return False

    async def close_popups(self) -> bool:
        """Fecha popups abertos."""
        try:
            page = await get_page()
            if not page:
                return False

            # Tenta diferentes métodos para fechar popups
            close_methods = [
                # Botões de fechar
                "button:has-text('Close')",
                "button:has-text('Cancel')",
                ".close",
                "[aria-label='Close']",
                # Tecla ESC
                "body"  # Para pressionar ESC
            ]

            for method in close_methods[:-1]:  # Não inclui o body ainda
                try:
                    elements = await page.query_selector_all(method)
                    for element in elements:
                        is_visible = await element.is_visible()
                        if is_visible:
                            await element.click()
                            await asyncio.sleep(0.5)
                            logger.info(f"✅ Popup fechado com {method}")
                            return True
                except:
                    continue

            # Tenta pressionar ESC
            try:
                await page.keyboard.press('Escape')
                await asyncio.sleep(0.5)
                logger.info("✅ Popup fechado com ESC")
                return True
            except:
                pass

            logger.warning("⚠️ Não foi possível fechar popup")
            return False

        except Exception as e:
            logger.error(f"❌ Erro ao fechar popup: {str(e)}")
            return False

    async def execute_quests_cycle(self, max_quests: int = 5) -> Dict[str, Any]:
        """Executa um ciclo completo de quests."""
        results = {
            "quests_attempted": 0,
            "quests_successful": 0,
            "quest_points_used": 0,
            "errors": []
        }

        try:
            logger.info("🚀 Iniciando ciclo de quests...")

            # Navega para a página de quests
            if not await self.navigate_to_quests():
                results["errors"].append("Falha ao navegar para quests")
                return results

            # Obtém quest points atuais
            current_points, max_points = await self.get_quest_points()
            if current_points <= 0:
                results["errors"].append("Sem quest points disponíveis")
                return results

            # Muda para aba "Not Completed"
            await self.switch_to_not_completed_tab()

            # Obtém lista de quests
            quests = await self.get_available_quests()
            if not quests:
                results["errors"].append("Nenhum quest disponível")
                return results

            # Executa quests até o limite ou até acabar os points
            quests_to_execute = min(max_quests, current_points, len(quests))

            for i in range(quests_to_execute):
                if i >= len(quests):
                    break

                quest = quests[i]
                logger.info(f"🎯 Executando quest {i+1}/{quests_to_execute}: {quest['name']}")

                results["quests_attempted"] += 1

                # Clica no quest
                if await self.click_quest(quest):
                    await asyncio.sleep(1)

                    # Executa o quest
                    if await self.perform_quest():
                        results["quests_successful"] += 1
                        results["quest_points_used"] += 1

                        # Fecha popups
                        await self.close_popups()
                        await asyncio.sleep(1)

                        # Volta para a página de quests
                        await self.navigate_to_quests()
                        await self.switch_to_not_completed_tab()
                    else:
                        results["errors"].append(f"Falha ao executar quest: {quest['name']}")
                        await self.close_popups()
                else:
                    results["errors"].append(f"Falha ao clicar no quest: {quest['name']}")

                # Pausa entre quests
                await asyncio.sleep(2)

            logger.info(f"✅ Ciclo de quests concluído: {results['quests_successful']}/{results['quests_attempted']} sucessos")

        except Exception as e:
            error_msg = f"Erro no ciclo de quests: {str(e)}"
            logger.error(f"❌ {error_msg}")
            results["errors"].append(error_msg)

        return results
