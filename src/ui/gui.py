"""
🎮 Interface Simples para Step Bot

Interface moderna com DearPyGUI para controlar o bot de steps.
Simples, completa e bonita.
"""

import asyncio
import sys
import threading
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

import dearpygui.dearpygui as dpg
from loguru import logger


class StepBotGUI:
    """
    🎮 Interface Gráfica Simples para Step Bot

    Features:
    - Controles básicos (Start/Stop)
    - Log em tempo real
    - Estatísticas do bot
    - Interface moderna e responsiva
    """

    def __init__(self):
        """Initialize GUI"""
        self.bot_running = False
        self.bot_task = None
        self.step_system = None
        self.web_engine = None
        self.stats = {
            "steps_taken": 0,
            "successful_steps": 0,
            "failed_steps": 0,
            "status": "Stopped",
        }

        # DearPyGUI setup
        dpg.create_context()

        # Configure theme for better visibility
        with dpg.theme() as global_theme, dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (15, 15, 15, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (40, 40, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 60, 60, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (80, 80, 80, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100, 100, 100, 255))

        dpg.bind_theme(global_theme)

        dpg.create_viewport(
            title="SimpleMMO Step Bot - Modern Edition",
            width=800,
            height=600,
            resizable=True,
            always_on_top=False,
        )
        dpg.setup_dearpygui()

        self._create_ui()

    def _create_ui(self):
        """Create the main UI"""

        # Main window
        with dpg.window(label="SimpleMMO Step Bot", tag="main_window"):
            # Header
            with dpg.group(horizontal=True):
                dpg.add_text("👣 SimpleMMO Step Bot - Modern Edition", tag="title")
                dpg.add_spacer(width=50)
                dpg.add_text("Status:", color=[255, 255, 255])
                dpg.add_text("Stopped", tag="status_text", color=[255, 100, 100])

            dpg.add_separator()

            # Controls
            with dpg.group(label="Controls"):
                dpg.add_text("🎮 Bot Controls", color=[100, 255, 100])

                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="🚀 Start Bot", tag="start_btn", callback=self.start_bot, width=100
                    )
                    dpg.add_button(
                        label="🛑 Stop Bot",
                        tag="stop_btn",
                        callback=self.stop_bot,
                        width=100,
                        enabled=False,
                    )
                    dpg.add_button(
                        label="🔄 Take Single Step",
                        tag="step_btn",
                        callback=self.take_single_step,
                        width=150,
                        enabled=False,
                    )

                dpg.add_separator()

            # Statistics
            with dpg.group(label="Statistics"):
                dpg.add_text("📊 Bot Statistics", color=[100, 255, 100])

                with dpg.group(horizontal=True):
                    with dpg.group():
                        dpg.add_text("Steps Taken:", color=[200, 200, 200])
                        dpg.add_text("0", tag="steps_taken", color=[255, 255, 100])

                    dpg.add_spacer(width=50)

                    with dpg.group():
                        dpg.add_text("Successful:", color=[200, 200, 200])
                        dpg.add_text("0", tag="successful_steps", color=[100, 255, 100])

                    dpg.add_spacer(width=50)

                    with dpg.group():
                        dpg.add_text("Failed:", color=[200, 200, 200])
                        dpg.add_text("0", tag="failed_steps", color=[255, 100, 100])

                dpg.add_separator()

            # Settings
            with dpg.group(label="Settings"):
                dpg.add_text("⚙️ Bot Settings", color=[100, 255, 100])

                with dpg.group(horizontal=True):
                    dpg.add_text("Max Cycles:")
                    dpg.add_input_int(label="", tag="max_cycles", default_value=50, width=100)

                    dpg.add_spacer(width=30)

                    dpg.add_text("Step Delay (s):")
                    dpg.add_input_float(
                        label="", tag="step_delay", default_value=1.5, width=100, step=0.1
                    )

                dpg.add_separator()

            # Log area
            with dpg.group(label="Logs"):
                dpg.add_text("📝 Bot Logs", color=[100, 255, 100])
                dpg.add_child_window(label="Log Window", tag="log_window", height=200, border=True)

        # Set main window as primary
        dpg.set_primary_window("main_window", True)

    def log_message(self, message: str, color: tuple = (255, 255, 255)):
        """Add message to log window"""
        with dpg.window_registry(), dpg.item_handler_registry():
            pass

        # Add to log window
        dpg.add_text(message, color=color, parent="log_window")

        # Auto-scroll to bottom
        try:
            # Get all children and scroll to last
            children = dpg.get_item_children("log_window", slot=1)
            if children and len(children) > 10:  # Keep only last 10 messages
                dpg.delete_item(children[0])
        except Exception:
            pass

    def update_stats(self):
        """Update statistics display"""
        if self.step_system:
            stats = self.step_system.get_step_stats()
            dpg.set_value("steps_taken", str(stats.get("steps_taken", 0)))
            dpg.set_value("successful_steps", str(stats.get("successful_steps", 0)))
            dpg.set_value("failed_steps", str(stats.get("failed_steps", 0)))

    def update_status(self, status: str, color: tuple = (255, 255, 255)):
        """Update bot status"""
        dpg.set_value("status_text", status)
        dpg.configure_item("status_text", color=color)

    def start_bot(self):
        """Start the bot"""
        if self.bot_running:
            return

        self.log_message("🚀 Starting bot...", (100, 255, 100))
        self.bot_running = True

        # Update UI
        dpg.configure_item("start_btn", enabled=False)
        dpg.configure_item("stop_btn", enabled=True)
        dpg.configure_item("step_btn", enabled=True)
        self.update_status("Starting...", (255, 255, 100))

        # Start bot in separate thread
        self.bot_task = threading.Thread(target=self._run_bot_sync, daemon=True)
        self.bot_task.start()

    def stop_bot(self):
        """Stop the bot"""
        if not self.bot_running:
            return

        self.log_message("🛑 Stopping bot...", (255, 100, 100))
        self.bot_running = False

        # Update UI
        dpg.configure_item("start_btn", enabled=True)
        dpg.configure_item("stop_btn", enabled=False)
        dpg.configure_item("step_btn", enabled=False)
        self.update_status("Stopped", (255, 100, 100))

    def take_single_step(self):
        """Take a single step"""
        if not self.step_system:
            self.log_message("❌ Step system not initialized", (255, 100, 100))
            return

        self.log_message("👣 Taking single step...", (100, 255, 255))
        threading.Thread(target=self._single_step_sync, daemon=True).start()

    def _single_step_sync(self):
        """Synchronous wrapper for single step"""
        asyncio.run(self._take_single_step_async())

    async def _take_single_step_async(self):
        """Take a single step asynchronously"""
        try:
            if await self.step_system.is_step_available():
                success = await self.step_system.take_step()
                if success:
                    self.log_message("✅ Single step successful", (100, 255, 100))
                else:
                    self.log_message("⚠️ Single step failed", (255, 255, 100))
            else:
                self.log_message("⏳ No step available", (255, 255, 100))

            self.update_stats()
        except Exception as e:
            self.log_message(f"❌ Error in single step: {e}", (255, 100, 100))

    def _run_bot_sync(self):
        """Synchronous wrapper for bot execution"""
        asyncio.run(self._run_bot_async())

    async def _run_bot_async(self):
        """Run the bot asynchronously"""
        try:
            # Initialize systems
            self.log_message("🌐 Initializing web engine...", (100, 255, 255))
            from src.core.steps import StepSystem
            from src.core.web_engine import get_web_engine

            self.web_engine = await get_web_engine()
            if not self.web_engine:
                self.log_message("❌ Failed to initialize web engine", (255, 100, 100))
                self.stop_bot()
                return

            self.log_message("✅ Web engine ready", (100, 255, 100))

            # Initialize step system
            config = {
                "browser_headless": False,
                "step_delay_min": 1.0,
                "step_delay_max": 2.0,
            }

            self.step_system = StepSystem(config)
            await self.step_system.initialize()
            self.log_message("✅ Step system ready", (100, 255, 100))

            self.update_status("Running", (100, 255, 100))

            # Main bot loop
            cycles = 0
            max_cycles = dpg.get_value("max_cycles")
            step_delay = dpg.get_value("step_delay")

            while self.bot_running and cycles < max_cycles:
                cycles += 1
                self.log_message(f"🔄 Cycle {cycles}/{max_cycles}", (200, 200, 255))

                try:
                    # Check if on travel page
                    if not await self.step_system.is_on_travel_page():
                        self.log_message("🧭 Navigating to travel...", (255, 255, 100))
                        await self.step_system.navigate_to_travel()
                        await asyncio.sleep(2)
                        continue

                    # Check if step available
                    if await self.step_system.is_step_available():
                        self.log_message("👣 Taking step...", (100, 255, 255))
                        success = await self.step_system.take_step()

                        if success:
                            self.log_message("✅ Step successful", (100, 255, 100))
                        else:
                            self.log_message("⚠️ Step failed", (255, 255, 100))

                        self.update_stats()
                        await asyncio.sleep(step_delay)
                    else:
                        self.log_message("⏳ No step available", (255, 255, 100))
                        await asyncio.sleep(3)

                except Exception as e:
                    self.log_message(f"❌ Error in cycle: {e}", (255, 100, 100))
                    await asyncio.sleep(5)

            # Bot finished
            self.log_message(f"🏁 Bot completed {cycles} cycles", (100, 255, 100))
            self.stop_bot()

        except Exception as e:
            self.log_message(f"💥 Fatal error: {e}", (255, 100, 100))
            logger.exception("Full error traceback:")
            self.stop_bot()

    def run(self):
        """Run the GUI"""
        try:
            # Show viewport and start GUI
            dpg.show_viewport()

            # Add a simple test to ensure GUI is working
            self.log_message("🎮 GUI Started Successfully", (100, 255, 100))
            self.log_message("📝 Ready for bot operations", (255, 255, 255))

            # Start the main loop
            while dpg.is_dearpygui_running():
                dpg.render_dearpygui_frame()

        except Exception as e:
            logger.error(f"Error running GUI: {e}")
        finally:
            dpg.destroy_context()


def main():
    """Main entry point"""
    try:
        logger.info("🎮 Starting Step Bot GUI")

        # Create and run GUI
        gui = StepBotGUI()
        gui.run()

    except Exception as e:
        logger.error(f"💥 Fatal error in GUI: {e}")
        logger.exception("Full error traceback:")


if __name__ == "__main__":
    main()
