"""
🚀 Quick Browser Launch - SimpleMMO Bot

Script simples para abrir o navegador rapidamente.
Ideal para interface gráfica e uso diário.
"""

import subprocess
import sys
from pathlib import Path

from loguru import logger


def quick_launch() -> bool:
    """Lança o navegador rapidamente com configuração padrão"""

    # Configuração padrão
    debug_port = 9222
    url = "https://web.simple-mmo.com/travel"

    # Configuração específica baseada no navegador encontrado
    profile_dir = r"C:\temp\BOTNOVOTESTATT"  # Padrão para Chrome/Brave/Edge

    # Caminhos possíveis dos navegadores (priorizando Chromium do Playwright)
    chrome_paths = [
        # Chromium do Playwright (PRIORIDADE - usado pelo bot)
        r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\chrome.exe",
        # Chrome padrão
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        rf"C:\Users\{Path.home().name}\AppData\Local\Google\Chrome\Application\chrome.exe",
        # Paths alternativos
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
        # Edge como fallback
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]

    # Encontrar navegador disponível e configurar perfil adequado
    browser_path = None
    profile_name = "Default"  # Valor padrão

    for path in chrome_paths:
        if Path(path).exists():
            browser_path = path

            # Configurar perfil específico para Chromium do Playwright
            if "ms-playwright" in path:
                profile_dir = (
                    r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\User Data"
                )
                profile_name = "perfilteste"  # Mesmo perfil usado pelo bot
                logger.info("🎯 Usando Chromium do Playwright (compatível com o bot)")
            else:
                profile_dir = r"C:\temp\BOTNOVOTESTATT"
                profile_name = "Default"
                logger.info(f"🌐 Usando navegador: {Path(path).stem}")
            break

    if not browser_path:
        logger.error("❌ Nenhum navegador encontrado!")
        logger.info("💡 Instale Chrome, Brave ou Edge")
        return False

    # Criar diretório do perfil
    Path(profile_dir).mkdir(parents=True, exist_ok=True)

    # Comando para abrir o navegador
    comando = [
        browser_path,
        f"--remote-debugging-port={debug_port}",
        f"--user-data-dir={profile_dir}",
        f"--profile-directory={profile_name}",
        "--window-size=1200,800",
        "--no-first-run",
        "--disable-extensions",
        url,
    ]

    try:
        logger.info("🚀 Abrindo navegador para o bot...")
        logger.info(f"📁 Perfil: {profile_dir}")
        logger.info(f"🔧 Profile: {profile_name}")
        logger.info(f"🌐 Porta: {debug_port}")

        subprocess.Popen(comando, creationflags=subprocess.CREATE_NEW_CONSOLE)

        logger.success("✅ Navegador aberto!")
        logger.info("🤖 Agora você pode executar o bot!")

        return True

    except Exception as e:
        logger.error(f"❌ Erro ao abrir navegador: {e}")
        return False


if __name__ == "__main__":
    logger.info("🌐 Abrindo navegador para SimpleMMO Bot...")

    if quick_launch():
        logger.info("🎯 Próximos passos:")
        logger.info("   1. Faça login no SimpleMMO")
        logger.info("   2. Vá para a página de viagem")
        logger.info("   3. Execute: python src/main.py")
    else:
        logger.error("❌ Falha ao abrir navegador")
        sys.exit(1)
