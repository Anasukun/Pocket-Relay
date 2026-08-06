#!/usr/bin/env bash
# PocketRelay One-Tap Installer for Linux / macOS
# Usage in terminal:
# curl -fsSL https://raw.githubusercontent.com/Anasukun/Pocket-Relay/main/install.sh | bash

set -e

echo -e "\033[0;36m==================================================\033[0m"
echo -e "\033[1;32m   📱 PocketRelay One-Tap Installer (Linux/macOS) \033[0m"
echo -e "\033[0;36m==================================================\033[0m"
echo ""

# Check for uv
if ! command -v uv &> /dev/null; then
    echo -e "\033[0;33m[1/3] 'uv' package manager not found. Installing uv...\033[0m"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
else
    echo -e "\033[0;32m[1/3] 'uv' found!\033[0m"
fi

echo -e "\033[0;33m[2/3] Installing PocketRelay globally...\033[0m"
uv tool install git+https://github.com/Anasukun/Pocket-Relay.git --force

export PATH="$HOME/.local/bin:$PATH"

echo -e "\033[0;32m[3/3] PocketRelay installed successfully! 🎉\033[0m"
echo ""
echo -e "\033[0;36mStarting PocketRelay Setup Wizard...\033[0m"
echo ""

if command -v pocketrelay &> /dev/null; then
    pocketrelay init
else
    uv run pocketrelay init
fi
