#!/usr/bin/env python3
"""
Simple browser starter - no interaction needed
"""

import os
import subprocess
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from loguru import logger


def start_chromium():
    """Start Chromium with persistent profile"""
    try:
        logger.info("🚀 Starting Chromium with perfilteste profile...")

        # Get username and paths
        username = os.getenv("USERNAME", "User")
        chromium_path = (
            rf"C:\Users\{username}\AppData\Local\ms-playwright\chromium-1179\chrome-win\chrome.exe"
        )
        profile_dir = (
            rf"C:\Users\{username}\AppData\Local\ms-playwright\chromium-1179\chrome-win\User Data"
        )

        # Check if Chromium exists
        if not os.path.exists(chromium_path):
            logger.error(f"❌ Chromium not found at: {chromium_path}")
            return False

        # Create profile directory
        os.makedirs(profile_dir, exist_ok=True)

        # Command to start Chromium
        command = [
            chromium_path,
            "--remote-debugging-port=9222",
            f"--user-data-dir={profile_dir}",
            "--profile-directory=perfilteste",
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--disable-extensions-except",
            "--disable-plugins-discovery",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-default-apps",
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            "--disable-backgrounding-occluded-windows",
            "https://web.simple-mmo.com/travel",
        ]

        logger.info("📍 Opening at: https://web.simple-mmo.com/travel")

        # Start process
        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )

        logger.success("✅ Chromium started!")
        logger.info("🎯 Browser should open with your saved login")
        return True

    except Exception as e:
        logger.error(f"❌ Error starting Chromium: {e}")
        return False


if __name__ == "__main__":
    if start_chromium():
        print("\n🎉 Browser started successfully!")
        print("💡 You can now run the GUI: python src/main.py")
    else:
        print("\n❌ Failed to start browser")
