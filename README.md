<p align="center">
  <img src="https://img.shields.io/badge/RELEASE-v1.4.2--STABLE-blue?style=for-the-badge&logoColor=white" alt="Release Version" />
  <img src="https://img.shields.io/badge/BUILD-PASSING-brightgreen?style=for-the-badge&logo=github&logoColor=white" alt="Build Status" />
  <img src="https://img.shields.io/badge/CLONE%20SOURCE-DXN1--termux-ff69b4?style=for-the-badge&logo=github&logoColor=white" alt="Repository Origin" />
  <img src="https://img.shields.io/badge/OS-ANDROID%20%7C%20MAC%20%7C%20LINUX%20%7C%20WIN-0c83ff?style=for-the-badge&logoColor=white" alt="Platforms Supported" />
  <img src="https://img.shields.io/badge/SANDBOX-LEVEL--3%20STRICT-red?style=for-the-badge&logoColor=white" alt="Sandbox Strictness" />
  <img src="https://img.shields.io/badge/MEMORY-%3C%2015%20MB%20RAM-purple?style=for-the-badge&logoColor=white" alt="RAM Usage" />
</p>

<p align="center"><b>MADE WITH ❤️ BY DXN1</b></p>

# 🌀 DXN1-Agent-CLI
### *Distributed, User-Space Microkernel for Multi-Platform Autonomous Agent Orchestration*

**DXN1-Agent-CLI** is an ultra-lightweight, system-native, user-space microkernel designed to orchestrate cooperative multi-agent networks without the heavyweight container overhead or host-level security compromises of traditional setups. Engineered with direct platform adaptivity, it runs as a fast background process yielding standard IPC socket paths across highly distinct developer environments: **Android (via Termux)**, **Windows (via native PowerShell Cmdlets)**, **Linux (via Bash/POSIX)**, and **macOS (via Zsh & BSD Sockets)**.

By treating autonomous agents as light, decoupled process isolates or daemon threads, DXN1-Agent-CLI limits core operational memory consumption to less than **15MB RAM**. It supports zero-overhead loopback channels, a strict file-system **Sandbox Shield**, and absolute cryptographic data sovereignty through a rigorous **Bring Your Own Key (BYOK)** gateway.

---

## 🚀 The Core Vision: Why DXN1 Made It

Most modern AI agent frameworks are over-engineered, heavy, and functionally fragile. DXN1 designed this microkernel to address fundamental architectural problems:

1. **Anti-Docker & Container Bloat**: Traditional multi-agent environments require heavy virtual machines, Docker layers, or complex hypervisors. This immediately locks out low-resource developer environments, embedded systems, and mobile environments like Android Termux. DXN1-Agent-CLI runs natively in raw user-space using standard Python virtual environments.
2. **Resource Exhaustion**: Running multiple active agent processes on standard loop frameworks routinely consumes gigabytes of memory. DXN1-Agent-CLI isolates agents into separate threads communicating via low-overhead loopback sockets, allowing highly parallel executions within 15MB of base system memory.
3. **Data Sovereignty & Privacy First**: Commercial developer tools often route context buffers through unencrypted intermediary servers or record telemetry. DXN1-Agent-CLI mandates **Bring Your Own Key (BYOK)** cryptography; API tokens stay in local device configuration memory space. If you want 100% offline security, it includes immediate support for localized offline model brokers (such as Ollama).
4. **Host Platform Incompatibility**: Writing script automation that behaves identically in Windows PowerShell background jobs, POSIX Unix daemons, and Android Termux sub-shells is notoriously difficult due to dissimilar shell semantics. DXN1-Agent-CLI solves this by providing modular, dedicated bootstrappers (`bootstrap.ps1` / `bootstrap.sh`) and unified Python core loop mechanisms.

---

## 📖 Deep Step-by-Step Hands-On Tutorial

*Welcome to the official DXN1-Agent-CLI masterclass. Follow these progressive phases to configure, deploy, run, and scale decentralized agent processes like a professional core sysop.*

### Phase 1: Dynamic Initial System Boot
To wake up your microkernel daemon, you need to clone and execute the universal launcher. Below is the multi-platform guide:

