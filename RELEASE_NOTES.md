# Release Notes - v2.1

## New Features
- **🌐 Brave Browser Installation**: You can now install Brave Browser directly from the "Ottimizzazioni" tab (GUI) or the CLI.
- **Improved Build Process**: Updated configuration for creating a standalone executable.

## Enhancements
- **Automatic Dependency Management**: Added `requirements.txt` for easier setup.
- **CustomTkinter Assets**: Better handling of GUI assets in the standalone EXE.

## How to use
Run `WindowsMaster.exe` to open the GUI or `unfucker.py` for the CLI experience.
- The Brave Browser installation uses `winget` by default with a fallback to direct download if `winget` is not available.
