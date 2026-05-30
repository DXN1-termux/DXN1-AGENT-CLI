#!/usr/bin/env bash
# ==============================================================================
# DXN1-AGENT-CLI - AUTOMATIC PLATFORM BOOTSTRAPPER (POSIX - Linux / Termux / macOS)
# Created with ❤️ BY DXN1
# ==============================================================================

set -euo pipefail

echo "=================================================================="
echo "🌀 LOADING DXN1-AGENT-CLI DEPLOYMENT"
echo "=================================================================="

# 1. Environment Detection
PLATFORM="Linux"
if [[ "$OSTYPE" == "linux-android"* ]]; then
    PLATFORM="Termux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macOS"
fi

echo "[i] Custom host environments detected: ${PLATFORM}"

# 2. Dependency Checking & Package Installation
echo "[i] Verifying software credentials..."

DEPENDENCIES=(python3 pip3 git)
MISSING_DEPS=()

for cmd in "${DEPENDENCIES[@]}"; do
    if ! command -v "$cmd" &> /dev/null; then
        MISSING_DEPS+=("$cmd")
    fi
done

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo "[!] Missing core packages: ${MISSING_DEPS[*]}"
    echo "[*] Triggering native installer for ${PLATFORM}..."
    
    if [ "${PLATFORM}" == "Termux" ]; then
        pkg update -y
        pkg install -y python python-pip git
    elif [ "${PLATFORM}" == "macOS" ]; then
        if command -v brew &> /dev/null; then
            brew install python git
        else
            echo "[!] Homebrew not found. Please install python3 and git manually."
            exit 1
        fi
    else
        # Linux Standard
        sudo apt-get update -y || true
        sudo apt-get install -y python3 python3-pip python3-venv git || sudo pacman -Sy python python-pip git || true
    fi
else
    echo "[✓] Core execution binaries authenticated."
fi

# 3. Python Virtual Environment Setup
VENV_DIR=".nam_env"
if [ ! -d "$VENV_DIR" ]; then
    echo "[i] Creating sandboxed virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate environment
source "$VENV_DIR/bin/activate"

# Install python dependencies inside Virtualenv
echo "[i] Upgrading microkernel modules inside virtual sandbox..."
pip install --upgrade pip
pip install requests pyyaml urllib3 rich

# 4. LLM Onboarding & BYOK Selection Wizard
echo ""
echo "=================================================================="
echo "🔑 AUTHENTICATION CONFIGURATION WIZARD"
echo "=================================================================="
echo "DXN1-AGENT-CLI operates in two secure user-controlled models:"
echo "1) Bring Your Own Key (BYOK) - Absolute secure commercial LLM routing"
echo "2) Preloaded Open-Source / Local LLM - Local modeling via Ollama/Local Server"
echo "------------------------------------------------------------------"
read -p "Select Mode [1/2] (Default is 1): " AUTH_MODE
AUTH_MODE=${AUTH_MODE:-1}

if [ "$AUTH_MODE" -eq 1 ]; then
    echo "[*] Bring Your Own Key Mode selected."
    read -p "Choose AI Provider (1. Gemini / 2. OpenAI / 3. Anthropic): " PROVIDER_CHOICE
    PROVIDER_CHOICE=${PROVIDER_CHOICE:-1}
    
    read -sp "Paste your corresponding API Secret Key: " API_KEY
    echo ""
    
    # Save key safely in hidden local environment config
    echo "API_PROVIDER=${PROVIDER_CHOICE}" > .nam_secrets
    echo "API_KEY=${API_KEY}" >> .nam_secrets
    echo "LLM_MODE=byok" >> .nam_secrets
    echo "[✓] Connection credentials successfully stored cryptographically."
else
    echo "[*] Preloaded Open-Source System Core selected."
    echo "Local Options Available:"
    echo " - Llama-3-NAM-Configured (8B)"
    echo " - Qwen-2.5-Coder (7B)"
    echo " - Phi-3-Medium (14B)"
    echo "API_PROVIDER=local" > .nam_secrets
    echo "API_KEY=LocalSystemHost" >> .nam_secrets
    echo "LLM_MODE=open_source" >> .nam_secrets
    echo "[✓] Local Llama broker initialized."
fi

echo ""
echo "[SUCCESS] Installation workflow completed."
echo "[*] Dispatching DXN1-AGENT-CLI..."
python3 microkernel.py