1. **Clone the official source repository** directly using your Terminal emulator:
   ```bash
   git clone https://github.com/DXN1-termux/DXN1-AGENT-CLI.git
   cd DXN1-AGENT-CLI
   ```
2. **Launch the Bootstrapper** appropriate for your current platform:
   * **macOS / Linux / Termux (Unix)**: Run `chmod +x launcher.sh && ./launcher.sh`
   * **Windows Terminal (PowerShell)**: Run `python launcher.py`
3. The launcher automatically executes dependency audits, establishes your localized `.nam_env/` virtual isolated environment sandbox, verifies your `python3` executable runtime status, and initializes the local IPC ports on Port **5001**.

### Phase 2: Authentic Key Injection (/byok)
DXN1-Agent-CLI operates under a zero-trust architecture. You must load your own secure AI reasoning keys:
1. In the console terminal, write the command `/byok` or select **"Wizard Setup"** to summon the Configuration Wizard Panel overlay.
2. Input your commercial AI developer secret keys (such as your **Gemini API Key**, **Claude credentials**, or local Ollama endpoints).
3. The microkernel registers these keys within an encrypted local coordinate file located at `.nam_secrets/keys.json`. These tokens stay strictly confined onto your native hardware.

### Phase 3: Executing Your First Autonomous Loop Agent (TUI)
Let's deploy an active, multi-staged agent reasoning process using our brand-new UI features:
1. Click bottom inside the **Quick Loop Designer** sidebar form or press the **"SHOW SUGGESTIONS"** toggle overlay.
2. Select **🔒 Security Audit**. The system will dynamically pre-fill your task query: *"Audit local microkernel.py security boundaries and sandbox shielding checks"*.
3. Click **"Execute Task Loop"** or hit Enter.
4. Watch the real-time timeline light up! The microkernel allocates immediate process resources and spins up an active **scrapper_agent (PID 1005)** and **reasoner_node (PID 1012)** to systematically execute deep checks, logging direct stream frames to your browser interface.

### Phase 4: Navigating the Slash Command Catalog
To execute rapid commands in the main CLI, type `/` to toggle our autocomplete overlay menu. Select actions by clicking:
* `/help` - Displays complete inline microkernel assistance metadata.
* `/ps` - Monitors real-time process thread telemetry logs, CPU values, and memory footprints.
* `/nodes` - Verifies dynamic socket attachments.
* `/crt` - Instantly toggles the high-contrast cathode-ray scanner overlay for nostalgia.
* `/theme matrix` - Refreshes the color palette to high-visibility phosphor terminal emerald.

---

## 🛠️ Microkernel Core Architectural Breakdown

At its heart, DXN1-Agent-CLI operates similarly to historical microkernels like Mach or QNX, but configured specifically for decentralized AI agents:

### 1. The Daemon IPC Link-Layer (microkernel.py)
The microkernel manages an internal **Process Table** maps active Agent IDs (PIDs), thread handles, socket addresses, and capability profiles. Agents do not communicate with each other directly—which would cause O(N²) connection scaling problems. Instead, all agents route structured instructions to the microkernel broker using loopback UDP/TCP socket channels on Port 5001.

### 2. The Sandbox Tool Guard (tool_executor.py)
When an agent wants to perform an action (like reading user configuration files or searching the local network), it sends a tool-execution frame. The **Sandbox Shield** checks the target directory constraints (blocking path escape attacks), validates execution policies, and guarantees your host filesystem's integrity.

### 3. Progressive JSON-RPC Message Format
Both client-to-kernel and agent-to-agent transactions rely on standard JSON-RPC 2.0 socket frames:
```json
{
  "jsonrpc": "2.0",
  "method": "ipc:broadcast",
  "params": {
    "sender_pid": 1005,
    "target_pid": 1012,
    "payload": "Querying local repository structure..."
  },
  "id": 104
}
```

---

## 📥 Comprehensive Setup & Installation Guides

Select the guide specific to your operational platform below to expand real clone & setup parameters:

