# Changelog

All notable changes to this project will be documented in this file.

## [1.4.3] - 2026-05-30

### Fixed
- **Syntax Error in `microkernel.py`**: Resolved a `SyntaxError: unterminated string literal` on line 123. The print statement was improperly formatted with a newline before the closing quote.
- **Dependency Build Failure (Termux)**: Removed `pydantic` from `launcher.py`, `bootstrap.sh`, and `bootstrap.ps1`. 
    - *Reasoning*: `pydantic-core` required a Rust compilation step that frequently failed or timed out in Android Termux environments. 
    - *Action*: After confirming `pydantic` was not used or imported anywhere in the microkernel source code, it was removed to streamline installation and ensure compatibility with mobile/low-resource environments.
- **Launcher Permissions**: Updated `launcher.sh` to be executable by default in the repository.

### Added
- **Interactive TUI Shell**: Implemented a full command-line REPL (Read-Eval-Print Loop) within `microkernel.py`. 
    - *Commands*: `status`, `spawn`, `chat`, `tasks`, `clear`, `exit`, and `help`.
    - *Aesthetic*: Integrated ANSI color coding for a high-contrast terminal experience.
    - *Functionality*: Real-time agent orchestration and IPC telemetry monitoring directly from the console.
- **Advanced Orchestration Features**:
    - **Command History**: Integrated `readline` for persistent command history across sessions.
    - **Tool-Assisted Reasoning**: Agents now automatically trigger `ToolSandboxExecutor` for "search" and "find" queries, combining real-world data with cognitive processing.
    - **System Pulse**: New `pulse` command for monitoring host environment health and kernel resource allocation.
    - **Dashboard UI**: Redesigned the boot sequence with a professional ASCII dashboard.

### Changed
- **Git Identity**: Configured repository-local git user to `DXN1-termux` for consistent commit history.
- **Authentication Flow**: Optimized `launcher.py` dependency check to be non-blocking and silent.
- **Repository Hygiene**: Updated `.gitignore` to explicitly ignore `.nam_secrets` (BYOK keys), `__pycache__/`, and the `.nam_env/` virtual environment to prevent accidental leakage of sensitive credentials and binary bloat.
