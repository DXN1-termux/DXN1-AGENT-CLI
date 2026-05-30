#!/usr/bin/env bash
# ==============================================================================
# DXN1-Agent-CLI - POSIX Shell Unified Quick Launcher (Unix/Linux/macOS/Termux)
# Created with ❤️ by DXN1
# ==============================================================================
set -euo pipefail

echo "=================================================================="
echo "🌀 DXN1 AGENT-CLI - INITIATING ENVIRONMENT HANDLER"
echo "=================================================================="

# Detect python binary
if command -v python3 &> /dev/null; then
    python3 launcher.py
elif command -v python &> /dev/null; then
    python launcher.py
else
    echo "❌ FATAL: Standard Python environment is absent on your system's PATH variables."
    echo ">> Please install Python 3.8+ to boot the user-space multi-programming client."
    exit 1
fi
