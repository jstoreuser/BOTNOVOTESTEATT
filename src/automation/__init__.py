"""
🚀 Automation Module

Módulo responsável pela automação web usando Playwright.
Contém engines de automação, gerenciamento de browser e conexões.
"""

from .web_engine import WebAutomationEngine, get_web_engine

__all__ = ['WebAutomationEngine', 'get_web_engine']
