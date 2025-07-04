"""
🎮 Modern SimpleMMO Bot GUI - CustomTkinter Interface

Ultra-modern GUI using CustomTkinter with:
- Beautiful dark/light themes
- Real-time statistics
- Live configuration updates
- Professional design
"""

import asyncio
import threading
from datetime import datetime
from pathlib import Path

import customtkinter as ctk
from loguru import logger

# Import bot components
try:
    from ..bot_runner import BotRunner
except ImportError:
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent))
    from src.bot_runner import BotRunner

try:
    from browser_launcher import BrowserLauncher
except ImportError:
    pass


class ModernBotGUI:
    """
    🎮 Modern GUI Controller for SimpleMMO Bot using CustomTkinter

    Features:
    - Beautiful modern interface
    - Real-time configuration updates
    - Live statistics and logs
    - Professional design
    """

    def __init__(self):
        """Initialize the modern GUI"""
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")  # Options: "dark", "light", "system"
        ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

        # Create main window
        self.root = ctk.CTk()
        self.root.title("🤖 SimpleMMO Bot - Modern Interface")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        # Bot state
        self.bot_runner: BotRunner | None = None
        self.bot_thread: threading.Thread | None = None
        self.running = False
        self.paused = False
        self.start_time = None

        # GUI update flags
        self.update_running = False

        # Create GUI
        self._create_widgets()
        self._start_gui_updater()

        logger.info("🎮 Modern GUI initialized")

    def _create_widgets(self):
        """Create and arrange GUI widgets"""
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Title frame
        self._create_title_frame()

        # Main content frame
        self._create_main_content()

        # Status bar
        self._create_status_bar()

    def _create_title_frame(self):
        """Create title and main controls"""
        title_frame = ctk.CTkFrame(self.root, height=100)
        title_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        title_frame.grid_columnconfigure(1, weight=1)

        # Title
        title_label = ctk.CTkLabel(
            title_frame, text="🤖 SimpleMMO Bot", font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Main control buttons
        self.start_btn = ctk.CTkButton(
            title_frame,
            text="🚀 Start Bot",
            command=self.start_bot,
            width=120,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.start_btn.grid(row=1, column=0, padx=5, pady=5)

        self.pause_btn = ctk.CTkButton(
            title_frame,
            text="⏸️ Pause",
            command=self.pause_bot,
            width=120,
            height=40,
            state="disabled",
        )
        self.pause_btn.grid(row=1, column=1, padx=5, pady=5)

        self.stop_btn = ctk.CTkButton(
            title_frame,
            text="🛑 Stop",
            command=self.stop_bot,
            width=120,
            height=40,
            state="disabled",
            fg_color="red",
            hover_color="darkred",
        )
        self.stop_btn.grid(row=1, column=2, padx=5, pady=5)

        # Browser button
        self.browser_btn = ctk.CTkButton(
            title_frame, text="🌐 Open Browser", command=self.open_browser, width=120, height=40
        )
        self.browser_btn.grid(row=1, column=3, padx=5, pady=5)

    def _create_main_content(self):
        """Create main content area with tabs"""
        # Create tabview
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        # Control tab
        self.tabview.add("⚙️ Control")
        self._create_control_tab()

        # Statistics tab
        self.tabview.add("📊 Statistics")
        self._create_statistics_tab()

        # Logs tab
        self.tabview.add("📝 Logs")
        self._create_logs_tab()

        # Set default tab
        self.tabview.set("⚙️ Control")

    def _create_control_tab(self):
        """Create control and configuration tab"""
        control_frame = self.tabview.tab("⚙️ Control")
        control_frame.grid_columnconfigure(0, weight=1)

        # Configuration section
        config_frame = ctk.CTkFrame(control_frame)
        config_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        config_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            config_frame, text="🔧 Bot Configuration", font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)

        # Configuration switches
        self.auto_heal_var = ctk.BooleanVar(value=True)
        self.auto_heal_switch = ctk.CTkSwitch(
            config_frame,
            text="Auto Healing",
            variable=self.auto_heal_var,
            command=self._on_config_change,
        )
        self.auto_heal_switch.grid(row=1, column=0, sticky="w", padx=20, pady=5)

        self.auto_gather_var = ctk.BooleanVar(value=True)
        self.auto_gather_switch = ctk.CTkSwitch(
            config_frame,
            text="Auto Gathering",
            variable=self.auto_gather_var,
            command=self._on_config_change,
        )
        self.auto_gather_switch.grid(row=2, column=0, sticky="w", padx=20, pady=5)

        self.auto_combat_var = ctk.BooleanVar(value=True)
        self.auto_combat_switch = ctk.CTkSwitch(
            config_frame,
            text="Auto Combat",
            variable=self.auto_combat_var,
            command=self._on_config_change,
        )
        self.auto_combat_switch.grid(row=3, column=0, sticky="w", padx=20, pady=5)

        self.headless_var = ctk.BooleanVar(value=False)
        self.headless_switch = ctk.CTkSwitch(
            config_frame,
            text="Headless Browser",
            variable=self.headless_var,
            command=self._on_config_change,
        )
        self.headless_switch.grid(row=4, column=0, sticky="w", padx=20, pady=5)

        # Quick stats in control tab
        quick_stats_frame = ctk.CTkFrame(control_frame)
        quick_stats_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        quick_stats_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            quick_stats_frame, text="📈 Quick Stats", font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)

        # Status indicator
        self.status_frame = ctk.CTkFrame(quick_stats_frame)
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=5)

        self.status_label = ctk.CTkLabel(
            self.status_frame, text="⏹️ Stopped", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.status_label.pack(pady=10)

        # Quick info
        self.cycles_label = ctk.CTkLabel(quick_stats_frame, text="Cycles: 0")
        self.cycles_label.grid(row=2, column=0, sticky="w", padx=20, pady=2)

        self.uptime_label = ctk.CTkLabel(quick_stats_frame, text="Uptime: 00:00:00")
        self.uptime_label.grid(row=3, column=0, sticky="w", padx=20, pady=2)

    def _create_statistics_tab(self):
        """Create detailed statistics tab"""
        stats_frame = self.tabview.tab("📊 Statistics")
        stats_frame.grid_columnconfigure(0, weight=1)

        # Create scrollable frame for stats
        self.stats_scroll = ctk.CTkScrollableFrame(stats_frame)
        self.stats_scroll.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        stats_frame.grid_rowconfigure(0, weight=1)

        # Stats will be populated dynamically
        self.stats_labels = {}

    def _create_logs_tab(self):
        """Create logs tab"""
        logs_frame = self.tabview.tab("📝 Logs")
        logs_frame.grid_columnconfigure(0, weight=1)
        logs_frame.grid_rowconfigure(0, weight=1)

        # Log display
        self.log_textbox = ctk.CTkTextbox(logs_frame)
        self.log_textbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Log controls
        log_controls = ctk.CTkFrame(logs_frame)
        log_controls.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        clear_logs_btn = ctk.CTkButton(
            log_controls, text="🗑️ Clear Logs", command=self.clear_logs, width=100
        )
        clear_logs_btn.pack(side="left", padx=5, pady=5)

        save_logs_btn = ctk.CTkButton(
            log_controls, text="💾 Save Logs", command=self.save_logs, width=100
        )
        save_logs_btn.pack(side="left", padx=5, pady=5)

    def _create_status_bar(self):
        """Create bottom status bar"""
        self.status_bar = ctk.CTkFrame(self.root, height=30)
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))

        self.status_text = ctk.CTkLabel(
            self.status_bar, text="Ready to start bot", font=ctk.CTkFont(size=12)
        )
        self.status_text.pack(side="left", padx=10, pady=5)

    def _on_config_change(self):
        """Handle configuration changes"""
        if self.bot_runner and self.running:
            # Get current configuration
            new_config = {
                "auto_heal": self.auto_heal_var.get(),
                "auto_gather": self.auto_gather_var.get(),
                "auto_combat": self.auto_combat_var.get(),
                "browser_headless": self.headless_var.get(),
            }

            # Update bot configuration
            try:
                self.bot_runner.update_config(new_config)

                # Show feedback
                changed_settings = []
                if hasattr(self, "_last_config"):
                    for key, value in new_config.items():
                        if self._last_config.get(key) != value:
                            setting_name = key.replace("_", " ").title()
                            status = "enabled" if value else "disabled"
                            changed_settings.append(f"{setting_name} {status}")

                if changed_settings:
                    message = "⚙️ " + ", ".join(changed_settings)
                    self._add_log(message)
                    logger.info(message)

                self._last_config = new_config.copy()

            except Exception as e:
                logger.error(f"Failed to update config: {e}")

    def start_bot(self):
        """Start the bot"""
        if self.running:
            return

        try:
            # Get configuration
            config = {
                "bot_name": "SimpleMMO Bot Modern GUI",
                "log_level": "INFO",
                "browser_headless": self.headless_var.get(),
                "auto_heal": self.auto_heal_var.get(),
                "auto_gather": self.auto_gather_var.get(),
                "auto_combat": self.auto_combat_var.get(),
            }

            # Store config for change detection
            self._last_config = config.copy()

            # Create bot runner
            self.bot_runner = BotRunner(config)

            # Start bot in separate thread
            self.bot_thread = threading.Thread(target=self._run_bot_async, daemon=True)
            self.bot_thread.start()

            # Update UI state
            self.running = True
            self.paused = False
            self.start_time = datetime.now()
            self._update_button_states()
            self._update_status("🟢 Running", "green")

            self._add_log("🚀 Bot started successfully!")
            logger.success("🚀 Bot started successfully!")

        except Exception as e:
            logger.error(f"❌ Failed to start bot: {e}")
            self._update_status("❌ Error", "red")
            self._add_log(f"❌ Failed to start bot: {e}")

    def pause_bot(self):
        """Pause or resume the bot"""
        if not self.running:
            return

        if self.bot_runner:
            self.paused = not self.paused
            self.bot_runner.paused = self.paused

            if self.paused:
                self.pause_btn.configure(text="▶️ Resume")
                self._update_status("⏸️ Paused", "orange")
                self._add_log("⏸️ Bot paused")
                logger.info("⏸️ Bot paused")
            else:
                self.pause_btn.configure(text="⏸️ Pause")
                self._update_status("🟢 Running", "green")
                self._add_log("▶️ Bot resumed")
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
                self.bot_thread.join(timeout=2.0)

            # Update UI state
            self.paused = False
            self._update_button_states()
            self._update_status("⏹️ Stopped", "gray")

            self._add_log("🛑 Bot stopped")
            logger.info("🛑 Bot stopped")

        except Exception as e:
            logger.error(f"❌ Error stopping bot: {e}")
            self._add_log(f"❌ Error stopping bot: {e}")

    def open_browser(self):
        """Open browser for SimpleMMO using Playwright"""
        try:
            # Try to get existing web engine first
            import asyncio

            async def launch_browser():
                # Try relative import first, then absolute
                try:
                    from ..automation.web_engine import get_web_engine
                except ImportError:
                    import sys

                    sys.path.append(str(Path(__file__).parent.parent.parent))
                    from src.automation.web_engine import get_web_engine

                engine = await get_web_engine()
                if engine:
                    page = await engine.get_page()
                    if page:
                        await page.goto("https://web.simple-mmo.com/")
                        return True
                return False

            # Run in separate thread to avoid blocking GUI
            def run_browser():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    success = loop.run_until_complete(launch_browser())
                    if success:
                        self._add_log("🌐 Playwright browser opened")
                        logger.info("🌐 Playwright browser opened")
                    else:
                        # Fallback to system browser
                        import webbrowser

                        webbrowser.open("https://web.simple-mmo.com/")
                        self._add_log("🌐 System browser opened (fallback)")
                        logger.info("🌐 System browser opened (fallback)")
                except Exception as e:
                    # Fallback to system browser
                    import webbrowser

                    webbrowser.open("https://web.simple-mmo.com/")
                    self._add_log(f"🌐 Browser opened (fallback): {e}")
                    logger.info(f"🌐 Browser opened (fallback): {e}")

            threading.Thread(target=run_browser, daemon=True).start()

        except Exception as e:
            logger.error(f"❌ Failed to open browser: {e}")
            self._add_log(f"❌ Failed to open browser: {e}")

    def clear_logs(self):
        """Clear the log display"""
        self.log_textbox.delete("1.0", "end")

    def save_logs(self):
        """Save logs to file"""
        try:
            from tkinter import filedialog

            filename = filedialog.asksaveasfilename(
                defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.log_textbox.get("1.0", "end"))
                self._add_log(f"💾 Logs saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save logs: {e}")

    def _run_bot_async(self):
        """Run bot in async context"""
        try:
            asyncio.run(self._bot_runner_loop())
        except Exception as e:
            logger.error(f"Bot runner error: {e}")
            self.running = False

    async def _bot_runner_loop(self):
        """Main bot runner loop"""
        if not await self.bot_runner.initialize():
            logger.error("Failed to initialize bot")
            return

        logger.info("Bot runner loop started")

        while self.running:
            if not self.paused:
                try:
                    await self.bot_runner.run_cycle()
                except Exception as e:
                    logger.error(f"Error in bot cycle: {e}")

            await asyncio.sleep(0.1)

    def _update_button_states(self):
        """Update button states based on bot status"""
        if self.running:
            self.start_btn.configure(state="disabled")
            self.pause_btn.configure(state="normal")
            self.stop_btn.configure(state="normal")
        else:
            self.start_btn.configure(state="normal")
            self.pause_btn.configure(state="disabled")
            self.stop_btn.configure(state="disabled")

    def _update_status(self, text: str, color: str):
        """Update status display"""
        self.status_label.configure(text=text)
        self.status_text.configure(text=text)

    def _add_log(self, message: str):
        """Add message to log display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        self.log_textbox.insert("end", log_entry)
        self.log_textbox.see("end")

    def _start_gui_updater(self):
        """Start GUI update loop"""
        self.update_running = True
        self._update_gui()

    def _update_gui(self):
        """Update GUI elements periodically"""
        if not self.update_running:
            return

        try:
            # Update uptime
            if self.running and self.start_time:
                uptime = datetime.now() - self.start_time
                uptime_str = str(uptime).split(".")[0]  # Remove microseconds
                self.uptime_label.configure(text=f"Uptime: {uptime_str}")

            # Update cycles and stats
            if self.bot_runner and self.running:
                stats = self.bot_runner.get_stats()
                self.cycles_label.configure(text=f"Cycles: {stats.get('cycles', 0)}")

                # Update detailed stats in stats tab
                self._update_stats_display(stats)

        except Exception as e:
            logger.error(f"GUI update error: {e}")

        # Schedule next update
        self.root.after(1000, self._update_gui)

    def _update_stats_display(self, stats: dict):
        """Update the statistics display"""
        try:
            # Clear existing stats
            for widget in self.stats_scroll.winfo_children():
                widget.destroy()

            # Add current stats
            for i, (key, value) in enumerate(stats.items()):
                if key in self.stats_labels:
                    continue

                # Format key name
                display_key = key.replace("_", " ").title()

                # Create stat frame
                stat_frame = ctk.CTkFrame(self.stats_scroll)
                stat_frame.grid(row=i, column=0, sticky="ew", padx=5, pady=2)

                # Stat label and value
                ctk.CTkLabel(stat_frame, text=f"{display_key}:").pack(side="left", padx=10, pady=5)
                ctk.CTkLabel(stat_frame, text=str(value), font=ctk.CTkFont(weight="bold")).pack(
                    side="right", padx=10, pady=5
                )

        except Exception as e:
            logger.error(f"Error updating stats display: {e}")

    def run(self):
        """Start the GUI"""
        logger.info("🎮 Starting Modern GUI...")
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            logger.info("GUI interrupted by user")
        finally:
            self.update_running = False
            if self.running:
                self.stop_bot()
            logger.info("🎮 GUI closed")


def main():
    """Main entry point for the modern GUI"""
    gui = ModernBotGUI()
    gui.run()


if __name__ == "__main__":
    main()