<details>
  <summary><b>🍎 macOS Universal Apple Silicon & Intel Setup</b></summary>
  <br />

  ```bash
  # 1. Grab project resources using Git
  git clone https://github.com/DXN1-termux/DXN1-AGENT-CLI.git
  cd DXN1-AGENT-CLI

  # 2. Grant executable privileges to the script 
  chmod +x launcher.sh

  # 3. Enter directory and run the everyday rocket launcher script
  ./launcher.sh
  ```
  *Note: macOS setup will scan for Homebrew packages, configure native pyenv/python3 virtual sandboxes, and run standard user-space isolation rules.*
</details>

<details>
  <summary><b>🐧 Linux Native (Debian / RedHat / Arch) Setup</b></summary>
  <br />

  ```bash
  # 1. Grab files from git
  git clone https://github.com/DXN1-termux/DXN1-AGENT-CLI.git
  cd DXN1-AGENT-CLI

  # 2. Set executable script permissions
  chmod +x launcher.sh

  # 3. Double run the everyday unified script
  ./launcher.sh
  ```
  *Note: Installs pip, virtualenv, and configures localized background systemd sockets if matching capabilities exist.*
</details>

<details>
  <summary><b>🪟 Windows PowerShell Native Command Line Setup</b></summary>
  <br />

  ```powershell
  # 1. Grab project resources using Git or Curl
  git clone https://github.com/DXN1-termux/DXN1-AGENT-CLI.git
  cd DXN1-AGENT-CLI

  # 2. Unblock session executing privileges (everyday fast launch)
  Set-ExecutionPolicy Bypass -Scope Process -Force

  # 3. Launch unified Windows module orchestrator wrapper
  python launcher.py
  ```
</details>

<details>
  <summary><b>🤖 Android Termux (Mobile Developer Terminal) Setup</b></summary>
  <br />

  Ensure you utilize the standard F-Droid client distribution of Termux.
  ```bash
  # 1. Fully synchronize Termux packaging registers
  pkg update -y && pkg upgrade -y
  pkg install git python clang -y

  # 2. Pull the repository
  git clone https://github.com/DXN1-termux/DXN1-AGENT-CLI.git
  cd DXN1-AGENT-CLI

  # 3. Run the mobile-compatible launch script
  chmod +x launcher.sh
  ./launcher.sh
  ```
</details>

---

## ⚡ Unified Daily Launch Stream (launcher.sh / launcher.py)

We have unified the first-time setup onboarding and subsequent day-to-day boot processes. You do NOT need separate complicated bootstrap files anymore! 

Whether it is your **first run** or your **hundred-and-first run**, enter the cloned directory and run:
* **macOS / Linux / Termux**: `./launcher.sh`
* **Windows PowerShell**: `python launcher.py`

The script will automatically detect if a local virtual environment (`.nam_env`) exists. If missing, it completes the background onboarding and package configurations. If it is already built, it immediately and safely launches the microkernel daemon under 15MB RAM footprint!

---

## ⚙️ Interactive CLI Wizard Modes

Upon launching the bootstrapper for the very first time, the platform executes a clean onboarding sequence:
1. **Bring Your Own Key (BYOK) Mode**: Instructs the system to load your custom credentials. Rest assured that API keys are committed directly to hidden local files (dots_secrets) and are never relayed to outside monitoring networks.
2. **Local AI Model Mode**: Connects directly to localized offline endpoints (such as an Ollama instance running Llama-3, Qwen-2.5-Coder, or Phi-3) over loopback loop. This is completely free, secure, and operates without an internet connection.

---

## 📁 Persistent Task History Sidebar & Telemetry Inspections

DXN1-Agent-CLI includes a fully synchronized, state-persistent **Task History Sidebar** nested tightly into the loopback terminal layout:
- **Quick Loop Designer**: Configures and deploys multi-staged agent thread goals without typing out raw command strings manually. Includes automated safety pre-fills.
- **Cognitive Timelines Tracking**: Monitors real-time pipeline milestones (goal validation, web queries, sandbox auditing, configurations commits, outcome formulation).
- **Deep-Fidelity Diagnostics Overlay**: Clicking "Inspect" triggers a rich sub-plane modal layout showing active JSON-RPC broker streams, file mutation scores, latency rates, and outcome abstracts.
- **Microkernel Persistence**: Tasks sync natively with state layers and local storage, enabling users to re-run complex historical goals asynchronously on active peer daemon targets.

