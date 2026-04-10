# Release Notes - v2.2

## New Features
- **🌐 Brave Browser Installation**: You can now install Brave Browser directly from the "Ottimizzazioni" tab (GUI) or the CLI.
- **Improved Build Process**: Updated configuration for creating a standalone executable.

## Enhancements
- **🔄 Scrollable Optimization Tab**: The "Ottimizzazioni" tab is now scrollable, ensuring all installation buttons are visible regardless of screen resolution.
- **🤫 Silent execution**: Windows PowerShell windows no longer pop up while cleaning the system or removing bloatware.
- **Automatic Dependency Management**: Added `requirements.txt` for easier setup.
- **CustomTkinter Assets**: Better handling of GUI assets in the standalone EXE.

## How to use
Run `WindowsMaster.exe` to open the GUI or `unfucker.py` for the CLI experience.
- The Brave Browser installation uses `winget` by default with a fallback to direct download if `winget` is not available.
