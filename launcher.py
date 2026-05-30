#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DXN1-Agent-CLI - Unified Platform Launcher & Diagnostic Tool
Designed to combine first-time onboarding setup and everyday run commands.
Created with ❤️ by DXN1.
"""
import os
import sys
import subprocess
import shutil

def main():
    print("==================================================================")
    print("🌀 DXN1 AGENT MICROKERNEL - UNIFIED ENTERPRISE LAUNCHER")
    print("==================================================================")

    # 1. Active virtualenv verification
    venv_dir = ".nam_env"
    is_windows = sys.platform.startswith("win")
    
    # Check if virtualenv is setup
    if not os.path.isdir(venv_dir):
        print("[!] Virtual isolation context not discovered. Executing first-time setup...")
        try:
            # Spawn virtual env
            subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
            print("[✓] Virtual sandbox environment created successfully.")
        except Exception as e:
            print(f"[❌] Fatal error creating sandbox namespace: {e}")
            sys.exit(1)
            
    # Resolve pip dependency binaries within sandbox
    pip_path = os.path.join(venv_dir, "Scripts", "pip") if is_windows else os.path.join(venv_dir, "bin", "pip")
    py_path = os.path.join(venv_dir, "Scripts", "python") if is_windows else os.path.join(venv_dir, "bin", "python")
    
    if not os.path.exists(pip_path) and not os.path.exists(pip_path + ".exe"):
        # Pip fallback checking
        pip_path = "pip"
        py_path = "python"

    # Install/upgrade dependencies silently
    print("[i] Validating active package alignments...")
    try:
        subprocess.check_call([py_path, "-m", "pip", "install", "--upgrade", "pip"], stdout=subprocess.DEVNULL)
        subprocess.check_call([py_path, "-m", "pip", "install", "requests", "pyyaml", "urllib3", "rich"], stdout=subprocess.DEVNULL)
        print("[✓] Sandboxed third-party libraries synchronised.")
    except Exception as e:
        print(f"[i] Non-blocking dependency synchronization remark: {e}")

    # 2. Check for .nam_secrets
    force_config = "--config" in sys.argv
    if not os.path.exists(".nam_secrets") or force_config:
        print("\n[!] Initializing secure BYOK cryptokey configuration stream...")
        print("------------------------------------------------------------------")
        print("Cognitive Routing Setup:")
        print("1) Bring Your Own Key (BYOK) Mode")
        print("2) Offline Local Modeling Node (Ollama proxy)")
        choice = input("Select Mode [1/2] (Default is 1): ").strip() or "1"
        
        if choice == "1":
            print("\nSelect AI Reasoning Provider:")
            print("1) Gemini (Google)")
            print("2) OpenAI (GPT-4o-mini)")
            print("3) Anthropic (Claude-3)")
            p_choice = input("Select [1/2/3] (Default: 1): ").strip() or "1"
            
            providers = {"1": "gemini", "2": "openai", "3": "anthropic"}
            provider = providers.get(p_choice, "gemini")
            
            import getpass
            key = getpass.getpass(f"Paste your secure {provider.upper()} API token: ")
            
            with open(".nam_secrets", "w") as f:
                f.write(f"API_PROVIDER={provider}\nAPI_KEY={key}\nLLM_MODE=byok\n")
            print(f"[✓] {provider.upper()} credentials persistently mapped.")
        else:
            with open(".nam_secrets", "w") as f:
                f.write("API_PROVIDER=local\nAPI_KEY=LocalSystemHost\nLLM_MODE=open_source\n")
            print("[✓] Configured local Offline model proxy.")

    # 3. Boot Core Daemon
    print("\n[SUCCESS] Unified checks passed. Forwarding run sequence directly to Daemon loop...")
    kernel_script = "microkernel.py"
    if os.path.exists(kernel_script):
        subprocess.call([py_path, kernel_script])
    else:
        print("[❌] Critical system error: microkernel.py core script not discovered!")
        sys.exit(1)

if __name__ == "__main__":
    main()
