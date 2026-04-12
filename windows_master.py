import customtkinter as ctk
import os
import shutil
import winshell
import datetime
import threading
import sys
import ctypes
import subprocess
import winreg

# --- Constants ---
APP_NAME = "Windows Unfucker Utility"
APP_VERSION = "v2.0"
TASK_NAME = "Windows_Unfucker_Auto_Clean"

# Color Scheme
PRIMARY_COLOR = "#1f6feb"
SECONDARY_COLOR = "#8b5cf6"
SUCCESS_COLOR = "#238636"
WARNING_COLOR = "#fb8500"
DANGER_COLOR = "#da3633"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class WindowsMaster(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title(f"{APP_NAME} {APP_VERSION}")
        self.geometry("900x650")
        self.resizable(False, False)
        
        # Bloatware apps dictionary
        self.bloatware_apps = {
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
            "Clipchamp": "Clipchamp.Clipchamp",
            "DevHome": "Microsoft.DevHome",
            "Microsoft Copilot": "Microsoft.Windows.Copilot",
            "Microsoft Recall": "Microsoft.Recall"
        }
        
        self.bloatware_vars = {}
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Content
        
        # Header
        header_frame = ctk.CTkFrame(self, fg_color=PRIMARY_COLOR, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text=f"🚀 {APP_NAME}",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=15)
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Complete Windows Cleaning and Optimization",
            font=ctk.CTkFont(size=13),
            text_color="#c9d1d9"
        )
        subtitle.pack(pady=(0, 15))
        
        # Tabview
        self.tabview = ctk.CTkTabview(self, width=860, corner_radius=10)
        self.tabview.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        # Create tabs
        self.tab_cleaning = self.tabview.add("🧹 System Cleaning")
        self.tab_bloat = self.tabview.add("🗑️ Remove Bloatware")
        self.tab_optimize = self.tabview.add("⚙️ Optimizations")
        self.tab_log = self.tabview.add("📊 Logs & Reports")
        
        self.setup_cleaning_tab()
        self.setup_bloatware_tab()
        self.setup_optimization_tab()
        self.setup_log_tab()
    
    def setup_cleaning_tab(self):
        frame = self.tab_cleaning
        frame.grid_columnconfigure(0, weight=1)
        
        # Info label
        info = ctk.CTkLabel(
            frame,
            text="Select the cleaning operations to perform:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        info.pack(pady=(10, 20), padx=20, anchor="w")
        
        # Checkboxes
        self.check_recycle = ctk.CTkCheckBox(
            frame, 
            text="♻️  Empty Recycle Bin",
            font=ctk.CTkFont(size=13),
            checkbox_width=22,
            checkbox_height=22
        )
        self.check_recycle.pack(pady=8, padx=30, anchor="w")
        self.check_recycle.select()
        
        self.check_downloads = ctk.CTkCheckBox(
            frame,
            text="📥  Delete obsolete Downloads (> 7 days)",
            font=ctk.CTkFont(size=13),
            checkbox_width=22,
            checkbox_height=22
        )
        self.check_downloads.pack(pady=8, padx=30, anchor="w")
        self.check_downloads.select()
        
        self.check_temp = ctk.CTkCheckBox(
            frame,
            text="🗂️  Clean Temporary Files (User + System)",
            font=ctk.CTkFont(size=13),
            checkbox_width=22,
            checkbox_height=22
        )
        self.check_temp.pack(pady=8, padx=30, anchor="w")
        self.check_temp.select()
        
        self.check_prefetch = ctk.CTkCheckBox(
            frame,
            text="⚡  Clean Prefetch (Requires Admin)",
            font=ctk.CTkFont(size=13),
            checkbox_width=22,
            checkbox_height=22
        )
        self.check_prefetch.pack(pady=8, padx=30, anchor="w")
        self.check_prefetch.select()
        
        self.check_windows_old = ctk.CTkCheckBox(
            frame,
            text="🔧  Delete Windows.old (Requires Admin)",
            font=ctk.CTkFont(size=13),
            checkbox_width=22,
            checkbox_height=22
        )
        self.check_windows_old.pack(pady=8, padx=30, anchor="w")
        
        # Action button
        self.btn_clean = ctk.CTkButton(
            frame,
            text="🚀 START SYSTEM CLEANING",
            command=self.start_cleaning,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=SUCCESS_COLOR,
            hover_color="#2ea043"
        )
        self.btn_clean.pack(pady=30, padx=40, fill="x")
    
    def setup_bloatware_tab(self):
        frame = self.tab_bloat
        frame.grid_columnconfigure(0, weight=1)
        
        info = ctk.CTkLabel(
            frame,
            text="Select the pre-installed apps to remove:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        info.pack(pady=(10, 15), padx=20, anchor="w")
        
        # Scrollable frame for apps
        scroll_frame = ctk.CTkScrollableFrame(frame, width=800, height=250)
        scroll_frame.pack(pady=10, padx=20, fill="x")
        
        # Create checkboxes for each bloatware app
        for app_name in self.bloatware_apps.keys():
            var = ctk.BooleanVar(value=False)
            self.bloatware_vars[app_name] = var
            
            check = ctk.CTkCheckBox(
                scroll_frame,
                text=f"❌  {app_name}",
                variable=var,
                font=ctk.CTkFont(size=13),
                checkbox_width=22,
                checkbox_height=22
            )
            check.pack(pady=5, padx=10, anchor="w")
        
        # Button frame
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=15, padx=20, fill="x")
        
        btn_select_all = ctk.CTkButton(
            btn_frame,
            text="Select All",
            command=self.select_all_bloatware,
            width=150,
            fg_color=SECONDARY_COLOR,
            hover_color="#7c3aed"
        )
        btn_select_all.pack(side="left", padx=5)
        
        btn_deselect_all = ctk.CTkButton(
            btn_frame,
            text="Deselect All",
            command=self.deselect_all_bloatware,
            width=150,
            fg_color="#6e7681",
            hover_color="#484f58"
        )
        btn_deselect_all.pack(side="left", padx=5)
        
        self.btn_remove_bloat = ctk.CTkButton(
            frame,
            text="🗑️ REMOVE SELECTED APPS",
            command=self.start_bloatware_removal,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=DANGER_COLOR,
            hover_color="#b62324"
        )
        self.btn_remove_bloat.pack(pady=15, padx=40, fill="x")
    
    def setup_optimization_tab(self):
        # Create a scrollable frame inside the tab
        scroll_frame = ctk.CTkScrollableFrame(self.tab_optimize, width=820, height=450)
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        scroll_frame.grid_columnconfigure(0, weight=1)
        
        info = ctk.CTkLabel(
            scroll_frame,
            text="Optimizations and Configurations:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        info.pack(pady=(10, 20), padx=20, anchor="w")
        
        # Disable Ads
        ads_frame = ctk.CTkFrame(scroll_frame)
        ads_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            ads_frame,
            text="🚫 Disable Windows Ads",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=10, padx=15, anchor="w")
        
        self.btn_disable_ads = ctk.CTkButton(
            ads_frame,
            text="Disable Ads",
            command=self.disable_ads,
            fg_color=WARNING_COLOR,
            hover_color="#d47100"
        )
        self.btn_disable_ads.pack(pady=10, padx=15)
        
        # Scheduling
        sched_frame = ctk.CTkFrame(scroll_frame)
        sched_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            sched_frame,
            text="📅 Automatic Scheduling (Sunday 10:00 AM)",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=10, padx=15, anchor="w")
        
        btn_frame = ctk.CTkFrame(sched_frame, fg_color="transparent")
        btn_frame.pack(pady=10, padx=15)
        
        self.btn_enable_sched = ctk.CTkButton(
            btn_frame,
            text="✅ Activate",
            command=self.enable_scheduling,
            width=150,
            fg_color=SUCCESS_COLOR,
            hover_color="#2ea043"
        )
        self.btn_enable_sched.pack(side="left", padx=5)
        
        self.btn_disable_sched = ctk.CTkButton(
            btn_frame,
            text="❌ Deactivate",
            command=self.disable_scheduling,
            width=150,
            fg_color=DANGER_COLOR,
            hover_color="#b62324"
        )
        self.btn_disable_sched.pack(side="left", padx=5)
        
        # VS Code Installation
        vscode_frame = ctk.CTkFrame(scroll_frame)
        vscode_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            vscode_frame,
            text="💻 Install Visual Studio Code",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=10, padx=15, anchor="w")
        
        self.btn_install_vscode = ctk.CTkButton(
            vscode_frame,
            text="Install VS Code",
            command=self.install_vscode,
            fg_color=PRIMARY_COLOR,
            hover_color="#1f5fcf"
        )
        self.btn_install_vscode.pack(pady=10, padx=15)
        
        # Brave Browser Installation
        brave_frame = ctk.CTkFrame(scroll_frame)
        brave_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            brave_frame,
            text="🌐 Install Brave Browser",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=10, padx=15, anchor="w")
        
        self.btn_install_brave = ctk.CTkButton(
            brave_frame,
            text="Install Brave",
            command=self.install_brave,
            fg_color="#fb8500",
            hover_color="#ef7000"
        )
        self.btn_install_brave.pack(pady=10, padx=15)
    
    def setup_log_tab(self):
        frame = self.tab_log
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        
        info = ctk.CTkLabel(
            frame,
            text="📋 Operations Log:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        info.grid(row=0, column=0, pady=(10, 10), padx=20, sticky="w")
        
        self.textbox_log = ctk.CTkTextbox(frame, width=820, height=400, font=ctk.CTkFont(size=12))
        self.textbox_log.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.textbox_log.configure(state="disabled")
        
        # Clear log button
        btn_clear = ctk.CTkButton(
            frame,
            text="🗑️ Clear Log",
            command=self.clear_log,
            width=150,
            fg_color="#6e7681",
            hover_color="#484f58"
        )
        btn_clear.grid(row=2, column=0, pady=(0, 15))
    
    def log(self, message, level="INFO"):
        icon = "ℹ️" if level == "INFO" else "✅" if level == "SUCCESS" else "⚠️" if level == "WARNING" else "❌"
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        
        self.textbox_log.configure(state="normal")
        self.textbox_log.insert("end", f"[{timestamp}] {icon} {message}\n")
        self.textbox_log.see("end")
        self.textbox_log.configure(state="disabled")
        
        # Switch to log tab if error
        if level == "ERROR":
            self.tabview.set("📊 Logs & Reports")
    
    def clear_log(self):
        self.textbox_log.configure(state="normal")
        self.textbox_log.delete("1.0", "end")
        self.textbox_log.configure(state="disabled")
    
    def select_all_bloatware(self):
        for var in self.bloatware_vars.values():
            var.set(True)
    
    def deselect_all_bloatware(self):
        for var in self.bloatware_vars.values():
            var.set(False)
    
    # ===== CLEANING OPERATIONS =====
    
    def start_cleaning(self):
        self.btn_clean.configure(state="disabled", text="⏳ Cleaning in progress...")
        threading.Thread(target=self.perform_cleaning, daemon=True).start()
    
    def perform_cleaning(self):
        import pythoncom
        pythoncom.CoInitialize()
        
        self.log("=== SYSTEM CLEANING STARTED ===")
        is_admin = self.is_admin()
        
        if not is_admin:
            self.log("ATTENTION: No administrator privileges. Some operations might fail.", "WARNING")
        
        try:
            # Recycle Bin
            if self.check_recycle.get():
                self.log("Emptying Recycle Bin...")
                try:
                    winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
                    self.log("Recycle Bin emptied successfully", "SUCCESS")
                except Exception as e:
                    self.log(f"Error emptying recycle bin: {e}", "ERROR")
            
            # Downloads
            if self.check_downloads.get():
                downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
                self.clean_folder(downloads_path, days=7, label="Download")
            
            # Temp files
            if self.check_temp.get():
                self.clean_folder(os.environ.get('TEMP'), label="User Temp", days=0)
                if is_admin:
                    self.clean_folder("C:\\Windows\\Temp", label="System Temp", days=0)
            
            # Prefetch
            if self.check_prefetch.get():
                if is_admin:
                    self.clean_folder("C:\\Windows\\Prefetch", label="Prefetch", days=0)
                else:
                    self.log("SKIP: Prefetch requires Admin privileges", "WARNING")
            
            # Windows.old
            if self.check_windows_old.get():
                path = "C:\\Windows.old"
                if os.path.exists(path):
                    if not is_admin:
                        self.log("SKIP: Windows.old requires Admin privileges", "WARNING")
                    else:
                        self.log("Removing Windows.old...")
                        try:
                            subprocess.run(["cmd", "/c", f"rd /s /q {path}"], check=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            self.log("Windows.old successfully removed", "SUCCESS")
                        except Exception as e:
                            self.log(f"Error removing Windows.old: {e}", "ERROR")
                else:
                    self.log("Windows.old not found", "INFO")
            
            self.log("=== CLEANING COMPLETED ===", "SUCCESS")
        finally:
            self.btn_clean.configure(state="normal", text="🚀 START SYSTEM CLEANING")
    
    def clean_folder(self, path, days=0, label=""):
        if not path or not os.path.exists(path):
            self.log(f"Folder {label} not found", "WARNING")
            return
        
        self.log(f"Cleaning {label}...")
        cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
        count = 0
        
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                try:
                    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(item_path))
                    if mtime < cutoff:
                        if os.path.isfile(item_path) or os.path.islink(item_path):
                            os.remove(item_path)
                            count += 1
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                            count += 1
                except:
                    pass
            self.log(f"{label}: Removed {count} items", "SUCCESS")
        except Exception as e:
            self.log(f"Error cleaning {label}: {e}", "ERROR")
    
    # ===== BLOATWARE REMOVAL =====
    
    def start_bloatware_removal(self):
        selected = {name: code for name, code in self.bloatware_apps.items() if self.bloatware_vars[name].get()}
        
        if not selected:
            self.log("No apps selected for removal", "WARNING")
            return
        
        if not self.is_admin():
            self.log("ERROR: Administrator privileges required to remove bloatware", "ERROR")
            return
        
        # Show confirmation dialog
        self.show_confirmation_dialog(selected)
    
    def show_confirmation_dialog(self, selected_apps):
        # Create modal dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("⚠️ Confirm Removal")
        dialog.geometry("500x550")
        dialog.resizable(False, False)
        
        # Make it modal
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (500 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (550 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Warning header
        warning_frame = ctk.CTkFrame(dialog, fg_color=WARNING_COLOR)
        warning_frame.pack(fill="x", padx=0, pady=0)
        
        ctk.CTkLabel(
            warning_frame,
            text="⚠️ CAUTION",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=15)
        
        # Message
        ctk.CTkLabel(
            dialog,
            text="You are about to remove the following applications:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(20, 10), padx=20)
        
        # Scrollable list of apps
        apps_frame = ctk.CTkScrollableFrame(dialog, width=450, height=200)
        apps_frame.pack(pady=10, padx=20)
        
        for app_name in selected_apps.keys():
            ctk.CTkLabel(
                apps_frame,
                text=f"• {app_name}",
                font=ctk.CTkFont(size=13),
                anchor="w"
            ).pack(pady=3, padx=10, anchor="w")
        
        # Warning message
        ctk.CTkLabel(
            dialog,
            text="This operation CANNOT be undone!",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=DANGER_COLOR
        ).pack(pady=(10, 5))
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        def on_cancel():
            dialog.destroy()
            self.log("Removal cancelled by user", "INFO")
        
        def on_confirm():
            dialog.destroy()
            self.btn_remove_bloat.configure(state="disabled", text="⏳ Removal in progress...")
            threading.Thread(target=self.remove_bloatware, args=(selected_apps,), daemon=True).start()
        
        # Cancel button
        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="❌ Cancel",
            command=on_cancel,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#6e7681",
            hover_color="#484f58"
        )
        btn_cancel.pack(side="left", padx=10)
        
        # Confirm button
        btn_confirm = ctk.CTkButton(
            btn_frame,
            text="✅ Confirm Removal",
            command=on_confirm,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=DANGER_COLOR,
            hover_color="#b62324"
        )
        btn_confirm.pack(side="left", padx=10)
    
    def remove_bloatware(self, selected_apps):
        import pythoncom
        pythoncom.CoInitialize()
        
        self.log("=== BLOATWARE REMOVAL STARTED ===")
        total = len(selected_apps)
        
        for i, (app_name, app_code) in enumerate(selected_apps.items(), 1):
            self.log(f"[{i}/{total}] Removing {app_name}...")
            command = f"Get-AppxPackage *{app_code}* | Remove-AppxPackage"
            
            try:
                subprocess.run(["powershell", "-Command", command], check=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                self.log(f"✓ {app_name} successfully removed", "SUCCESS")
            except:
                self.log(f"✗ Unable to remove {app_name}", "ERROR")
        
        self.log("=== BLOATWARE REMOVAL COMPLETED ===", "SUCCESS")
        self.btn_remove_bloat.configure(state="normal", text="🗑️ REMOVE SELECTED APPS")
    
    # ===== OPTIMIZATIONS =====
    
    def disable_ads(self):
        if not self.is_admin():
            self.log("ERROR: Administrator privileges required", "ERROR")
            return
        
        self.log("Disabling Windows ads...")
        self.btn_disable_ads.configure(state="disabled")
        
        try:
            paths = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                r"SOFTWARE\Policies\Microsoft\Windows\CloudContent"
            ]
            for path in paths:
                key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_ALL_ACCESS)
                winreg.SetValueEx(key, "DisableWindowsConsumerFeatures", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
            
            self.log("Windows ads successfully disabled", "SUCCESS")
        except Exception as e:
            self.log(f"Error disabling ads: {e}", "ERROR")
        finally:
            self.btn_disable_ads.configure(state="normal")
    
    def enable_scheduling(self):
        if not self.is_admin():
            self.log("ERROR: Administrator privileges required", "ERROR")
            return
        
        exe_path = sys.executable if not getattr(sys, 'frozen', False) else sys.executable
        cmd = [
            "schtasks", "/create", "/tn", TASK_NAME,
            "/tr", f'"{exe_path}"',
            "/sc", "weekly", "/d", "SUN", "/st", "10:00", "/f", "/rl", "highest"
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log("Scheduling activated: every Sunday at 10:00 AM", "SUCCESS")
        except Exception as e:
            self.log(f"Scheduling error: {e}", "ERROR")
    
    def disable_scheduling(self):
        if not self.is_admin():
            self.log("ERROR: Administrator privileges required", "ERROR")
            return
        
        try:
            subprocess.run(["schtasks", "/delete", "/tn", TASK_NAME, "/f"], check=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log("Scheduling deactivated", "SUCCESS")
        except:
            self.log("No scheduling found", "WARNING")
    
    def install_vscode(self):
        self.log("Downloading VS Code...")
        self.btn_install_vscode.configure(state="disabled", text="⏳ Downloading...")
        
        def download_install():
            try:
                download_cmd = "Invoke-WebRequest -Uri 'https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user' -OutFile 'VSCodeSetup.exe'"
                subprocess.run(["powershell", "-Command", download_cmd], check=True, capture_output=True)
                
                self.log("Installing VS Code...")
                self.btn_install_vscode.configure(text="⏳ Installing...")
                
                install_cmd = "./VSCodeSetup.exe /VERYSILENT /NORESTART /MERGETASKS=!runcode"
                subprocess.run(["powershell", "-Command", install_cmd], check=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                
                os.remove("VSCodeSetup.exe")
                self.log("VS Code successfully installed", "SUCCESS")
            except Exception as e:
                self.log(f"Error installing VS Code: {e}", "ERROR")
            finally:
                self.btn_install_vscode.configure(state="normal", text="Installa VS Code")
        
        threading.Thread(target=download_install, daemon=True).start()
    
    def install_brave(self):
        self.log("Downloading Brave Browser...")
        self.btn_install_brave.configure(state="disabled", text="⏳ Downloading...")
        
        def download_install():
            try:
                # Using winget for Brave as it's more reliable for Chromium-based browsers
                self.log("Installing Brave via Winget...")
                install_cmd = "winget install Brave.Brave --silent --accept-package-agreements --accept-source-agreements"
                result = subprocess.run(["powershell", "-Command", install_cmd], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                
                if result.returncode == 0:
                    self.log("Brave Browser successfully installed", "SUCCESS")
                else:
                    # Fallback to direct download if winget fails
                    self.log("Winget failed, trying direct download...", "WARNING")
                    download_cmd = "Invoke-WebRequest -Uri 'https://laptop-updates.brave.com/latest/winx64' -OutFile 'BraveSetup.exe'"
                    subprocess.run(["powershell", "-Command", download_cmd], check=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    
                    self.log("Running Brave installer...")
                    subprocess.run(["./BraveSetup.exe", "/silent", "/install"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    os.remove("BraveSetup.exe")
                    self.log("Brave Browser successfully installed", "SUCCESS")
            except Exception as e:
                self.log(f"Error installing Brave: {e}", "ERROR")
            finally:
                self.btn_install_brave.configure(state="normal", text="Installa Brave")
        
        threading.Thread(target=download_install, daemon=True).start()
    
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

if __name__ == "__main__":
    app = WindowsMaster()
    app.mainloop()
