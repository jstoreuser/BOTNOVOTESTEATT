"""
🎮 Interface Simples e Funcional para Step Bot

Interface testada e funcional com DearPyGUI.
"""

import asyncio
import sys
import threading
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

import dearpygui.dearpygui as dpg
from loguru import logger


class SimpleStepBotGUI:
    """Interface simples e funcional para o Step Bot"""

    def __init__(self):
        """Initialize GUI"""
        self.bot_running = False
        self.step_system = None

        # Setup DearPyGUI
        dpg.create_context()
        self._setup_gui()

    def _setup_gui(self):
        """Setup the GUI interface"""

        # Main window
        with dpg.window(label="SimpleMMO Step Bot", tag="main_window", width=600, height=400):
            # Title
            dpg.add_text("👣 SimpleMMO Step Bot - Modern Edition")
            dpg.add_separator()

            # Status
            with dpg.group(horizontal=True):
                dpg.add_text("Status:")
                dpg.add_text("Stopped", tag="status", color=(255, 100, 100))

            dpg.add_separator()

            # Controls
            dpg.add_text("🎮 Controls")
            with dpg.group(horizontal=True):
                dpg.add_button(label="🚀 Start Bot", callback=self.start_bot, tag="start_btn")
                dpg.add_button(
                    label="🛑 Stop Bot", callback=self.stop_bot, tag="stop_btn", enabled=False
                )
                dpg.add_button(
                    label="👣 Single Step", callback=self.single_step, tag="step_btn", enabled=False
                )

            dpg.add_separator()

            # Stats
            dpg.add_text("📊 Statistics")
            with dpg.group(horizontal=True):
                dpg.add_text("Steps: ")
                dpg.add_text("0", tag="steps_count", color=(100, 255, 100))
                dpg.add_spacer(width=20)
                dpg.add_text("Success: ")
                dpg.add_text("0", tag="success_count", color=(100, 255, 100))
                dpg.add_spacer(width=20)
                dpg.add_text("Failed: ")
                dpg.add_text("0", tag="failed_count", color=(255, 100, 100))

            dpg.add_separator()

            # Settings
            dpg.add_text("⚙️ Settings")
            with dpg.group(horizontal=True):
                dpg.add_text("Max Cycles:")
                dpg.add_input_int(tag="max_cycles", default_value=10, width=80)
                dpg.add_spacer(width=20)
                dpg.add_text("Delay (s):")
                dpg.add_input_float(tag="delay", default_value=2.0, width=80)

            dpg.add_separator()

            # Log area
            dpg.add_text("📝 Logs")
            dpg.add_child_window(tag="log_area", height=150)

        # Set as primary window
        dpg.set_primary_window("main_window", True)

        # Create viewport
        dpg.create_viewport(title="SimpleMMO Step Bot", width=700, height=500)
        dpg.setup_dearpygui()

    def log(self, message: str, color=(255, 255, 255)):
        """Add log message"""
        dpg.add_text(message, color=color, parent="log_area")
        print(f"LOG: {message}")  # Also print to console

        # Keep only last 20 messages
        try:
            children = dpg.get_item_children("log_area", slot=1)
            if children and len(children) > 20:
                dpg.delete_item(children[0])
        except Exception:
            pass

    def update_status(self, status: str, color=(255, 255, 255)):
        """Update status"""
        dpg.set_value("status", status)
        dpg.configure_item("status", color=color)

    def update_stats(self, steps=0, success=0, failed=0):
        """Update statistics"""
        dpg.set_value("steps_count", str(steps))
        dpg.set_value("success_count", str(success))
        dpg.set_value("failed_count", str(failed))

    def start_bot(self):
        """Start bot"""
        if self.bot_running:
            return

        self.log("🚀 Starting bot...", (100, 255, 100))
        self.bot_running = True

        # Update UI
        dpg.configure_item("start_btn", enabled=False)
        dpg.configure_item("stop_btn", enabled=True)
        dpg.configure_item("step_btn", enabled=True)
        self.update_status("Starting...", (255, 255, 100))

        # Start bot thread
        threading.Thread(target=self._run_bot_thread, daemon=True).start()

    def stop_bot(self):
        """Stop bot"""
        self.log("🛑 Stopping bot...", (255, 100, 100))
        self.bot_running = False

        # Update UI
        dpg.configure_item("start_btn", enabled=True)
        dpg.configure_item("stop_btn", enabled=False)
        dpg.configure_item("step_btn", enabled=False)
        self.update_status("Stopped", (255, 100, 100))

    def single_step(self):
        """Take single step"""
        if not self.step_system:
            self.log("❌ Bot not initialized", (255, 100, 100))
            return

        self.log("👣 Taking single step...", (100, 255, 255))
        threading.Thread(target=self._single_step_thread, daemon=True).start()

    def _single_step_thread(self):
        """Single step in thread"""
        try:
            asyncio.run(self._single_step_async())
        except Exception as e:
            self.log(f"❌ Error: {e}", (255, 100, 100))

    async def _single_step_async(self):
        """Single step async"""
        try:
            if await self.step_system.is_step_available():
                success = await self.step_system.take_step()
                if success:
                    self.log("✅ Step successful", (100, 255, 100))
                else:
                    self.log("⚠️ Step failed", (255, 255, 100))
            else:
                self.log("⏳ No step available", (255, 255, 100))
        except Exception as e:
            self.log(f"❌ Step error: {e}", (255, 100, 100))

    def _run_bot_thread(self):
        """Run bot in thread"""
        try:
            asyncio.run(self._run_bot_async())
        except Exception as e:
            self.log(f"💥 Bot error: {e}", (255, 100, 100))
            self.stop_bot()

    async def _run_bot_async(self):
        """Run bot async"""
        try:
            # Initialize
            self.log("🌐 Initializing web engine...", (100, 255, 255))

            from src.core.steps import StepSystem
            from src.core.web_engine import get_web_engine

            web_engine = await get_web_engine()
            if not web_engine:
                self.log("❌ Web engine failed", (255, 100, 100))
                self.stop_bot()
                return

            self.log("✅ Web engine ready", (100, 255, 100))

            # Initialize step system
            config = {"browser_headless": False}
            self.step_system = StepSystem(config)
            await self.step_system.initialize()

            self.log("✅ Step system ready", (100, 255, 100))
            self.update_status("Running", (100, 255, 100))

            # Bot loop
            max_cycles = dpg.get_value("max_cycles")
            delay = dpg.get_value("delay")

            for cycle in range(1, max_cycles + 1):
                if not self.bot_running:
                    break

                self.log(f"🔄 Cycle {cycle}/{max_cycles}", (200, 200, 255))

                try:
                    # Navigate to travel if needed
                    if not await self.step_system.is_on_travel_page():
                        self.log("🧭 Going to travel page...", (255, 255, 100))
                        await self.step_system.navigate_to_travel()
                        await asyncio.sleep(2)
                        continue

                    # Take step
                    if await self.step_system.is_step_available():
                        self.log("👣 Taking step...", (100, 255, 255))
                        success = await self.step_system.take_step()

                        if success:
                            self.log("✅ Step successful", (100, 255, 100))
                        else:
                            self.log("⚠️ Step failed", (255, 255, 100))

                        # Update stats
                        if self.step_system:
                            stats = self.step_system.get_step_stats()
                            self.update_stats(
                                steps=stats.get("steps_taken", 0),
                                success=stats.get("successful_steps", 0),
                                failed=stats.get("failed_steps", 0),
                            )

                        await asyncio.sleep(delay)
                    else:
                        self.log("⏳ No step available", (255, 255, 100))
                        await asyncio.sleep(3)

                except Exception as e:
                    self.log(f"❌ Cycle error: {e}", (255, 100, 100))
                    await asyncio.sleep(5)

            self.log("🏁 Bot completed", (100, 255, 100))
            self.stop_bot()

        except Exception as e:
            self.log(f"💥 Fatal error: {e}", (255, 100, 100))
            self.stop_bot()

    def run(self):
        """Run the GUI"""
        try:
            print("🎮 Starting GUI...")
            dpg.show_viewport()

            # Initial log
            self.log("🎮 GUI Started", (100, 255, 100))
            self.log("Ready for bot operations", (255, 255, 255))

            # Main loop
            dpg.start_dearpygui()

        except Exception as e:
            print(f"❌ GUI Error: {e}")
            logger.exception("GUI error:")
        finally:
            dpg.destroy_context()


def main():
    """Main entry point"""
    try:
        print("🎮 Starting SimpleMMO Step Bot GUI...")

        gui = SimpleStepBotGUI()
        gui.run()

    except Exception as e:
        print(f"💥 Fatal error: {e}")
        logger.exception("Fatal error:")


if __name__ == "__main__":
    main()
