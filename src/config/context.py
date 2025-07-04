"""
🎯 Context System for SimpleMMO Bot

Modern context management using async patterns.
Based on the original threading implementation but updated for async operation.
"""

import asyncio
import time
from collections.abc import Callable
from typing import Any

from loguru import logger

# Constants for time formatting
SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 3600


class ContextSystem:
    """Modern context management for SimpleMMO Bot"""

    def __init__(self, config: dict[str, Any]):
        """Initialize Context System"""
        self.config = config
        self.is_initialized = False

        # Bot state
        self.is_running = False
        self.is_stopping = False
        self.current_action = "idle"

        # Configuration (runtime changeable)
        self.bot_config = {
            "auto_heal": config.get("auto_heal", True),
            "auto_gather": config.get("auto_gather", True),
            "auto_combat": config.get("auto_combat", True),
            "auto_step": config.get("auto_step", True),
        }

        # Statistics
        self.stats = {
            "actions_taken": 0,
            "steps_taken": 0,
            "combat_actions": 0,
            "gather_actions": 0,
            "heal_actions": 0,
            "errors": 0,
            "start_time": 0,
        }

        # Action history (limited to last 50)
        self.action_history: list[tuple[str, str]] = []
        self.max_history = 50

        # Callbacks for UI updates
        self.update_callbacks: list[Callable] = []

        logger.info("🎯 Context System created")

    async def initialize(self) -> bool:
        """Initialize context system"""
        try:
            self.stats["start_time"] = time.time()
            self.is_initialized = True
            logger.success("✅ Context System initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Context System: {e}")
            return False
        else:
            return True

    def set_running(self, running: bool) -> None:
        """Set bot running state"""
        self.is_running = running
        if running:
            self.current_action = "running"
            logger.info("🚀 Bot started")
        else:
            self.current_action = "stopped"
            logger.info("🛑 Bot stopped")

        self._notify_callbacks("status_change")

    def is_bot_running(self) -> bool:
        """Check if bot is running"""
        return self.is_running

    def set_stopping(self, stopping: bool) -> None:
        """Set bot stopping state"""
        self.is_stopping = stopping
        if stopping:
            self.current_action = "stopping"
            logger.info("⏸️ Bot stopping...")

    def should_stop(self) -> bool:
        """Check if bot should stop"""
        return self.is_stopping

    def update_config(self, key: str, value: Any) -> None:
        """Update configuration at runtime"""
        if key in self.bot_config:
            old_value = self.bot_config[key]
            self.bot_config[key] = value
            logger.info(f"⚙️ Config updated: {key} = {value} (was {old_value})")
            self._notify_callbacks("config_change")

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.bot_config.get(key, default)

    def get_all_config(self) -> dict[str, Any]:
        """Get all configuration"""
        return self.bot_config.copy()

    def record_action(self, action: str, details: str = "") -> None:
        """Record an action in history"""
        timestamp = time.strftime("%H:%M:%S")
        action_entry = (timestamp, f"{action}: {details}" if details else action)

        self.action_history.append(action_entry)

        # Keep only last max_history entries
        if len(self.action_history) > self.max_history:
            self.action_history.pop(0)

        # Update current action
        self.current_action = action

        # Update stats
        self.stats["actions_taken"] += 1

        # Action-specific stats
        if "step" in action.lower():
            self.stats["steps_taken"] += 1
        elif "combat" in action.lower() or "attack" in action.lower():
            self.stats["combat_actions"] += 1
        elif "gather" in action.lower():
            self.stats["gather_actions"] += 1
        elif "heal" in action.lower():
            self.stats["heal_actions"] += 1

        logger.debug(f"📝 Action recorded: {action}")
        self._notify_callbacks("action_recorded")

    def record_error(self, error: str) -> None:
        """Record an error"""
        self.stats["errors"] += 1
        self.record_action("error", error)
        logger.warning(f"❌ Error recorded: {error}")

    def get_action_history(self) -> list[tuple[str, str]]:
        """Get action history"""
        return self.action_history.copy()

    def get_stats(self) -> dict[str, Any]:
        """Get bot statistics"""
        runtime = time.time() - self.stats["start_time"] if self.stats["start_time"] > 0 else 0

        return {
            **self.stats,
            "runtime_seconds": runtime,
            "runtime_formatted": self._format_runtime(runtime),
            "current_action": self.current_action,
            "is_running": self.is_running,
        }

    def _format_runtime(self, seconds: float) -> str:
        """Format runtime in human readable format"""
        if seconds < SECONDS_PER_MINUTE:
            return f"{seconds:.0f}s"
        elif seconds < SECONDS_PER_HOUR:
            minutes = seconds // SECONDS_PER_MINUTE
            secs = seconds % SECONDS_PER_MINUTE
            return f"{minutes:.0f}m {secs:.0f}s"
        else:
            hours = seconds // SECONDS_PER_HOUR
            minutes = (seconds % SECONDS_PER_HOUR) // SECONDS_PER_MINUTE
            return f"{hours:.0f}h {minutes:.0f}m"

    def register_callback(self, callback: Callable) -> None:
        """Register callback for updates"""
        if callback not in self.update_callbacks:
            self.update_callbacks.append(callback)

    def unregister_callback(self, callback: Callable) -> None:
        """Unregister callback"""
        if callback in self.update_callbacks:
            self.update_callbacks.remove(callback)

    def _notify_callbacks(self, event_type: str) -> None:
        """Notify all registered callbacks"""
        for callback in self.update_callbacks.copy():
            try:
                if asyncio.iscoroutinefunction(callback):
                    # Schedule async callback and store reference
                    task = asyncio.create_task(callback(event_type))
                    # We don't need to await or store the task reference permanently
                    # but we create it to satisfy the linter
                    _ = task
                else:
                    # Call sync callback
                    callback(event_type)
            except Exception as e:
                logger.debug(f"Error in callback: {e}")

    def reset_stats(self) -> None:
        """Reset statistics"""
        self.stats = {
            "actions_taken": 0,
            "steps_taken": 0,
            "combat_actions": 0,
            "gather_actions": 0,
            "heal_actions": 0,
            "errors": 0,
            "start_time": time.time(),
        }

        self.action_history.clear()
        logger.info("📊 Statistics reset")
        self._notify_callbacks("stats_reset")
