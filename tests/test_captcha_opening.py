"""
🧪 Teste do Sistema de Captcha

Teste específico para verificar se o sistema de captcha está abrindo
corretamente em nova aba (como clique do meio do mouse).
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


async def test_captcha_opening():
    """Teste de abertura de captcha em nova aba"""
    print("🧪 Testando sistema de captcha...")

    try:
        from src.automation.web_engine import get_web_engine
        from src.systems.captcha import CaptchaSystem

        # Initialize web engine
        print("🌐 Inicializando web engine...")
        engine = await get_web_engine()

        # Navigate to travel page
        print("🧭 Navegando para página travel...")
        page = await engine.get_page()
        if page:
            await page.goto("https://web.simple-mmo.com/travel")
            await asyncio.sleep(2)

        # Initialize captcha system
        print("🔒 Inicializando sistema de captcha...")
        captcha_system = CaptchaSystem()
        await captcha_system.initialize()

        # Check if captcha is present
        print("🔍 Verificando se captcha está presente...")
        is_present = await captcha_system.is_captcha_present()

        if is_present:
            print("🔒 Captcha detectado! Testando abertura em nova aba...")

            # Test clicking captcha button
            clicked = await captcha_system._click_captcha_button()
            if clicked:
                print("✅ Captcha button clicado com sucesso!")

                # Wait for tab to open
                tab_found = await captcha_system._wait_for_captcha_tab()
                if tab_found:
                    print("✅ Tab de captcha encontrada!")
                    print("💡 Agora você pode resolver o captcha manualmente na nova aba")
                else:
                    print("❌ Tab de captcha não foi encontrada")
            else:
                print("❌ Falha ao clicar no botão de captcha")
        else:
            print("ℹ️ Nenhum captcha detectado na página atual")
            print("💡 Navegue até uma página que tenha captcha para testar")

        print("🧪 Teste concluído!")
        return True

    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback

        traceback.print_exc()
        return False


async def main():
    """Main test function"""
    success = await test_captcha_opening()
    if success:
        print("\n🎉 Teste concluído!")
    else:
        print("\n💥 Teste falhou!")


if __name__ == "__main__":
    asyncio.run(main())
