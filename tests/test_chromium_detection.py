#!/usr/bin/env python3
"""
Simple test to check if Playwright Chromium is installed
"""

import os
import platform
from pathlib import Path


def find_chromium():
    """Find Playwright's Chromium executable"""
    print("🔍 Looking for Playwright Chromium...")

    system = platform.system().lower()
    if system != "windows":
        print("❌ Currently only Windows is supported")
        return None

    # Try to find Playwright's Chromium
    username = os.getenv("USERNAME", "User")
    chromium_patterns = [
        rf"C:\Users\{username}\AppData\Local\ms-playwright\chromium-*\chrome-win\chrome.exe",
        rf"C:\Users\{username}\AppData\Local\ms-playwright\chromium-1179\chrome-win\chrome.exe",
    ]

    print(f"👤 Username: {username}")

    chromium_path = None
    for pattern in chromium_patterns:
        print(f"📂 Checking pattern: {pattern}")
        # Use glob to find matching paths
        import glob

        matches = glob.glob(pattern)
        print(f"   Found {len(matches)} matches: {matches}")
        if matches:
            chromium_path = matches[0]
            break

    # Fallback: try common paths
    if not chromium_path:
        print("🔄 Trying fallback paths...")
        common_paths = [
            rf"C:\Users\{username}\AppData\Local\ms-playwright\chromium-1179\chrome-win\chrome.exe",
        ]
        for path in common_paths:
            print(f"📂 Checking: {path}")
            if Path(path).exists():
                chromium_path = path
                print(f"✅ Found at: {path}")
                break
            else:
                print(f"❌ Not found: {path}")

    if chromium_path and Path(chromium_path).exists():
        print(f"✅ Chromium found: {chromium_path}")
        return chromium_path
    else:
        print("❌ Chromium not found!")
        print("💡 Try running: python -m playwright install chromium")
        return None


if __name__ == "__main__":
    chromium = find_chromium()
    if chromium:
        print("✅ SUCCESS: Chromium is available")
    else:
        print("❌ FAILED: Chromium not found")
