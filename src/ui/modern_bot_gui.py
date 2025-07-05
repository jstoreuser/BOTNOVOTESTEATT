"""
🎮 Modern SimpleMMO Bot GUI - CustomTkinter Interface

Ultra-modern GUI using CustomTkinter with:
- Beautiful dark/light themes
- Real-time statistics
- Live configuration updates
- Professional design
"""

import asyncio
import sys
import threading
from datetime import datetime
from pathlib import Path

import customtkinter as ctk
from loguru import logger

# Import bot components
try:
    from ..config.types import BotConfig
    from ..core.bot_runner import BotRunner
except ImportError:
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent))
    from src.config.types import BotConfig
    from src.core.bot_runner import BotRunner

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

        # GUI state flags
        self.update_running = False
        self.shutdown_requested = False
        self.widgets_destroyed = False

        # Setup close protocol for graceful shutdown
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create GUI
        self._create_widgets()
        self._start_gui_updater()

        logger.info("🎮 Modern GUI initialized")

    def _safe_widget_update(self, widget_update_func):
        """Safely update a widget, catching TclError if widget is destroyed"""
        if self.widgets_destroyed or self.shutdown_requested:
            return

        try:
            widget_update_func()
        except Exception as e:
            # Log but don't propagate widget update errors during shutdown
            if not self.shutdown_requested:
                logger.debug(f"Widget update error: {e}")

    def _widget_exists(self, widget) -> bool:
        """Check if a widget still exists and hasn't been destroyed"""
        if self.widgets_destroyed or self.shutdown_requested:
            return False

        try:
            # Try to access a property of the widget
            _ = widget.winfo_exists()
            return True
        except Exception:
            return False

    def on_closing(self):
        """Handle window close event gracefully"""
        logger.info("🔒 GUI close requested")
        self.shutdown_requested = True

        # Stop GUI updates
        self.update_running = False

        # Stop bot if running
        if self.running:
            try:
                self.stop_bot()
            except Exception as e:
                logger.debug(f"Error stopping bot during close: {e}")

        # Mark widgets as destroyed before actually destroying
        self.widgets_destroyed = True

        # Close the window
        try:
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            logger.debug(f"Error destroying GUI: {e}")

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

        self.auto_quest_var = ctk.BooleanVar(value=False)  # Disabled by default
        self.auto_quest_switch = ctk.CTkSwitch(
            config_frame,
            text="Auto Quests",
            variable=self.auto_quest_var,
            command=self._on_config_change,
        )
        self.auto_quest_switch.grid(row=4, column=0, sticky="w", padx=20, pady=5)

        self.headless_var = ctk.BooleanVar(value=False)
        self.headless_switch = ctk.CTkSwitch(
            config_frame,
            text="Headless Browser",
            variable=self.headless_var,
            command=self._on_config_change,
        )
        self.headless_switch.grid(row=5, column=0, sticky="w", padx=20, pady=5)

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
        """Start the bot with proper cleanup of previous instance"""
        if self.running:
            return

        try:
            # Ensure complete cleanup of previous bot instance
            if hasattr(self, "bot_thread") and self.bot_thread and self.bot_thread.is_alive():
                logger.info("🔄 Waiting for previous bot thread to finish...")
                self.bot_thread.join(timeout=5.0)  # Wait up to 5 seconds
                if self.bot_thread.is_alive():
                    logger.warning("⚠️ Previous bot thread still running - forcing new instance")            # CRITICAL: Force complete reset of web engine before creating new bot
            logger.info("🔄 Force resetting web engine for fresh start...")
            try:
                import asyncio

                # Create new event loop for this thread
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                # Import and force reset global web engine
                try:
                    from src.automation.web_engine import WebEngineManager
                except ImportError:
                    from automation.web_engine import WebEngineManager

                # Force complete reset of singleton instance
                loop.run_until_complete(WebEngineManager.force_reset())
                logger.success("✅ Web engine force reset complete")

            except Exception as e:
                logger.warning(f"⚠️ Could not force reset web engine: {e}")

            # If there's an existing bot_runner, ensure it's reset
            if self.bot_runner:
                logger.info("🔄 Resetting previous bot runner state...")
                try:
                    # Run reset and wait for completion
                    loop.run_until_complete(self.bot_runner.reset_state())
                    logger.success("✅ Previous bot state reset completed")

                except Exception as e:
                    logger.error(f"❌ Error resetting previous bot state: {e}")

            # Reset all state variables
            self.running = False
            self.paused = False
            self.bot_runner = None
            self.bot_thread = None

            # Small delay to ensure cleanup is complete
            import time

            time.sleep(1.0)  # Increased delay to ensure complete cleanup

            # Get configuration
            config: BotConfig = {
                "auto_heal": self.auto_heal_var.get(),
                "auto_gather": self.auto_gather_var.get(),
                "auto_combat": self.auto_combat_var.get(),
                "auto_quests": self.auto_quest_var.get(),
                "auto_steps": True,  # Always enable steps
                "auto_captcha": True,  # Always enable captcha handling
                "quests_enabled": self.auto_quest_var.get(),
                "max_quests_per_cycle": 3,  # Default value
                "browser_headless": self.headless_var.get(),
                "target_url": "https://web.simple-mmo.com/travel",
            }

            # Store config for change detection
            self._last_config = config.copy()

            # Create fresh bot runner instance
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
            # Reset state on error
            self.running = False
            self.bot_runner = None
            self.bot_thread = None

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
        """Stop the bot and reset all systems to initial state"""
        if not self.running:
            return

        try:
            # Set running to False first
            self.running = False

            # Stop the bot runner
            if self.bot_runner:
                self.bot_runner.running = False

            # Wait for thread to finish (with timeout)
            if self.bot_thread and self.bot_thread.is_alive():
                logger.info("🔄 Waiting for bot thread to finish...")
                self.bot_thread.join(timeout=5.0)
                if self.bot_thread.is_alive():
                    logger.warning("⚠️ Bot thread still running after timeout")

            # Clear bot references immediately to prevent further operations
            self.bot_runner = None
            self.bot_thread = None
            self.paused = False

            # Update UI state only if widgets still exist
            self._update_button_states()
            self._update_status("⏹️ Stopped", "gray")
            self._add_log("🛑 Bot stopped - ready for fresh start")

            logger.info("🛑 Bot stopped successfully")

        except Exception as e:
            logger.error(f"❌ Error stopping bot: {e}")
            # Try to add log, but don't fail if UI is destroyed
            if not self.shutdown_requested:
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
                        # Always navigate to travel page instead of home page
                        await page.goto("https://web.simple-mmo.com/travel")
                        await page.wait_for_load_state("networkidle")
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

                        webbrowser.open("https://web.simple-mmo.com/travel")
                        self._add_log("🌐 System browser opened (fallback)")
                        logger.info("🌐 System browser opened (fallback)")
                except Exception as e:
                    # Fallback to system browser
                    import webbrowser

                    webbrowser.open("https://web.simple-mmo.com/travel")
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
        try:
            success = await self.bot_runner.initialize()
            if not success:
                logger.error("Failed to initialize bot - initialize returned False")
                return
        except Exception as e:
            logger.error(f"Failed to initialize bot - exception: {e}")
            logger.exception("Full traceback:")
            return

        logger.info("Bot runner loop started")

        while self.running:
            if not self.paused:
                try:
                    results = await self.bot_runner.run_cycle()

                    # Check if context was destroyed (navigation crash)
                    if results.get("context_destroyed"):
                        logger.error("🚨 Bot detected page navigation crash!")
                        self._handle_bot_crash("Page navigation detected - context destroyed")
                        break

                except Exception as e:
                    error_msg = str(e).lower()
                    if "execution context was destroyed" in error_msg:
                        logger.error("🚨 Bot crashed due to page navigation!")
                        self._handle_bot_crash("Execution context destroyed")
                        break
                    else:
                        logger.error(f"Error in bot cycle: {e}")

            await asyncio.sleep(0.1)

    def _update_button_states(self):
        """Update button states based on bot status"""
        if not self._widget_exists(self.start_btn):
            return

        def update_buttons():
            if self.running:
                self.start_btn.configure(state="disabled")
                self.pause_btn.configure(state="normal")
                self.stop_btn.configure(state="normal")
            else:
                self.start_btn.configure(state="normal")
                self.pause_btn.configure(state="disabled")
                self.stop_btn.configure(state="disabled")

        self._safe_widget_update(update_buttons)

    def _update_status(self, text: str, color: str):
        """Update status display"""
        if not self._widget_exists(self.status_label):
            return

        def update_status():
            self.status_label.configure(text=text)
            self.status_text.configure(text=text)

        self._safe_widget_update(update_status)

    def _add_log(self, message: str):
        """Add message to log display"""
        if not self._widget_exists(self.log_textbox):
            return

        def add_log():
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"
            self.log_textbox.insert("end", log_entry)
            self.log_textbox.see("end")

        self._safe_widget_update(add_log)

    def _start_gui_updater(self):
        """Start GUI update loop"""
        self.update_running = True
        self._update_gui()

    def _update_gui(self):
        """Update GUI elements periodically"""
        if not self.update_running or self.shutdown_requested:
            return

        try:
            # Update uptime
            if self.running and self.start_time and self._widget_exists(self.uptime_label):
                uptime = datetime.now() - self.start_time
                uptime_str = str(uptime).split(".")[0]  # Remove microseconds

                def update_uptime():
                    self.uptime_label.configure(text=f"Uptime: {uptime_str}")

                self._safe_widget_update(update_uptime)

            # Update cycles and stats
            if self.bot_runner and self.running and self._widget_exists(self.cycles_label):
                stats = self.bot_runner.get_stats()

                def update_cycles():
                    self.cycles_label.configure(text=f"Cycles: {stats.get('cycles', 0)}")

                self._safe_widget_update(update_cycles)

                # Update detailed stats in stats tab
                self._update_stats_display(stats)

        except Exception as e:
            if not self.shutdown_requested:
                logger.error(f"GUI update error: {e}")

        # Schedule next update only if not shutting down
        if not self.shutdown_requested and self.update_running:
            try:
                self.root.after(1000, self._update_gui)
            except Exception:
                # Ignore scheduling errors during shutdown
                pass

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
        except Exception as e:
            logger.error(f"GUI error: {e}")
        finally:
            # Clean shutdown
            logger.info("🧹 Starting GUI cleanup...")
            self.update_running = False
            if self.running:
                try:
                    self.stop_bot()
                except Exception as e:
                    logger.debug(f"Error during bot stop: {e}")

            # Give time for any pending operations
            import time

            time.sleep(0.5)

            logger.info("🎮 GUI closed")

    def _handle_bot_crash(self, reason: str):
        """Handle bot crash by stopping it and updating UI"""
        logger.error(f"🚨 Bot crashed: {reason}")

        try:
            # Stop the bot immediately
            self.running = False
            if self.bot_runner:
                self.bot_runner.running = False

            # Clear references to crashed bot
            self.bot_runner = None
            self.bot_thread = None
            self.paused = False

            # Update UI to reflect crash and require manual restart
            self._update_button_states()
            self._update_status("🚨 Crashed - Manual Restart Required", "red")
            self._add_log(f"🚨 Bot crashed: {reason}")
            self._add_log("🛑 Bot stopped automatically due to page navigation")
            self._add_log("📝 Please check the browser page and restart when ready")

        except Exception as e:
            logger.error(f"Error handling bot crash: {e}")


def main():
    """Main entry point for the modern GUI"""
    gui = ModernBotGUI()
    gui.run()


if __name__ == "__main__":
    main()
