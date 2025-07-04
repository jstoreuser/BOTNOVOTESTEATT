"""
🔧 Configuration types for SimpleMMO Bot

Defines TypedDict for configuration objects to improve type safety.
"""

from typing import TypedDict


class BotConfig(TypedDict, total=False):
    """
    Configuration dictionary for SimpleMMO Bot

    All fields are optional (total=False) with sensible defaults.
    """
    # Bot identification
    bot_name: str
    log_level: str

    # Browser settings
    browser_headless: bool
    browser_type: str
    debugging_port: int
    user_data_dir: str
    target_url: str

    # Automation settings
    auto_heal: bool
    auto_gather: bool
    auto_combat: bool
    auto_steps: bool
    auto_captcha: bool

    # Timing settings
    step_delay_min: float
    step_delay_max: float
    combat_delay: float
    gathering_delay: float

    # URLs
    travel_url: str
