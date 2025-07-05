"""
🤖 SimpleMMO Bot - Entry Point

Modern entry point for the SimpleMMO Bot.
Starts the GUI interface for easy bot control.
"""

import sys
from pathlib import Path

# Add src directory to Python path for direct execution
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(project_root))

# Import GUI
try:
    from src.ui.modern_bot_gui import main as gui_main
except ImportError as e:
    try:
        # Try alternative import path
        import sys

        sys.path.append(str(Path(__file__).parent.parent))
        from src.ui.modern_bot_gui import main as gui_main
    except ImportError as e2:
        print(f"❌ Failed to import Modern GUI: {e}")
        print(f"❌ Alternative import also failed: {e2}")
        print("❌ CustomTkinter GUI não pode ser carregado. Instale as dependências:")
        print("pip install customtkinter")
        sys.exit(1)


def main():
    """
    🚀 Main entry point - Start the GUI
    """
    print("🎮 Starting SimpleMMO Bot GUI...")
    gui_main()


if __name__ == "__main__":
    main()
