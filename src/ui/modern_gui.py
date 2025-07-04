"""
🎮 Interface Gráfica Moderna para SimpleMMO Bot

Interface funcional com tkinter para controlar o bot.
Botões: Iniciar, Pausar, Abrir Navegador + logs e estatísticas.
"""

import asyncio
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path
from tkinter import *
from tkinter import messagebox, ttk
from typing import Optional

from loguru import logger

# Add src directory to Python path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(project_root))


class ModernBotGUI:
    """
    🎮 Interface Gráfica Moderna para SimpleMMO Bot

    Features:
    - Botão Iniciar/Pausar Bot
    - Botão Abrir Navegador
    - Log em tempo real
    - Estatísticas do bot
    - Interface moderna e responsiva
    """

    def __init__(self):
        """Initialize GUI"""
        self.bot_running = False
        self.bot_paused = False
        self.bot_task = None
        self.bot_runner = None
        self.stats = {
            "steps_taken": 0,
            "successful_steps": 0,
            "failed_steps": 0,
            "combat_wins": 0,
            "gathering_success": 0,
            "runtime": 0
        }
        self.start_time = None

        # Setup GUI
        self._create_gui()

    def _create_gui(self):
        """Create the main GUI window"""
        # Main window
        self.root = Tk()
        self.root.title("🤖 SimpleMMO Bot - Modern Edition")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e1e")

        # Style configuration
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TLabel", background="#1e1e1e", foreground="#ffffff")
        style.configure("TButton", padding=10)

        # Title frame
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill="x", padx=20, pady=10)

        title_label = ttk.Label(title_frame, text="🤖 SimpleMMO Bot - Modern Edition",
                               font=("Arial", 16, "bold"))
        title_label.pack(side="left")

        self.status_label = ttk.Label(title_frame, text="Status: Stopped",
                                     font=("Arial", 12), foreground="#ff6666")
        self.status_label.pack(side="right")

        # Control buttons frame
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill="x", padx=20, pady=10)

        # Start/Pause button
        self.start_pause_btn = ttk.Button(control_frame, text="🚀 Iniciar Bot",
                                         command=self.toggle_bot, width=15)
        self.start_pause_btn.pack(side="left", padx=5)

        # Open browser button
        self.browser_btn = ttk.Button(control_frame, text="🌐 Abrir Navegador",
                                     command=self.open_browser, width=15)
        self.browser_btn.pack(side="left", padx=5)

        # Force stop button
        self.stop_btn = ttk.Button(control_frame, text="🛑 Parar",
                                  command=self.force_stop_bot, width=15)
        self.stop_btn.pack(side="left", padx=5)

        # Settings frame
        settings_frame = ttk.LabelFrame(self.root, text="⚙️ Configurações", padding=10)
        settings_frame.pack(fill="x", padx=20, pady=10)

        # Settings controls
        settings_controls = ttk.Frame(settings_frame)
        settings_controls.pack(fill="x")

        ttk.Label(settings_controls, text="Max Cycles:").grid(row=0, column=0, sticky="w", padx=5)
        self.max_cycles_var = StringVar(value="50")
        ttk.Entry(settings_controls, textvariable=self.max_cycles_var, width=10).grid(row=0, column=1, padx=5)

        ttk.Label(settings_controls, text="Delay (s):").grid(row=0, column=2, sticky="w", padx=5)
        self.delay_var = StringVar(value="2.0")
        ttk.Entry(settings_controls, textvariable=self.delay_var, width=10).grid(row=0, column=3, padx=5)

        # Mode selection
        ttk.Label(settings_controls, text="Modo:").grid(row=1, column=0, sticky="w", padx=5)
        self.mode_var = StringVar(value="Completo")
        mode_combo = ttk.Combobox(settings_controls, textvariable=self.mode_var,
                                 values=["Completo", "Apenas Steps", "Apenas Combat", "Apenas Gathering"],
                                 width=15, state="readonly")
        mode_combo.grid(row=1, column=1, columnspan=2, padx=5, sticky="w")

        # Statistics frame
        stats_frame = ttk.LabelFrame(self.root, text="📊 Estatísticas", padding=10)
        stats_frame.pack(fill="x", padx=20, pady=10)

        # Stats grid
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill="x")

        # First row
        ttk.Label(stats_grid, text="Steps:").grid(row=0, column=0, sticky="w", padx=5)
        self.steps_label = ttk.Label(stats_grid, text="0", foreground="#66ff66")
        self.steps_label.grid(row=0, column=1, sticky="w", padx=5)

        ttk.Label(stats_grid, text="Sucessos:").grid(row=0, column=2, sticky="w", padx=5)
        self.success_label = ttk.Label(stats_grid, text="0", foreground="#66ff66")
        self.success_label.grid(row=0, column=3, sticky="w", padx=5)

        ttk.Label(stats_grid, text="Falhas:").grid(row=0, column=4, sticky="w", padx=5)
        self.failed_label = ttk.Label(stats_grid, text="0", foreground="#ff6666")
        self.failed_label.grid(row=0, column=5, sticky="w", padx=5)

        # Second row
        ttk.Label(stats_grid, text="Combates:").grid(row=1, column=0, sticky="w", padx=5)
        self.combat_label = ttk.Label(stats_grid, text="0", foreground="#66ff66")
        self.combat_label.grid(row=1, column=1, sticky="w", padx=5)

        ttk.Label(stats_grid, text="Gathering:").grid(row=1, column=2, sticky="w", padx=5)
        self.gathering_label = ttk.Label(stats_grid, text="0", foreground="#66ff66")
        self.gathering_label.grid(row=1, column=3, sticky="w", padx=5)

        ttk.Label(stats_grid, text="Runtime:").grid(row=1, column=4, sticky="w", padx=5)
        self.runtime_label = ttk.Label(stats_grid, text="00:00:00", foreground="#66ddff")
        self.runtime_label.grid(row=1, column=5, sticky="w", padx=5)

        # Log frame
        log_frame = ttk.LabelFrame(self.root, text="📝 Log do Bot", padding=10)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Log text area with scrollbar
        log_container = ttk.Frame(log_frame)
        log_container.pack(fill="both", expand=True)

        self.log_text = Text(log_container, height=15, bg="#2d2d2d", fg="#ffffff",
                            font=("Consolas", 9), wrap="word")
        scrollbar = ttk.Scrollbar(log_container, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Clear log button
        clear_btn = ttk.Button(log_frame, text="🗑️ Limpar Log", command=self.clear_log)
        clear_btn.pack(pady=5)

        # Start update timer
        self.update_runtime()

        # Initial log
        self.log_message("🎮 Interface gráfica iniciada", "INFO")
        self.log_message("⚙️ Configure as opções e clique em 'Iniciar Bot'", "INFO")

    def log_message(self, message: str, level: str = "INFO"):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")

        # Color coding based on level
        colors = {
            "INFO": "#ffffff",
            "SUCCESS": "#66ff66",
            "WARNING": "#ffff66",
            "ERROR": "#ff6666",
            "DEBUG": "#66ddff"
        }

        color = colors.get(level, "#ffffff")
        formatted_message = f"[{timestamp}] {message}\n"

        # Add to text widget
        self.log_text.insert("end", formatted_message)
        self.log_text.see("end")  # Auto-scroll

        # Limit log size
        lines = self.log_text.get("1.0", "end").count('\n')
        if lines > 100:
            self.log_text.delete("1.0", "10.0")

        # Also log to logger
        logger.info(message)

    def clear_log(self):
        """Clear the log text area"""
        self.log_text.delete("1.0", "end")
        self.log_message("🗑️ Log limpo", "INFO")

    def update_stats(self):
        """Update statistics display"""
        self.steps_label.config(text=str(self.stats["steps_taken"]))
        self.success_label.config(text=str(self.stats["successful_steps"]))
        self.failed_label.config(text=str(self.stats["failed_steps"]))
        self.combat_label.config(text=str(self.stats["combat_wins"]))
        self.gathering_label.config(text=str(self.stats["gathering_success"]))

    def update_runtime(self):
        """Update runtime display"""
        if self.bot_running and self.start_time:
            elapsed = time.time() - self.start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            runtime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.runtime_label.config(text=runtime_str)

        # Schedule next update
        self.root.after(1000, self.update_runtime)

    def toggle_bot(self):
        """Toggle bot start/pause/resume"""
        if not self.bot_running:
            self.start_bot()
        elif self.bot_paused:
            self.resume_bot()
        else:
            self.pause_bot()

    def start_bot(self):
        """Start the bot"""
        try:
            self.log_message("🚀 Iniciando bot...", "INFO")

            # Get settings
            max_cycles = int(self.max_cycles_var.get())
            delay = float(self.delay_var.get())
            mode = self.mode_var.get()

            # Update UI
            self.bot_running = True
            self.bot_paused = False
            self.start_time = time.time()
            self.start_pause_btn.config(text="⏸️ Pausar Bot")
            self.status_label.config(text="Status: Rodando", foreground="#66ff66")

            # Create bot config
            config = {
                "bot_name": "SimpleMMO Bot Modern",
                "log_level": "INFO",
                "browser_headless": False,
                "auto_heal": True,
                "auto_gather": mode in ["Completo", "Apenas Gathering"],
                "auto_combat": mode in ["Completo", "Apenas Combat"],
                "step_system_enabled": mode in ["Completo", "Apenas Steps"],
                "max_cycles": max_cycles,
                "cycle_delay": delay
            }

            # Start bot in separate thread
            self.bot_task = threading.Thread(target=self._run_bot_thread, args=(config,), daemon=True)
            self.bot_task.start()

            self.log_message(f"✅ Bot iniciado - Modo: {mode}, Max Cycles: {max_cycles}", "SUCCESS")

        except ValueError as e:
            self.log_message(f"❌ Erro nas configurações: {e}", "ERROR")
            messagebox.showerror("Erro", f"Configurações inválidas: {e}")
        except Exception as e:
            self.log_message(f"❌ Erro ao iniciar bot: {e}", "ERROR")
            messagebox.showerror("Erro", f"Falha ao iniciar bot: {e}")

    def pause_bot(self):
        """Pause the bot"""
        self.bot_paused = True
        self.start_pause_btn.config(text="▶️ Retomar Bot")
        self.status_label.config(text="Status: Pausado", foreground="#ffff66")
        self.log_message("⏸️ Bot pausado", "WARNING")

    def resume_bot(self):
        """Resume the bot"""
        self.bot_paused = False
        self.start_pause_btn.config(text="⏸️ Pausar Bot")
        self.status_label.config(text="Status: Rodando", foreground="#66ff66")
        self.log_message("▶️ Bot retomado", "SUCCESS")

    def force_stop_bot(self):
        """Force stop the bot"""
        if self.bot_running:
            self.bot_running = False
            self.bot_paused = False
            self.start_pause_btn.config(text="🚀 Iniciar Bot")
            self.status_label.config(text="Status: Parado", foreground="#ff6666")
            self.log_message("🛑 Bot parado forçadamente", "WARNING")
        else:
            self.log_message("ℹ️ Bot já está parado", "INFO")

    def open_browser(self):
        """Open browser to SimpleMMO"""
        try:
            # Try to open the game URL
            url = "https://simplemmo.me/travel"
            webbrowser.open(url)
            self.log_message("🌐 Navegador aberto para SimpleMMO", "SUCCESS")
        except Exception as e:
            self.log_message(f"❌ Erro ao abrir navegador: {e}", "ERROR")

        # Also try to run browser launcher if it exists
        try:
            browser_launcher = Path(__file__).parent.parent.parent / "browser_launcher.py"
            if browser_launcher.exists():
                subprocess.Popen([sys.executable, str(browser_launcher)],
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
                self.log_message("🚀 Launcher do navegador executado", "SUCCESS")
        except Exception as e:
            self.log_message(f"⚠️ Launcher não disponível: {e}", "DEBUG")

    def _run_bot_thread(self, config):
        """Run bot in separate thread"""
        try:
            # Import and run bot
            from bot_runner import run_bot

            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Run bot with GUI integration
            loop.run_until_complete(self._run_bot_with_gui(config))

        except Exception as e:
            self.log_message(f"💥 Erro fatal no bot: {e}", "ERROR")
            logger.exception("Full bot error traceback:")
        finally:
            # Update UI when bot stops
            self.root.after(0, self._bot_stopped_callback)

    async def _run_bot_with_gui(self, config):
        """Run bot with GUI integration"""
        try:
            from bot_runner import BotRunner

            # Create bot runner
            self.bot_runner = BotRunner(config)

            # Initialize bot
            self.log_message("🔧 Inicializando sistemas do bot...", "INFO")
            await self.bot_runner.initialize()

            # Main bot loop with GUI integration
            cycle = 0
            max_cycles = config.get("max_cycles", 50)

            while self.bot_running and cycle < max_cycles:
                # Check if paused
                while self.bot_paused and self.bot_running:
                    await asyncio.sleep(1)

                if not self.bot_running:
                    break

                cycle += 1
                self.log_message(f"🔄 Ciclo {cycle}/{max_cycles}", "INFO")

                # Run bot cycle
                try:
                    result = await self.bot_runner.run_cycle()

                    # Update stats based on result
                    if result:
                        if "step" in result:
                            self.stats["steps_taken"] += 1
                            if result["step"]:
                                self.stats["successful_steps"] += 1
                            else:
                                self.stats["failed_steps"] += 1

                        if "combat" in result and result["combat"]:
                            self.stats["combat_wins"] += 1

                        if "gathering" in result and result["gathering"]:
                            self.stats["gathering_success"] += 1

                    # Update GUI stats
                    self.root.after(0, self.update_stats)

                except Exception as e:
                    self.log_message(f"❌ Erro no ciclo {cycle}: {e}", "ERROR")
                    await asyncio.sleep(5)

                # Wait between cycles
                await asyncio.sleep(config.get("cycle_delay", 2.0))

            self.log_message(f"🏁 Bot finalizado após {cycle} ciclos", "SUCCESS")

        except Exception as e:
            self.log_message(f"💥 Erro crítico: {e}", "ERROR")
            raise

    def _bot_stopped_callback(self):
        """Callback when bot stops"""
        self.bot_running = False
        self.bot_paused = False
        self.start_pause_btn.config(text="🚀 Iniciar Bot")
        self.status_label.config(text="Status: Parado", foreground="#ff6666")

    def run(self):
        """Run the GUI"""
        try:
            self.root.mainloop()
        except Exception as e:
            logger.error(f"Error running GUI: {e}")
        finally:
            # Cleanup
            if self.bot_running:
                self.bot_running = False


def main():
    """Main entry point for GUI"""
    try:
        logger.info("🎮 Starting Modern Bot GUI")

        # Create and run GUI
        gui = ModernBotGUI()
        gui.run()

    except Exception as e:
        logger.error(f"💥 Fatal error in GUI: {e}")
        messagebox.showerror("Erro Fatal", f"Erro na interface: {e}")


if __name__ == "__main__":
    main()
