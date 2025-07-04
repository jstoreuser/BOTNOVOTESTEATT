"""
🔍 Teste de Debug Port 9222

Script simples para verificar se a porta de debugging está ativa.
"""

import socket

import requests
from loguru import logger


def test_debug_port():
    """Testa se a porta 9222 está ativa"""
    logger.info("🔍 Testing debug port 9222...")

    try:
        # Teste 1: Socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(('localhost', 9222))
        sock.close()

        if result == 0:
            logger.success("✅ Port 9222 is open!")
        else:
            logger.error("❌ Port 9222 is closed")
            return False

        # Teste 2: HTTP request to debug endpoint
        response = requests.get("http://localhost:9222/json", timeout=5)
        if response.status_code == 200:
            logger.success("✅ Debug endpoint is responding!")

            data = response.json()
            logger.info(f"📊 Found {len(data)} browser tabs/contexts")

            for i, tab in enumerate(data[:3]):  # Show first 3 tabs
                title = tab.get('title', 'No title')
                url = tab.get('url', 'No URL')
                logger.info(f"   Tab {i+1}: {title}")
                logger.info(f"         URL: {url}")

            return True
        else:
            logger.error(f"❌ Debug endpoint returned status {response.status_code}")
            return False

    except OSError:
        logger.error("❌ Cannot connect to port 9222")
        return False
    except requests.RequestException as e:
        logger.error(f"❌ HTTP request failed: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False


def main():
    """Função principal"""
    logger.info("🔍 Debug Port Tester")
    logger.info("=" * 30)

    if test_debug_port():
        logger.success("🎉 Debug port is working!")
        logger.info("💡 You can now run: python start_bot_with_debugging.py")
    else:
        logger.error("❌ Debug port is not working")
        logger.info("💡 Make sure:")
        logger.info("   • Browser was opened with manual_profile_launcher.py")
        logger.info("   • Browser window is still open")
        logger.info("   • No firewall is blocking port 9222")


if __name__ == "__main__":
    main()