---

## 📡 Peer-to-Peer Agent Clustering Protocols

An advanced feature of DXN1-Agent-CLI is **distributed socket clustering**. An agent running on your Android Termux app can dial the microkernel TCP Broker port running on your Windows PC or Linux server:
- This allows a central, secure computer with loaded BYOK keys or a GPU-accelerated local AI node to handle reasoning tasks dispatched directly from your mobile terminal.
- Sub-nodes are configured inside the config file (`config.json`), allowing easy modifications to target addresses, model weights, and performance parameters.

---

## ❓ Frequently Asked Questions (FAQ)

### Q1: How does DXN1-Agent-CLI achieve a memory memory cap of under 15MB RAM?
Unlike heavy NodeJS or Java engines, the DXN1 microkernel is engineered in **highly optimized Python daemons** utilizing light thread handles instead of multi-process OS worker pools. External dependencies are thoroughly pruned to avoid memory bloat. Standard message routing is handled directly over raw UDP/TCP loopbacks with zero complex virtualization overhead.

### Q2: Does it require ROOT privileges on Android devices?
**No.** DXN1-Agent-CLI runs strictly inside Android's native userspace within the standard sandboxed Termux container environment, keeping your personal core system files completely untouched.

### Q3: Can I run multiple agents concurrently with different models?
**Yes.** The daemon's internal process table keeps track of individual actor configurations. You can assign different target models (e.g., Llama-3 for quick scraping, Gemini for reasoning pipeline commits) to separate PIDs simultaneously.

### Q4: Are my commercial API developer keys securely protected?
**Yes.** DXN1-Agent-CLI follows the strict **BYOK** layout. Your configurations and keys reside in standard local hidden sandboxed files (`.nam_secrets/`). Zero telemetry is reported back, keeping your context buffers 100% sovereign.

### Q5: What happens if a peer node goes offline during cooperative swarming?
The microkernel loop detected sudden link loss by ping heartbeats on Port 5001. If a node drops, the active broker automatically re-allocates scheduled tasks to healthy standby endpoints or halts non-sovereign queues safely to avoid leakage.

---

## 🔍 Deep Troubleshooting & Practical Help

### 1. Connection Errors / Port Sockets Blocked
* **Problem**: Microkernel boot fails with `OSError: [Errno 98] Address already in use`.
* **Explanation**: Another program is occupying Port `5001`.
* **Fix**: Edit `config.json` to swap `broker_port` to `5002` or `8080`, or terminate the occupying thread:
  * Linux/macOS: `lsof -i :5001` followed by `kill -9 <PID>`
  * Windows: `Get-NetTCPConnection -LocalPort 5001 | Select-Object OwningProcess` followed by `Stop-Process -Id <PID>`

### 2. Termux Virtual Environment Failures
* **Problem**: Installing wheels for packages like `cryptography` fails due to missing `rustc` compiler components.
* **Explanation**: Android system libraries differ from desktop Linux.
* **Fix**: Install required dev environments in Termux first:
  ```bash
  pkg install -y build-essential binutils rust python-cryptography
  pip install --upgrade pip
  ```

### 3. BYOK Key Injection Validation
* **Problem**: Commands return `Authentication Error: Core token payload empty`.
* **Explanation**: The key isn't loaded or isn't formatted properly in `.nam_secrets`.
* **Fix**: Open `.nam_secrets` and verify the entry coordinates. Make sure there are no trailing whitespace elements or quotes around the key:
  ```env
  KEY_COORDINATE=YourActualSecureKeyCoordinatesHere
  ```

---

<p align="center"><b>CREATED WITH ❤️ BY DXN1</b></p>
<p align="center">Fully open-source and released under the Apache 2.0 license. Let's build the decentralized future of autonomous systems together!</p>