import subprocess
import winreg
import os
from elevate import elevate

class WindowsCleaner:
    def __init__(self):
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
            print(f"[{i}/{total}] Removing {app_name}...")
            command = f"Get-AppxPackage *{app_code}* | Remove-AppxPackage"
            if self.run_powershell_command(command):
                print(f"✓ Successfully removed {app_name}")
            else:
                print(f"✗ Failed to remove {app_name}")

    def disable_ads(self):
        print("\nDisabling advertisements...")
        try:
            paths = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                r"SOFTWARE\Policies\Microsoft\Windows\CloudContent"
            ]
            for path in paths:
                key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_ALL_ACCESS)
                winreg.SetValueEx(key, "DisableWindowsConsumerFeatures", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
            print("✓ Successfully disabled advertisements")
        except Exception as e:
            print(f"✗ Failed to disable advertisements: {str(e)}")

    def install_vscode(self):
        print("\nInstalling VS Code...")
        try:
            download_command = "Invoke-WebRequest -Uri 'https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user' -OutFile 'VSCodeSetup.exe'"
            if self.run_powershell_command(download_command):
                install_command = "./VSCodeSetup.exe /VERYSILENT /NORESTART /MERGETASKS=!runcode"
                if self.run_powershell_command(install_command):
                    print("✓ Successfully installed VS Code")
                    os.remove("VSCodeSetup.exe")
                    return True
            print("✗ Failed to install VS Code")
            return False
        except Exception as e:
            print(f"✗ Error installing VS Code: {str(e)}")
            return False

    def install_brave(self):
        print("\nInstalling Brave Browser...")
        try:
            # Using winget for Brave as it's more reliable for Chromium-based browsers
            print("Installing Brave via Winget...")
            install_cmd = "winget install Brave.Brave --silent --accept-package-agreements --accept-source-agreements"
            result = subprocess.run(["powershell", "-Command", install_cmd], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            if result.returncode == 0:
                print("✓ Successfully installed Brave Browser")
                return True
            else:
                # Fallback to direct download if winget fails
                print("Winget failed, trying direct download...")
                download_cmd = "Invoke-WebRequest -Uri 'https://laptop-updates.brave.com/latest/winx64' -OutFile 'BraveSetup.exe'"
                if self.run_powershell_command(download_cmd):
                    print("Running Brave installer...")
                    subprocess.run(["./BraveSetup.exe", "/silent", "/install"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    os.remove("BraveSetup.exe")
                    print("✓ Successfully installed Brave Browser")
                    return True
            return False
        except Exception as e:
            print(f"✗ Error installing Brave Browser: {str(e)}")
            return False

    def run(self):
        try:
            elevate(graphical=False)
        except Exception:
            print("Error: Administrator privileges required!")
            return

        print("Windows System Unfucker v1.0 by Samuele Gonnella")
        print("=" * 48)
        
        selected_apps = {}
        print("\nSelect apps to remove (y/n):")
        for app_name, app_code in self.apps.items():
            while True:
                choice = input(f"Remove {app_name}? (y/n): ").lower()
                if choice in ['y', 'n']:
                    if choice == 'y':
                        selected_apps[app_name] = app_code
                    break

        while True:
            choice = input("\nDisable Windows Advertisements? (y/n): ").lower()
            if choice in ['y', 'n']:
                disable_ads_flag = choice == 'y'
                break

            if choice in ['y', 'n']:
                install_vscode_flag = choice == 'y'
                break

        while True:
            choice = input("\nInstall Brave Browser? (y/n): ").lower()
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

        confirm = input("\nProceed with cleanup? (y/n): ").lower()
        if confirm != 'y':
            print("Operation cancelled.")
            return

        print("\nStarting cleanup...")
        if selected_apps:
            self.remove_bloatware(selected_apps)
        if disable_ads_flag:
            self.disable_ads()
        if install_vscode_flag:
            self.install_vscode()
        if install_brave_flag:
            self.install_brave()
        
        print("\nCleanup completed!")
        input("\nPress Enter to exit...")

def main():
    app = WindowsCleaner()
    app.run()

if __name__ == "__main__":
    main()
