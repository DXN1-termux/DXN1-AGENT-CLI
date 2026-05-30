# Changelog

All notable changes to this project will be documented in this file.

## [1.4.3] - 2026-05-30

### Fixed
- **Syntax Error in `microkernel.py`**: Resolved a `SyntaxError: unterminated string literal` on line 123. The print statement was improperly formatted with a newline before the closing quote.
- **Dependency Build Failure (Termux)**: Removed `pydantic` from `launcher.py`, `bootstrap.sh`, and `bootstrap.ps1`. 
    - *Reasoning*: `pydantic-core` required a Rust compilation step that frequently failed or timed out in Android Termux environments. 
    - *Action*: After confirming `pydantic` was not used or imported anywhere in the microkernel source code, it was removed to streamline installation and ensure compatibility with mobile/low-resource environments.
- **Launcher Permissions**: Updated `launcher.sh` to be executable by default in the repository.

### Changed
- **Git Identity**: Configured repository-local git user to `DXN1-termux` for consistent commit history.
- **Authentication Flow**: Optimized `launcher.py` dependency check to be non-blocking and silent.
