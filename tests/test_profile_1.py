"""
🧪 Teste do Profile 1 do Chromium

Verifica se o perfil Profile 1 existe e pode ser usado.
"""

import os
import subprocess

from loguru import logger


def test_profile_1():
    """Testa se o Profile 1 existe e funciona"""

    chromium_path = r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\chrome.exe"
    user_data_dir = r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\User Data"
    profile_1_dir = os.path.join(user_data_dir, "Profile 1")

    logger.info("🔍 Testing Profile 1 setup...")
    logger.info(f"📁 Chromium path: {chromium_path}")
    logger.info(f"📁 User Data dir: {user_data_dir}")
    logger.info(f"📁 Profile 1 dir: {profile_1_dir}")

    # Check if Chromium exists
    if not os.path.exists(chromium_path):
        logger.error("❌ Chromium not found!")
        return False
    else:
        logger.success("✅ Chromium found")

    # Check if User Data dir exists
    if not os.path.exists(user_data_dir):
        logger.error("❌ User Data directory not found!")
        return False
    else:
        logger.success("✅ User Data directory found")

    # Check if Profile 1 exists
    if not os.path.exists(profile_1_dir):
        logger.error("❌ Profile 1 not found!")
        logger.info("💡 You may need to create the profile first by:")
        logger.info("   1. Run Chromium manually")
        logger.info("   2. Go to Settings -> Add Profile")
        logger.info("   3. Name it 'Profile 1' or use existing profile")
        return False
    else:
        logger.success("✅ Profile 1 found")

        # Check profile contents
        profile_files = os.listdir(profile_1_dir)
        logger.info(f"📄 Profile has {len(profile_files)} files/folders")

        # Check for important profile files
        important_files = ["Preferences", "History", "Cookies"]
        for file in important_files:
            if file in profile_files:
                logger.success(f"✅ {file} found")
            else:
                logger.warning(f"⚠️ {file} not found")

    logger.success("🎉 Profile 1 test completed!")
    return True


def test_start_chromium():
    """Testa iniciar o Chromium com Profile 1"""

    logger.info("🚀 Testing Chromium startup with Profile 1...")

    chromium_path = r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\chrome.exe"
    user_data_dir = r"C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\User Data"

    command = [
        chromium_path,
        "--remote-debugging-port=9222",
        f"--user-data-dir={user_data_dir}",
        "--profile-directory=Profile 1",
        "--no-first-run",
        "--no-default-browser-check",
        "https://web.simple-mmo.com"
    ]

    logger.info("⚡ Starting Chromium...")
    logger.info("🌐 This should open SimpleMMO with your saved login")

    try:
        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )

        logger.success("✅ Chromium started successfully!")
        logger.info("👆 Check if a browser window opened")
        logger.info("🔑 It should automatically log you in to SimpleMMO")
        logger.info("🎯 If it works, you can close the browser and run demo_bot_completo.py")

        return True

    except Exception as e:
        logger.error(f"❌ Failed to start Chromium: {e}")
        return False


def main():
    """Executa todos os testes"""
    logger.info("🧪 Profile 1 Testing Suite")
    logger.info("=" * 50)

    # Test 1: Check if profile exists
    if not test_profile_1():
        logger.error("❌ Profile test failed!")
        return

    # Test 2: Try to start Chromium
    logger.info("\n" + "=" * 30)
    answer = input("🤔 Do you want to test starting Chromium? (y/n): ").lower().strip()

    if answer in ['y', 'yes']:
        test_start_chromium()
        logger.info("💡 Close the browser when you're done testing")
    else:
        logger.info("⏭️ Skipping Chromium startup test")

    logger.info("=" * 50)
    logger.success("✅ Testing completed!")
    logger.info("🎯 If everything looks good, run: python demo_bot_completo.py")


if __name__ == "__main__":
    main()
