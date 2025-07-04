"""
📦 SimpleMMO Bot Package Configuration

Este arquivo facilita a importação dos módulos do bot de qualquer lugar.
"""

import sys
from pathlib import Path

# Adicionar src ao path se não estiver
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Importações principais para facilitar o acesso
try:
    from automation.web_engine import WebAutomationEngine, get_web_engine
    from config.context import ContextSystem
    from systems.captcha import CaptchaSystem
    from systems.combat import CombatSystem
    from systems.gathering import GatheringSystem
    from systems.healing import HealingSystem
    from systems.steps import StepSystem

    __all__ = [
        'CaptchaSystem',
        'CombatSystem',
        'ContextSystem',
        'GatheringSystem',
        'HealingSystem',
        'StepSystem',
        'WebAutomationEngine',
        'get_web_engine'
    ]

except ImportError as e:
    print(f"Warning: Some modules could not be imported: {e}")
    __all__ = []
