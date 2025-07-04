"""
🎮 SimpleMMO Bot GUI - DearPyGui Interface

A modern GUI for controlling the SimpleMMO Bot using DearPyGui.
Features Start/Pause/Stop controls, browser launcher, and real-time statistics.
"""

import asyncio
import threading
import time
from pathlib import Path
from typing import Any, Dict, Optional

import dearpygui.dearpygui as dpg
from loguru import logger

# Import bot components
from ..bot_runner import BotRunner
import sys
from pathlib import Path

# Add project root to path for browser_launcher
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from browser_launcher import BrowserLauncher


class BotGUI:
    """
    🎮 Main GUI Controller for SimpleMMO Bot

    Provides a modern interface with real-time controls and monitoring.
    """

    def __init__(self):
        """Initialize the GUI controller"""
        self.bot_runner: Optional[BotRunner] = None
        self.browser_launcher = BrowserLauncher()
        self.bot_thread: Optional[threading.Thread] = None
        self.running = False
        self.paused = False

        # GUI state
        self.stats_window_visible = False
        self.log_window_visible = False

        # Initialize DearPyGui
        dpg.create_context()
        self.setup_theme()
        self.create_main_window()

        # Stats update timer
        self.last_stats_update = time.time()
        self.stats_update_interval = 1.0  # Update every second

    def setup_theme(self):
        """Setup the GUI theme and styling"""
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 30, 255))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (45, 45, 45, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Button, (70, 130, 180, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (100, 149, 237, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (65, 105, 225, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (0, 255, 0, 255))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 8)

        dpg.bind_theme(global_theme)

    def create_main_window(self):
        """Create the main GUI window"""
        with dpg.window(label="🤖 SimpleMMO Bot Control Panel", tag="main_window",
                       width=600, height=400, no_close=True, no_collapse=True):

            # Header
            dpg.add_text("🚀 SimpleMMO Bot - Modern GUI Control", color=(100, 200, 255))
            dpg.add_separator()

            # Control buttons section
            with dpg.group(horizontal=True):
                dpg.add_button(label="🚀 Start Bot", callback=self.start_bot,
                              tag="start_btn", width=120, height=40)
                dpg.add_button(label="⏸️ Pause Bot", callback=self.pause_bot,
                              tag="pause_btn", width=120, height=40, enabled=False)
                dpg.add_button(label="⏹️ Stop Bot", callback=self.stop_bot,
                              tag="stop_btn", width=120, height=40, enabled=False)
                dpg.add_button(label="🌐 Open Browser", callback=self.open_browser,
                              tag="browser_btn", width=120, height=40)

            dpg.add_spacing(count=2)

            # Status section
            dpg.add_text("📊 Bot Status", color=(255, 215, 0))
            dpg.add_separator()

            with dpg.group(horizontal=True):
                dpg.add_text("Status:")
                dpg.add_text("Stopped", tag="status_text", color=(255, 100, 100))

            with dpg.group(horizontal=True):
                dpg.add_text("Cycles:")
                dpg.add_text("0", tag="cycles_text")

            with dpg.group(horizontal=True):
                dpg.add_text("Uptime:")
                dpg.add_text("00:00:00", tag="uptime_text")

            dpg.add_spacing(count=2)

            # Configuration section
            dpg.add_text("⚙️ Configuration", color=(255, 215, 0))
            dpg.add_separator()

            dpg.add_checkbox(label="Auto Healing", tag="auto_heal_cb", default_value=True)
            dpg.add_checkbox(label="Auto Gathering", tag="auto_gather_cb", default_value=True)
            dpg.add_checkbox(label="Auto Combat", tag="auto_combat_cb", default_value=True)
            dpg.add_checkbox(label="Headless Browser", tag="headless_cb", default_value=False)

            dpg.add_spacing(count=2)

            # Additional windows toggle
            with dpg.group(horizontal=True):
                dpg.add_button(label="📈 Show Statistics", callback=self.toggle_stats_window,
                              width=140, height=30)
                dpg.add_button(label="📝 Show Logs", callback=self.toggle_log_window,
                              width=140, height=30)

            dpg.add_spacing(count=3)
            dpg.add_text("💡 Tip: Start the browser first, then start the bot!",
                        color=(200, 200, 200))

        # Create additional windows (hidden by default)
        self.create_stats_window()
        self.create_log_window()

    def create_stats_window(self):
        """Create the statistics window"""
        with dpg.window(label="📈 Bot Statistics", tag="stats_window",
                       width=400, height=300, show=False, pos=(620, 50)):

            dpg.add_text("📊 Real-time Statistics", color=(100, 200, 255))
            dpg.add_separator()

            # Statistics display
            dpg.add_text("Steps Taken: 0", tag="steps_taken_stat")
            dpg.add_text("Successful Steps: 0", tag="successful_steps_stat")
            dpg.add_text("Failed Steps: 0", tag="failed_steps_stat")
            dpg.add_text("Combat Wins: 0", tag="combat_wins_stat")
            dpg.add_text("Gathering Success: 0", tag="gathering_success_stat")
            dpg.add_text("Captchas Solved: 0", tag="captcha_solved_stat")
            dpg.add_text("Health Restored: 0", tag="health_restored_stat")

            dpg.add_spacing(count=2)

            # Success rate calculations
            dpg.add_text("Success Rates:", color=(255, 215, 0))
            dpg.add_separator()
            dpg.add_text("Step Success Rate: 0%", tag="step_success_rate")
            dpg.add_text("Combat Win Rate: 100%", tag="combat_win_rate")

    def create_log_window(self):
        """Create the log window"""
        with dpg.window(label="📝 Bot Logs", tag="log_window",
                       width=500, height=400, show=False, pos=(620, 370)):

            dpg.add_text("📝 Recent Bot Activity", color=(100, 200, 255))
            dpg.add_separator()

            dpg.add_input_text(label="", tag="log_display", multiline=True,
                             readonly=True, height=300, width=460)

            with dpg.group(horizontal=True):
                dpg.add_button(label="Clear Logs", callback=self.clear_logs, width=100)
                dpg.add_button(label="Save Logs", callback=self.save_logs, width=100)

    def start_bot(self):
        """Start the bot in a separate thread"""
        if self.running:
            logger.warning("Bot is already running!")
            return

        try:
            # Get configuration from GUI
            config = {
                "bot_name": "SimpleMMO Bot GUI",
                "log_level": "INFO",
                "browser_headless": dpg.get_value("headless_cb"),
                "auto_heal": dpg.get_value("auto_heal_cb"),
                "auto_gather": dpg.get_value("auto_gather_cb"),
                "auto_combat": dpg.get_value("auto_combat_cb"),
            }

            # Create bot runner
            self.bot_runner = BotRunner(config)

            # Start bot in separate thread
            self.bot_thread = threading.Thread(target=self._run_bot_async, daemon=True)
            self.bot_thread.start()

            # Update UI state
            self.running = True
            self.paused = False
            self._update_button_states()
            self._update_status("Running", (100, 255, 100))

            logger.success("🚀 Bot started successfully!")

        except Exception as e:
            logger.error(f"❌ Failed to start bot: {e}")
            self._update_status("Error", (255, 100, 100))

    def pause_bot(self):
        """Pause or resume the bot"""
        if not self.running:
            return

        if self.bot_runner:
            self.paused = not self.paused
            self.bot_runner.paused = self.paused

            if self.paused:
                dpg.set_item_label("pause_btn", "▶️ Resume Bot")
                self._update_status("Paused", (255, 215, 0))
                logger.info("⏸️ Bot paused")
            else:
                dpg.set_item_label("pause_btn", "⏸️ Pause Bot")
                self._update_status("Running", (100, 255, 100))
                logger.info("▶️ Bot resumed")

    def stop_bot(self):
        """Stop the bot"""
        if not self.running:
            return

        try:
            self.running = False
            if self.bot_runner:
                self.bot_runner.running = False

            # Wait for thread to finish (with timeout)
            if self.bot_thread and self.bot_thread.is_alive():
                self.bot_thread.join(timeout=5.0)

            # Reset UI state
            self.paused = False
            self._update_button_states()
            self._update_status("Stopped", (255, 100, 100))
            dpg.set_item_label("pause_btn", "⏸️ Pause Bot")

            logger.success("⏹️ Bot stopped successfully!")

        except Exception as e:
            logger.error(f"❌ Error stopping bot: {e}")

    def open_browser(self):
        """Open the browser for the game"""
        try:
            # Check if Chromium is available
            if not self.browser_launcher.check_chromium_installed():
                logger.error("❌ Chromium not installed. Run: python -m playwright install chromium")
                return

            # Launch browser
            success = self.browser_launcher.launch_browser()
            if success:
                logger.success("🌐 Browser opened successfully!")
            else:
                logger.error("❌ Failed to open browser")

        except Exception as e:
            logger.error(f"❌ Error opening browser: {e}")

    def toggle_stats_window(self):
        """Toggle the statistics window"""
        self.stats_window_visible = not self.stats_window_visible
        dpg.configure_item("stats_window", show=self.stats_window_visible)

        if self.stats_window_visible:
            dpg.set_item_label("📈 Show Statistics", "📈 Hide Statistics")
        else:
            dpg.set_item_label("📈 Show Statistics", "📈 Show Statistics")

    def toggle_log_window(self):
        """Toggle the log window"""
        self.log_window_visible = not self.log_window_visible
        dpg.configure_item("log_window", show=self.log_window_visible)

        if self.log_window_visible:
            dpg.set_item_label("📝 Show Logs", "📝 Hide Logs")
        else:
            dpg.set_item_label("📝 Show Logs", "📝 Show Logs")

    def clear_logs(self):
        """Clear the log display"""
        dpg.set_value("log_display", "")

    def save_logs(self):
        """Save logs to file"""
        try:
            logs = dpg.get_value("log_display")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"bot_logs_{timestamp}.txt"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(logs)

            logger.success(f"📄 Logs saved to {filename}")

        except Exception as e:
            logger.error(f"❌ Failed to save logs: {e}")

    def _run_bot_async(self):
        """Run the bot asynchronously in a thread"""
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Run the bot
            loop.run_until_complete(self._bot_main_loop())

        except Exception as e:
            logger.error(f"❌ Bot thread error: {e}")
        finally:
            self.running = False
            self._update_status("Stopped", (255, 100, 100))

    async def _bot_main_loop(self):
        """Main bot execution loop"""
        try:
            if not self.bot_runner:
                return

            # Initialize the bot
            await self.bot_runner.initialize()
            self.bot_runner.running = True

            start_time = time.time()

            # Main loop
            while self.running and self.bot_runner.running:
                if not self.paused:
                    # Run bot cycle
                    try:
                        await self.bot_runner.run_cycle()
                    except Exception as e:
                        logger.error(f"❌ Bot cycle error: {e}")
                        await asyncio.sleep(1.0)
                        continue

                # Update GUI stats periodically
                current_time = time.time()
                if current_time - self.last_stats_update >= self.stats_update_interval:
                    self._update_gui_stats(current_time - start_time)
                    self.last_stats_update = current_time

                # Small delay to prevent excessive CPU usage
                await asyncio.sleep(0.1)

        except Exception as e:
            logger.error(f"❌ Bot main loop error: {e}")
        finally:
            if self.bot_runner:
                await self.bot_runner.cleanup()

    def _update_gui_stats(self, uptime: float):
        """Update GUI statistics display"""
        if not self.bot_runner:
            return

        try:
            stats = self.bot_runner.stats

            # Update main window stats
            dpg.set_value("cycles_text", str(stats.get("cycles", 0)))

            # Format uptime
            hours, remainder = divmod(int(uptime), 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            dpg.set_value("uptime_text", uptime_str)

            # Update statistics window if visible
            if self.stats_window_visible:
                dpg.set_value("steps_taken_stat", f"Steps Taken: {stats.get('steps_taken', 0)}")
                dpg.set_value("successful_steps_stat", f"Successful Steps: {stats.get('successful_steps', 0)}")
                dpg.set_value("failed_steps_stat", f"Failed Steps: {stats.get('failed_steps', 0)}")
                dpg.set_value("combat_wins_stat", f"Combat Wins: {stats.get('combat_wins', 0)}")
                dpg.set_value("gathering_success_stat", f"Gathering Success: {stats.get('gathering_success', 0)}")
                dpg.set_value("captcha_solved_stat", f"Captchas Solved: {stats.get('captcha_solved', 0)}")
                dpg.set_value("health_restored_stat", f"Health Restored: {stats.get('health_restored', 0)}")

                # Calculate success rates
                steps_taken = stats.get('steps_taken', 0)
                successful_steps = stats.get('successful_steps', 0)
                if steps_taken > 0:
                    success_rate = (successful_steps / steps_taken) * 100
                    dpg.set_value("step_success_rate", f"Step Success Rate: {success_rate:.1f}%")

        except Exception as e:
            logger.error(f"❌ Error updating GUI stats: {e}")

    def _update_button_states(self):
        """Update button enabled/disabled states"""
        if self.running:
            dpg.configure_item("start_btn", enabled=False)
            dpg.configure_item("pause_btn", enabled=True)
            dpg.configure_item("stop_btn", enabled=True)
        else:
            dpg.configure_item("start_btn", enabled=True)
            dpg.configure_item("pause_btn", enabled=False)
            dpg.configure_item("stop_btn", enabled=False)

    def _update_status(self, status: str, color: tuple):
        """Update the status text and color"""
        dpg.set_value("status_text", status)
        dpg.configure_item("status_text", color=color)

    def run(self):
        """Run the GUI application"""
        try:
            # Setup viewport
            dpg.create_viewport(title="🤖 SimpleMMO Bot - Modern GUI",
                              width=1200, height=800, resizable=True)
            dpg.setup_dearpygui()
            dpg.show_viewport()
            dpg.set_primary_window("main_window", True)

            logger.success("🎮 GUI started successfully!")

            # Main GUI loop
            while dpg.is_dearpygui_running():
                dpg.render_dearpygui_frame()

        except KeyboardInterrupt:
            logger.info("🛑 GUI shutdown requested")
        except Exception as e:
            logger.error(f"❌ GUI error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Cleanup resources before exit"""
        try:
            # Stop bot if running
            if self.running:
                self.stop_bot()

            # Cleanup DearPyGui
            dpg.destroy_context()
            logger.success("🧹 GUI cleanup completed")

        except Exception as e:
            logger.error(f"❌ Cleanup error: {e}")


def main():
    """Main entry point for the GUI application"""
    try:
        logger.info("🚀 Starting SimpleMMO Bot GUI...")

        # Create and run GUI
        gui = BotGUI()
        gui.run()

    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
    finally:
        logger.info("👋 GUI application ended")


if __name__ == "__main__":
    main()
