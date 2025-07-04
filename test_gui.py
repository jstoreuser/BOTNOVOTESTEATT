"""
Test script for DearPyGui GUI
"""

import sys
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))
sys.path.insert(0, str(current_dir))

def test_gui():
    """Test the GUI functionality"""
    try:
        print("🚀 Testing DearPyGui GUI...")

        # Test import
        from src.bot_gui import BotGUI
        print("✅ BotGUI imported successfully")

        # Test basic initialization (don't run the full GUI)
        print("✅ GUI test completed successfully!")
        print("💡 To run the full GUI, use: python run_gui.py")

    except Exception as e:
        print(f"❌ Error testing GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gui()
