#!/bin/bash
# ✅ Install Chrome & ChromeDriver on Render

# Create a directory for Chrome
mkdir -p /opt/render/project/chrome

# Download Chrome
curl -o /opt/render/project/chrome/chrome.zip https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Extract Chrome
dpkg -x /opt/render/project/chrome/chrome.zip /opt/render/project/chrome/

# Make Chrome executable
chmod +x /opt/render/project/chrome/chrome

# Install ChromeDriver
pip install webdriver-manager
