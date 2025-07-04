"""
🎮 Modern GUI Demo

Demonstração da nova interface moderna usando CustomTkinter.
Execute este arquivo para ver a interface sem inicializar o bot.
"""

from src.ui.modern_bot_gui import ModernBotGUI


def demo():
    """Demo da GUI moderna"""
    print("🎮 Iniciando demonstração da GUI moderna...")
    print("💡 CustomTkinter oferece:")
    print("  ✅ Interface moderna e bonita")
    print("  ✅ Dark/Light mode automático")
    print("  ✅ Widgets estilizados")
    print("  ✅ Performance excelente")
    print("  ✅ Fácil de usar")

    # Criar e mostrar GUI
    gui = ModernBotGUI()
    gui.run()


if __name__ == "__main__":
    demo()
