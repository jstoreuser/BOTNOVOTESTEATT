"""
🎮 Systems Module

Módulo responsável pelos sistemas de gameplay do bot.
Contém sistemas de movimento, combate, coleta, cura e anti-captcha.
"""

from .captcha import CaptchaSystem
from .combat import CombatSystem
from .gathering import GatheringSystem
from .healing import HealingSystem
from .steps import StepSystem

__all__ = [
    'CaptchaSystem',
    'CombatSystem',
    'GatheringSystem',
    'HealingSystem',
    'StepSystem'
]
