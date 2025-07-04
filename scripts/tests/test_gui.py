"""
🎮 Teste de Interface DearPyGUI

Teste simples para verificar se a interface está funcionando corretamente.
"""

import dearpygui.dearpygui as dpg


def main():
    """Teste principal da interface."""
    # Create context and viewport
    dpg.create_context()

    # Create viewport
    dpg.create_viewport(title="🎮 Teste DearPyGUI - SimpleMMO Bot", width=400, height=300)

    # Create a simple window
    with dpg.window(label="🎮 Teste de Interface", tag="test_window", width=350, height=250):
        dpg.add_text("🎮 Teste de Interface DearPyGUI")
        dpg.add_separator()
        dpg.add_button(label="🔘 Botão Teste", callback=lambda: print("✅ Botão clicado!"))
        dpg.add_text("Se você vê esta janela, DearPyGUI está funcionando!")
        dpg.add_separator()
        dpg.add_text("📝 Status: Interface OK")

    # Set primary window
    dpg.set_primary_window("test_window", True)

    # Setup and show
    dpg.setup_dearpygui()
    dpg.show_viewport()

    # Start GUI loop
    dpg.start_dearpygui()

    # Cleanup
    dpg.destroy_context()


if __name__ == "__main__":
    main()
