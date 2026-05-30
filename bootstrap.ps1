# ==============================================================================
# DXN1-AGENT-CLI - WINDOWS POWERSHELL BOOTSTRAPPER
# Created with ❤️ BY DXN1
# ==============================================================================

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "🌀 LOADING DXN1-AGENT-CLI ON POWERSHELL (WINDOWS)" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan

# 1. Verify python execution context
$PythonBin = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonBin) {
    Write-Host "[!] Python environment not found on standard Windows execution scopes." -ForegroundColor Red
    Write-Host "[*] Prompting default python web installer..." -ForegroundColor Yellow
    Start-Process "$env:SystemRoot\System32\winget.exe" -ArgumentList "install -e --id Python.Python.3.11" -Wait
} else {
    Write-Host "[✓] Core python interpreter verified." -ForegroundColor Green
}

# 2. Virtual Env setup
$VenvName = ".nam_env"
if (-not (Test-Path $VenvName)) {
    Write-Host "[i] Initializing virtual assembly sandboxing..." -ForegroundColor Cyan
    python -m venv $VenvName
}

# Activate VirtuallEnv
& ".\$VenvName\Scripts\Activate.ps1"

# Upgrading modules
Write-Host "[i] Synchronizing runtime dependencies in assembly..." -ForegroundColor Cyan
python -m pip install --upgrade pip
pip install requests pyyaml pydantic urllib3

# 3. Onboarding Wizard
Write-Host ""
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "🔑 SECURE COGNITIVE BACKEND SELECTION" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "Choose Core Cognitive Routing Option:"
Write-Host "1) Bring Your Own Key (BYOK) - Custom security routing"
Write-Host "2) Open-Source / Offline LLMs - Custom Local Ports"

$AuthMode = Read-Host "Select Configuration [1/2] (Default is 1)"
if ([string]::IsNullOrEmpty($AuthMode)) { $AuthMode = "1" }

if ($AuthMode -eq "1") {
    Write-Host "[*] Secure BYOK Selected."
    Write-Host "Choose Provider: (1) Gemini, (2) OpenAI, (3) Anthropic"
    $Provider = Read-Host "Select Provider [1-3] (Default: 1)"
    if ([string]::IsNullOrEmpty($Provider)) { $Provider = "1" }
    
    $ApiKey = Read-Host -AsSecureString "Input secure Client API Key Token"
    
    # Convert SecureString to plain text safely inside process memory block
    $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($ApiKey)
    $PlainKey = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
    
    # Secure Persistence
    "API_PROVIDER=$Provider" | Out-File -FilePath .nam_secrets -Encoding UTF8
    "API_KEY=$PlainKey" | Out-File -FilePath .nam_secrets -Append -Encoding UTF8
    "LLM_MODE=byok" | Out-File -FilePath .nam_secrets -Append -Encoding UTF8
    Write-Host "[✓] Environmental credentials recorded." -ForegroundColor Green
} else {
    Write-Host "[*] Local Open-Source Broker model selected." -ForegroundColor Yellow
    "API_PROVIDER=local" | Out-File -FilePath .nam_secrets -Encoding UTF8
    "API_KEY=LocalSystemHost" | Out-File -FilePath .nam_secrets -Append -Encoding UTF8
    "LLM_MODE=open_source" | Out-File -FilePath .nam_secrets -Append -Encoding UTF8
    Write-Host "[✓] Configured for offline Llama integrations." -ForegroundColor Green
}

Write-Host ""
Write-Host "[SUCCESS] Windows System installation sequence resolved." -ForegroundColor Green
Write-Host "[*] Launching NAM Daemon..." -ForegroundColor Cyan
python microkernel.py
