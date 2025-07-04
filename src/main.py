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
    from ui.bot_gui import main as gui_main
except ImportError as e:
    print(f"❌ Failed to import GUI: {e}")
    sys.exit(1)


def main():
    """
    🚀 Main entry point - Start the GUI
    """
    print("🎮 Starting SimpleMMO Bot GUI...")
    gui_main()


if __name__ == "__main__":
    main()
