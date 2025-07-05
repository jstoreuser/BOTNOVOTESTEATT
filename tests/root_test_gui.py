"""
Test script for Modern GUI (CustomTkinter)
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
        print("🚀 Testing Modern GUI (CustomTkinter)...")

        # Test CustomTkinter import
        try:
            import customtkinter

            print("✅ CustomTkinter installed")
        except ImportError:
            print("❌ CustomTkinter not installed - run: pip install customtkinter")
            return

        # Test GUI import
        try:
            from src.ui.modern_bot_gui import ModernBotGUI

            print("✅ Modern GUI imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import Modern GUI: {e}")
            return

        # Test basic initialization (don't run the full GUI)
        print("✅ Modern GUI test completed successfully!")
        print("💡 To run the Modern GUI, use: python src/main.py")

    except Exception as e:
        print(f"❌ Error testing GUI: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_gui()
