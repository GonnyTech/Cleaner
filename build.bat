@echo off
echo ========================================
echo Building Windows Master Utility EXE
echo ========================================

echo 1. Installing dependencies...
pip install -r requirements.txt

echo 2. Cleaning previous builds...
if exist build rd /s /q build
if exist dist rd /s /q dist

echo 3. Running PyInstaller...
pyinstaller --clean WindowsMaster.spec

echo ========================================
echo Build Complete! Check the 'dist' folder.
echo ========================================
pause
