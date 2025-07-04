"""
🎮 SimpleMMO Bot GUI Launcher

Entry point for running the bot with the DearPyGui interface.
"""

import sys
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))
sys.path.insert(0, str(current_dir))

# Import and run the DearPyGui interface
from src.ui.bot_gui import main

if __name__ == "__main__":
    main()
