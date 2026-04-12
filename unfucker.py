import subprocess
import winreg
import os
from elevate import elevate
from utils import get_config, save_config, get_text
from translations import TRANSLATIONS

class WindowsCleaner:
    def __init__(self):
        self.config = get_config()
        self.lang = self.config.get("language", "en")
        self.apps = {
            "Microsoft ToDo": "Microsoft.ToDo",
            "Mail and Calendar": "Microsoft.WindowsCommunicationsApps",
            "Camera": "Microsoft.WindowsCamera",
            "People": "Microsoft.People",
            "Notepad": "Microsoft.WindowsNotepad",
            "Microsoft Edge": "Microsoft.Edge",
            "Sticky Notes": "Microsoft.MicrosoftStickyNotes",
            "Get Started": "Microsoft.Getstarted",
            "3D Builder": "Microsoft.3DBuilder",
            "Paint 3D": "Microsoft.MSPaint",
            "Paint": "Microsoft.Windows.Paint",
            "Clipchamp": "Clipchamp.Clipchamp",
            "DevHome": "Microsoft.DevHome",
            "Outlook": "Microsoft.Office.Outlook",
            "Mail": "Microsoft.WindowsCommunicationsApps",
            "Sticky Notes (Windows 11)": "Microsoft.StickyNotes",
            "Microsoft Copilot": "Microsoft.Windows.Copilot",
            "Microsoft Recall": "Microsoft.Recall"
        }

    def run_powershell_command(self, command):
        try:
            subprocess.run(["powershell", "-Command", command], check=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            return True
        except subprocess.CalledProcessError:
            return False

    def remove_bloatware(self, selected_apps):
        total = len(selected_apps)
        for i, (app_name, app_code) in enumerate(selected_apps.items(), 1):
            print(f"[{i}/{total}] {get_text('log_removing', self.lang)} {app_name}...")
            command = f"Get-AppxPackage *{app_code}* | Remove-AppxPackage"
            if self.run_powershell_command(command):
                print(f"✓ {app_name} {get_text('log_removed_success', self.lang)}")
            else:
                print(f"✗ {get_text('log_removed_error', self.lang)} {app_name}")

    def disable_ads(self):
        print(f"\n{get_text('log_disable_ads', self.lang)}")
        try:
            paths = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                r"SOFTWARE\Policies\Microsoft\Windows\CloudContent"
            ]
            for path in paths:
                key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_ALL_ACCESS)
                winreg.SetValueEx(key, "DisableWindowsConsumerFeatures", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
            print(f"✓ {get_text('log_ads_success', self.lang)}")
        except Exception as e:
            print(f"✗ {get_text('log_ads_error', self.lang)}: {str(e)}")

    def install_vscode(self):
        print(f"\n{get_text('log_vscode_install', self.lang)}")
        try:
            download_command = "Invoke-WebRequest -Uri 'https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user' -OutFile 'VSCodeSetup.exe'"
            if self.run_powershell_command(download_command):
                install_command = "./VSCodeSetup.exe /VERYSILENT /NORESTART /MERGETASKS=!runcode"
                if self.run_powershell_command(install_command):
                    print(f"✓ {get_text('log_vscode_success', self.lang)}")
                    os.remove("VSCodeSetup.exe")
                    return True
            print(f"✗ {get_text('log_vscode_error', self.lang)}")
            return False
        except Exception as e:
            print(f"✗ {get_text('log_vscode_error', self.lang)}: {str(e)}")
            return False

    def install_brave(self):
        print(f"\n{get_text('log_brave_download', self.lang)}")
        try:
            # Using winget for Brave as it's more reliable for Chromium-based browsers
            print(f"{get_text('log_brave_winget', self.lang)}")
            install_cmd = "winget install Brave.Brave --silent --accept-package-agreements --accept-source-agreements"
            result = subprocess.run(["powershell", "-Command", install_cmd], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            if result.returncode == 0:
                print(f"✓ {get_text('log_brave_success', self.lang)}")
                return True
            else:
                # Fallback to direct download if winget fails
                print(f"{get_text('log_brave_fallback', self.lang)}")
                download_cmd = "Invoke-WebRequest -Uri 'https://laptop-updates.brave.com/latest/winx64' -OutFile 'BraveSetup.exe'"
                if self.run_powershell_command(download_cmd):
                    print(f"{get_text('log_brave_download', self.lang)}")
                    subprocess.run(["./BraveSetup.exe", "/silent", "/install"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    os.remove("BraveSetup.exe")
                    print(f"✓ {get_text('log_brave_success', self.lang)}")
                    return True
            return False
        except Exception as e:
            print(f"✗ {get_text('log_brave_error', self.lang)}: {str(e)}")
            return False

    def run(self):
        try:
            elevate(graphical=False)
        except Exception:
            print(get_text('log_admin_required_bloat', self.lang))
            return

        print("Windows System Unfucker v1.0 by Samuele Gonnella")
        print("=" * 48)
        
        selected_apps = {}
        print(f"\n{get_text('bloat_info', self.lang)}")
        for app_name, app_code in self.apps.items():
            while True:
                choice = input(f"{get_text('log_removing', self.lang)} {app_name}? (y/n): ").lower()
                if choice in ['y', 'n']:
                    if choice == 'y':
                        selected_apps[app_name] = app_code
                    break

        while True:
            choice = input(f"\n{get_text('title_disable_ads', self.lang)}? (y/n): ").lower()
            if choice in ['y', 'n']:
                disable_ads_flag = choice == 'y'
                break

        while True:
            choice = input(f"\n{get_text('title_vscode', self.lang)}? (y/n): ").lower()
            if choice in ['y', 'n']:
                install_vscode_flag = choice == 'y'
                break

        while True:
            choice = input(f"\n{get_text('title_brave', self.lang)}? (y/n): ").lower()
            if choice in ['y', 'n']:
                install_brave_flag = choice == 'y'
                break

        print("\nReview selected actions:")
        if selected_apps:
            print("\nApps to remove:")
            for app in selected_apps:
                print(f"- {app}")
        if disable_ads_flag:
            print("\nWindows Advertisements will be disabled")
        if install_vscode_flag:
            print("VS Code will be installed")
        if install_brave_flag:
            print("Brave Browser will be installed")

        confirm = input(f"\n{get_text('dialog_confirm_title', self.lang)}? (y/n): ").lower()
        if confirm != 'y':
            print(get_text('log_removal_cancelled', self.lang))
            return

        print(f"\n{get_text('log_cleaning_in_progress', self.lang)}")
        if selected_apps:
            self.remove_bloatware(selected_apps)
        if disable_ads_flag:
            self.disable_ads()
        if install_vscode_flag:
            self.install_vscode()
        if install_brave_flag:
            self.install_brave()
        
        print(f"\n{get_text('log_cleaning_complete', self.lang)}")
        input("\nPress Enter to exit...")

def main():
    app = WindowsCleaner()
    app.run()

if __name__ == "__main__":
    main()
