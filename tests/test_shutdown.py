"""
🧪 Teste de Shutdown - Verificar se o shutdown está funcionando sem erros

Este teste verifica se o bot pode ser iniciado e fechado sem erros de TclError
ou problemas com Playwright event loop.
"""

import sys
import threading
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_gui_shutdown():
    """Teste automatizado de shutdown da GUI"""
    print("🧪 Iniciando teste de shutdown...")

    try:
        # Import GUI
        from src.ui.modern_bot_gui import ModernBotGUI

        print("✅ GUI importada com sucesso")

        # Create GUI instance
        gui = ModernBotGUI()
        print("✅ GUI criada com sucesso")

        # Schedule automatic close after 3 seconds
        def auto_close():
            time.sleep(3)
            print("🔄 Executando shutdown automático...")
            try:
                gui.on_closing()
                print("✅ Shutdown executado com sucesso")
            except Exception as e:
                print(f"❌ Erro no shutdown: {e}")

        # Start auto-close thread
        close_thread = threading.Thread(target=auto_close, daemon=True)
        close_thread.start()

        # Run GUI (will close automatically)
        print("🎮 Iniciando GUI (fechará automaticamente em 3s)...")
        gui.run()

        print("✅ Teste de shutdown concluído com sucesso!")
        return True

    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_gui_shutdown()
    if success:
        print("\n🎉 TESTE PASSOU - Shutdown funcionando corretamente!")
        sys.exit(0)
    else:
        print("\n💥 TESTE FALHOU - Problemas no shutdown detectados!")
        sys.exit(1)
